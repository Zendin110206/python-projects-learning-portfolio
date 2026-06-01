player_name = input("Type your name: ").strip()
print(f"Welcome {player_name} to this adventure!")
print("You are on a dirt road. It has come to an end and you can go left or right.")
first_choice_text = input("Which way would you like to go? ")
first_choice = first_choice_text.strip().lower()

if first_choice == "left":
    print("You come to a river. You can walk around it or swim across.")
    river_choice_text = input("Type walk to walk around and swim to swim across: ")
    river_choice = river_choice_text.strip().lower()

    if river_choice == "swim":
        print("You swam across and were eaten by an alligator.")

    elif river_choice == "walk":
        print("You walked for many miles, ran out of water, and lost.")

    else:
        print("Not a valid option. You lose.")

elif first_choice == "right":
    print("You come to a bridge. It looks wobbly.")
    bridge_choice_text = input("Do you want to cross it or head back? Type cross or back: ")
    bridge_choice = bridge_choice_text.strip().lower()

    if bridge_choice == "cross":
        print("You cross the bridge and meet a stranger.")
        stranger_choice_text = input("Do you talk to them? Type yes or no: ")
        stranger_choice = stranger_choice_text.strip().lower()

        if stranger_choice == "yes":
            print("You talk to the stranger and they give you gold. You win!")

        elif stranger_choice == "no":
            print("You ignore the stranger and they are offended. You lose.")

        else:
            print("Not a valid option. You lose.")

    elif bridge_choice == "back":
        print("You go back and lose.")

    else:
        print("Not a valid option. You lose.")

else:
    print("Not a valid option. You lose.")


print(f"Thank you for trying, {player_name}.")
