import random as rd

print("Welcome to Rock Paper Scissors!")
valid_choices = ["rock", "paper", "scissors"]
player_wins = 0
computer_wins = 0

while True:
    player_choice_text = input("Type rock, paper, scissors, or q to quit: ")
    player_choice = player_choice_text.strip().lower()

    if player_choice == "q":
        break

    if player_choice not in valid_choices:
        print("Please type rock, paper, scissors, or q.")
        continue

    computer_choice = rd.choice(valid_choices)
    print(f"Computer picked {computer_choice}.")

    if player_choice == "scissors" and computer_choice == "paper":
        print("You won!")
        player_wins += 1

    elif player_choice == "paper" and computer_choice == "rock":
        print("You won!")
        player_wins += 1

    elif player_choice == "rock" and computer_choice == "scissors":
        print("You won!")
        player_wins += 1

    elif player_choice == computer_choice:
        print("It's a tie!")

    else:
        print("You lost!")
        computer_wins += 1

print(f"You won {player_wins} times.")
print(f"The computer won {computer_wins} times.")
print("Goodbye!")
