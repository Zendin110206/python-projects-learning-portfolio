print("Welcome to the Computer Quiz!")

play_choice = input("Do you want to play? (yes / no): ")
if play_choice.strip().lower() == "yes":
    print("Okay, let's play!")
    score = 0
    total_questions = 4

    cpu_answer = input("\nWhat does CPU stand for? ")
    if cpu_answer.strip().lower() == "central processing unit":
        print("Correct!")
        score += 1
    else:
        print("Incorrect!")

    gpu_answer = input("\nWhat does GPU stand for? ")
    if gpu_answer.strip().lower() == "graphics processing unit":
        print("Correct!")
        score += 1
    else:
        print("Incorrect!")

    ram_answer = input("\nWhat does RAM stand for? ")
    if ram_answer.strip().lower() == "random access memory":
        print("Correct!")
        score += 1
    else:
        print("Incorrect!")

    psu_answer = input("\nWhat does PSU stand for? ")
    if psu_answer.strip().lower() == "power supply":
        print("Correct!")
        score += 1
    else:
        print("Incorrect!")

    print(f"You got {score} questions correct.")
    print(f"You got {(score / total_questions) * 100}%.")

else:
    print("Maybe next time!")
