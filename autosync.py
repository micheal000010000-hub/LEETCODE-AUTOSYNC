from repo_manager import add_new_solution
from git_manager import push_to_github


def main():
    print("==== LeetCode AutoSync ====")
    print("1 → Add new solution locally")
    print("2 → Push existing changes to GitHub")

    choice = input("Select option (1 or 2): ").strip()

    if choice == "1":
        problem_number = input("Problem number: ").strip()
        problem_name = input("Problem name: ").strip()
        difficulty = input("Difficulty (easy/medium/hard): ").strip()
        link = input("Problem link: ").strip()

        print("Paste your solution below. Type END on a new line to finish:")

        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        solution_code = "\n".join(lines)

        add_new_solution(
            problem_number,
            problem_name,
            difficulty,
            link,
            solution_code
        )

    elif choice == "2":
        push_to_github()

    else:
        print("Invalid option selected.")


if __name__ == "__main__":
    main()