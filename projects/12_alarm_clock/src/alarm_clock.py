import time


def parse_duration(duration_text):
    duration_text = duration_text.strip()
    parts = duration_text.split(":")

    if len(parts) != 3:
        print("Invalid format. Please use HH:MM:SS.")
        return None

    for part in parts:
        if not part.isdigit():
            print("Invalid format. Please use HH:MM:SS.")
            return None

    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])

    if hours == 0 and minutes == 0 and seconds == 0:
        print("Duration must be greater than 0 seconds.")
        return None

    if minutes >= 60 or seconds >= 60:
        print("Minutes and seconds must be between 0 and 59.")
        return None

    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def format_duration(total_seconds):
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return formatted_time


def get_alarm_duration():
    while True:
        duration_text = input("Enter alarm duration (HH:MM:SS): ")
        total_seconds = parse_duration(duration_text)

        if total_seconds is not None:
            return total_seconds


def run_countdown(total_seconds):
    while total_seconds > 0:
        formatted_time = format_duration(total_seconds)
        print(f"Time remaining: {formatted_time}")

        time.sleep(1)
        total_seconds -= 1

    print("Wake up! Alarm finished.")


def main():
    total_seconds = get_alarm_duration()
    formatted_time = format_duration(total_seconds)
    print(f"Alarm set for {formatted_time}.")
    run_countdown(total_seconds)


if __name__ == "__main__":
    main()
