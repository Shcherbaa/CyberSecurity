import re
from pathlib import Path

EXERCISES_DIR = Path(__file__).parent / "exercises"


def list_exercises():
    return sorted(EXERCISES_DIR.glob("*.txt"))


def show_menu(exercises):
    print("\nExercises:")
    if not exercises:
        print("(no .txt files in the exercises folder)")
    for number, exercise in enumerate(exercises, start=1):
        print(f"{number}. {exercise.name}")
    print("f. Use your own file")
    print("q. Quit")


def ask_own_file():
    path_text = input("Path to your file: ")
    # "Copy as path" on Windows adds quotes around the path
    path_text = path_text.strip().replace('"', "")
    path = Path(path_text)
    if path.is_file():
        return path
    print(f"File not found: {path}")
    return None


# Returns None when the user wants to quit
def choose_exercise(exercises):
    while True:
        choice = input("Your choice: ").strip().lower()

        if choice == "q":
            return None

        if choice == "f":
            own_file = ask_own_file()
            if own_file is not None:
                return own_file
            continue

        try:
            number = int(choice)
        except ValueError:
            print("Please enter a number from the list, f or q.")
            continue

        if number < 1 or number > len(exercises):
            print("This number is not in the list.")
            continue

        return exercises[number - 1]


# Returns None when the regex is empty or invalid
def ask_pattern():
    pattern_text = input("Regex: ")
    if pattern_text == "":
        print("Invalid regex: the pattern is empty.")
        return None
    try:
        return re.compile(pattern_text)
    except re.error as error:
        print(f"Invalid regex: {error}")
        return None


# Returns None when the file cannot be read
def read_text(path):
    try:
        # errors="replace" lets us open files that are not in UTF-8
        with open(path, "r", encoding="utf-8", errors="replace") as file:
            return file.read()
    except OSError as error:
        print(f"Cannot read the file: {error}")
        return None


def find_matches(pattern, text):
    matches = []
    # finditer gives the full match, findall would return only the groups
    for match in pattern.finditer(text):
        matches.append(match.group())
    return matches


def show_results(matches):
    if not matches:
        print("No matches found.")
        return
    for match in matches:
        print(match)
    print(f"Total matches: {len(matches)}")


def main():
    exercises = list_exercises()

    while True:
        show_menu(exercises)
        exercise = choose_exercise(exercises)
        if exercise is None:
            break

        pattern = ask_pattern()
        if pattern is None:
            continue

        text = read_text(exercise)
        if text is None:
            continue

        show_results(find_matches(pattern, text))


if __name__ == "__main__":
    main()
