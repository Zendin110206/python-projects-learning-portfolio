from pathlib import Path

project_dir = Path(__file__).parent.parent
story_file = project_dir / "story.txt"


def find_placeholders(story):
    placeholders = []
    start_index = -1

    for index, character in enumerate(story):
        if character == "<":
            start_index = index

        if character == ">" and start_index != -1:
            placeholder = story[start_index : index + 1]
            if placeholder not in placeholders:
                placeholders.append(placeholder)
            start_index = -1

    return placeholders


def collect_answers(placeholders):
    answers = {}

    for placeholder in placeholders:
        answer = input(f"Enter a word for {placeholder}: ")
        answers[placeholder] = answer

    return answers


def build_story(story, answers):
    completed_story = story
    for placeholder, answer in answers.items():
        completed_story = completed_story.replace(placeholder, answer)
    return completed_story


def main():
    story = story_file.read_text(encoding="utf-8")
    placeholders = find_placeholders(story)
    answers = collect_answers(placeholders)
    completed_story = build_story(story, answers)
    print("\nHere is your completed story:")
    print(completed_story)


if __name__ == "__main__":
    main()
