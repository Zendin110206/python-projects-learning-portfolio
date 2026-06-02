import random as rd
import time

OPERATORS = ["+", "-", "*"]
MIN_OPERAND = 3
MAX_OPERAND = 12
TOTAL_PROBLEMS = 10


def calculate_answer(*, left_operand: int, right_operand: int, operator: str) -> int:
    if operator == "+":
        return left_operand + right_operand
    if operator == "-":
        return left_operand - right_operand
    if operator == "*":
        return left_operand * right_operand

    msg = f"Unsupported operator: {operator}"
    raise ValueError(msg)


def generate_problem():
    left_operand = rd.randint(MIN_OPERAND, MAX_OPERAND)
    right_operand = rd.randint(MIN_OPERAND, MAX_OPERAND)
    operator = rd.choice(OPERATORS)
    answer = calculate_answer(
        left_operand=left_operand,
        right_operand=right_operand,
        operator=operator,
    )
    expression = f"{left_operand} {operator} {right_operand}"

    return expression, answer


def run_challenge():
    wrong_attempts = 0
    for problem_number in range(1, TOTAL_PROBLEMS + 1):
        expression, answer = generate_problem()
        prompt = f"Problem #{problem_number}: {expression} = "

        while True:
            guess = input(prompt)
            if guess == str(answer):
                break

            wrong_attempts += 1

    return wrong_attempts


def main():
    input("Press enter to start.")
    print("-" * 22)
    start_time = time.time()

    wrong_attempts = run_challenge()

    end_time = time.time()
    total_time = round(end_time - start_time, 2)

    print("-" * 22)
    print(f"Nice work! You finished in {total_time} seconds.")
    print(f"You made {wrong_attempts} incorrect attempts.")


if __name__ == "__main__":
    main()
