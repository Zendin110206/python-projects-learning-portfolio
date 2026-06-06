import importlib.util
import io
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock, patch

import pytest
import requests

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "16_currency_converter" / "src" / "currency_converter.py"

SAMPLE_CURRENCIES_RESPONSE = [
    {"iso_code": "USD", "name": "United States Dollar"},
    {"iso_code": "IDR", "name": "Indonesian Rupiah"},
    {"iso_code": "EUR", "name": "Euro"},
]

SAMPLE_RATE_RESPONSE = [
    {
        "date": "2026-06-04",
        "base": "USD",
        "quote": "IDR",
        "rate": 17952,
    }
]


def load_currency_converter() -> ModuleType:
    spec = importlib.util.spec_from_file_location("currency_converter_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def call_with_inputs(function, player_inputs: list[str], *args):
    inputs = iter(player_inputs)
    output = io.StringIO()

    def fake_input(prompt: str = "") -> str:
        print(prompt, end="")
        return next(inputs)

    with patch("builtins.input", fake_input), redirect_stdout(output):
        result = function(*args)

    return result, output.getvalue()


def test_module_import_does_not_prompt_or_request_api() -> None:
    with (
        patch("builtins.input") as input_mock,
        patch("requests.get") as get,
    ):
        load_currency_converter()

    input_mock.assert_not_called()
    get.assert_not_called()


def test_fetch_json_uses_timeout_and_params() -> None:
    currency_converter = load_currency_converter()
    response = Mock()
    response.json.return_value = SAMPLE_RATE_RESPONSE

    with patch.object(currency_converter.requests, "get", return_value=response) as get:
        data = currency_converter.fetch_json(
            "/rates",
            params={"base": "USD", "quotes": "IDR"},
        )

    assert data == SAMPLE_RATE_RESPONSE
    get.assert_called_once_with(
        "https://api.frankfurter.dev/v2/rates",
        params={"base": "USD", "quotes": "IDR"},
        timeout=10,
    )
    response.raise_for_status.assert_called_once_with()


def test_fetch_json_wraps_request_and_json_errors() -> None:
    currency_converter = load_currency_converter()
    response = Mock()
    response.json.side_effect = ValueError("not json")

    with patch.object(currency_converter.requests, "get", return_value=response):
        with pytest.raises(currency_converter.CurrencyApiError):
            currency_converter.fetch_json("/currencies")

    with patch.object(
        currency_converter.requests,
        "get",
        side_effect=requests.RequestException("network error"),
    ):
        with pytest.raises(currency_converter.CurrencyApiError):
            currency_converter.fetch_json("/currencies")


def test_fetch_currencies_parses_supported_currency_map() -> None:
    currency_converter = load_currency_converter()

    with patch.object(
        currency_converter,
        "fetch_json",
        return_value=SAMPLE_CURRENCIES_RESPONSE,
    ):
        currencies = currency_converter.fetch_currencies()

    assert currencies == {
        "USD": "United States Dollar",
        "IDR": "Indonesian Rupiah",
        "EUR": "Euro",
    }


def test_fetch_currencies_rejects_invalid_response_shape() -> None:
    currency_converter = load_currency_converter()

    with patch.object(currency_converter, "fetch_json", return_value=[]):
        with pytest.raises(currency_converter.CurrencyApiError):
            currency_converter.fetch_currencies()

    with patch.object(currency_converter, "fetch_json", return_value={"USD": "Dollar"}):
        with pytest.raises(currency_converter.CurrencyApiError):
            currency_converter.fetch_currencies()


def test_fetch_exchange_rate_parses_decimal_rate() -> None:
    currency_converter = load_currency_converter()

    with patch.object(currency_converter, "fetch_json", return_value=SAMPLE_RATE_RESPONSE) as fetch:
        rate = currency_converter.fetch_exchange_rate("USD", "IDR")

    assert rate == Decimal("17952")
    fetch.assert_called_once_with(
        "/rates",
        params={"base": "USD", "quotes": "IDR"},
    )


def test_fetch_exchange_rate_rejects_invalid_response_shape() -> None:
    currency_converter = load_currency_converter()

    for response in ([], [{"rate": "Infinity"}], [{"missing": 1}]):
        with patch.object(currency_converter, "fetch_json", return_value=response):
            with pytest.raises(currency_converter.CurrencyApiError):
                currency_converter.fetch_exchange_rate("USD", "IDR")


def test_normalize_and_validate_currency_codes() -> None:
    currency_converter = load_currency_converter()
    currencies = {"USD": "United States Dollar", "IDR": "Indonesian Rupiah"}

    assert currency_converter.normalize_currency(" usd ") == "USD"
    assert currency_converter.is_supported_currency("USD", currencies) is True
    assert currency_converter.is_supported_currency("ABC", currencies) is False


def test_parse_amount_accepts_positive_finite_numbers_only() -> None:
    currency_converter = load_currency_converter()

    assert currency_converter.parse_amount("10") == Decimal("10")
    assert currency_converter.parse_amount("12500.50") == Decimal("12500.50")
    assert currency_converter.parse_amount("0") is None
    assert currency_converter.parse_amount("-5") is None
    assert currency_converter.parse_amount("abc") is None
    assert currency_converter.parse_amount("Infinity") is None


def test_conversion_and_formatting_helpers() -> None:
    currency_converter = load_currency_converter()

    converted_amount = currency_converter.convert_amount(
        Decimal("10"),
        Decimal("17952"),
    )

    assert converted_amount == Decimal("179520.00")
    assert currency_converter.format_rate("USD", "IDR", Decimal("17952")) == (
        "1 USD = 17952.0000 IDR"
    )
    assert currency_converter.format_conversion(
        Decimal("10"),
        "USD",
        converted_amount,
        "IDR",
    ) == "10.00 USD = 179520.00 IDR"


def test_format_currency_list_sorts_by_currency_code() -> None:
    currency_converter = load_currency_converter()

    output = currency_converter.format_currency_list(
        {
            "USD": "United States Dollar",
            "IDR": "Indonesian Rupiah",
            "EUR": "Euro",
        }
    )

    assert output == (
        "Supported Currencies\n"
        "EUR - Euro\n"
        "IDR - Indonesian Rupiah\n"
        "USD - United States Dollar"
    )


def test_main_handles_list_and_exit() -> None:
    currency_converter = load_currency_converter()

    with patch.object(
        currency_converter,
        "fetch_currencies",
        return_value={"USD": "United States Dollar", "IDR": "Indonesian Rupiah"},
    ):
        _, output = call_with_inputs(currency_converter.main, ["list", "q"])

    assert "Supported Currencies" in output
    assert "IDR - Indonesian Rupiah" in output
    assert output.rstrip().endswith("Goodbye.")


def test_main_handles_rate_command() -> None:
    currency_converter = load_currency_converter()

    with (
        patch.object(
            currency_converter,
            "fetch_currencies",
            return_value={"USD": "United States Dollar", "IDR": "Indonesian Rupiah"},
        ),
        patch.object(
            currency_converter,
            "fetch_exchange_rate",
            return_value=Decimal("17952"),
        ),
    ):
        _, output = call_with_inputs(currency_converter.main, ["rate", "usd", "idr", "q"])

    assert "1 USD = 17952.0000 IDR" in output


def test_main_handles_convert_command() -> None:
    currency_converter = load_currency_converter()

    with (
        patch.object(
            currency_converter,
            "fetch_currencies",
            return_value={"USD": "United States Dollar", "IDR": "Indonesian Rupiah"},
        ),
        patch.object(
            currency_converter,
            "fetch_exchange_rate",
            return_value=Decimal("17952"),
        ),
    ):
        _, output = call_with_inputs(
            currency_converter.main,
            ["convert", "usd", "10", "idr", "q"],
        )

    assert "10.00 USD = 179520.00 IDR" in output


def test_main_handles_invalid_command_currency_amount_and_api_error() -> None:
    currency_converter = load_currency_converter()

    with (
        patch.object(
            currency_converter,
            "fetch_currencies",
            side_effect=[
                {"USD": "United States Dollar"},
                {"USD": "United States Dollar", "IDR": "Indonesian Rupiah"},
                currency_converter.CurrencyApiError(),
            ],
        ),
        patch.object(currency_converter, "fetch_exchange_rate", return_value=Decimal("1")),
    ):
        _, output = call_with_inputs(
            currency_converter.main,
            [
                "hello",
                "rate",
                "abc",
                "idr",
                "convert",
                "usd",
                "-5",
                "idr",
                "list",
                "q",
            ],
        )

    assert "Unrecognized command." in output
    assert "Invalid currency code." in output
    assert "Amount must be a positive number." in output
    assert currency_converter.API_ERROR_MESSAGE in output
    assert output.rstrip().endswith("Goodbye.")
