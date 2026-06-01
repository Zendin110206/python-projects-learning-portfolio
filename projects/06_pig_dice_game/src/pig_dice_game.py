import random as rd

min_players = 2
max_players = 4
target_score = 50


def roll_die():
    return rd.randint(1, 6)


def get_player_count():
    while True:
        player_count_text = input("Enter the number of players (2 - 4): ")

        if not player_count_text.isdigit():
            print("Invalid input. Please enter a number.")
            continue

        player_count = int(player_count_text)

        if player_count < min_players or player_count > max_players:
            print("Player count must be between 2 and 4.")
            continue

        return player_count


def main():
    player_count = get_player_count()
    player_scores = [0 for _ in range(player_count)]

    while max(player_scores) < target_score:
        for player_index in range(0, player_count):
            current_score = 0
            print(f"Player {player_index + 1} turn has started.")
            print(f"Your total score is {player_scores[player_index]}.")

            while True:
                should_roll_text = input("Would you like to roll? ")
                should_roll = should_roll_text.strip().lower()

                if should_roll != "y":
                    player_scores[player_index] += current_score
                    print(f"Your total score is {player_scores[player_index]}.")
                    break

                roll_value = roll_die()

                if roll_value == 1:
                    print("You rolled a 1. Turn over with no points.")
                    current_score = 0
                    print(f"Your total score is {player_scores[player_index]}.")
                    break

                print(f"You rolled a {roll_value}.")
                current_score += roll_value
                print(f"Your current turn score is {current_score}.")

                if player_scores[player_index] + current_score >= target_score:
                    player_scores[player_index] += current_score
                    print(f"Your total score is {player_scores[player_index]}.")
                    break

            if player_scores[player_index] >= target_score:
                break

    winning_score = max(player_scores)
    winning_player_index = player_scores.index(winning_score)
    print(f"Player {winning_player_index + 1} wins with a score of {winning_score}!")


if __name__ == "__main__":
    main()
