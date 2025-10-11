## This is The start of somthing new 
import functions
continu = "yes"  
option = 0

while continu == "Yes" or continu == "yes":
    
    print("Hello and welcome to polo Park East Men's Club Handicap Calculator\n")
    print("pleas select from the falowing options\n")
    print("1: Add new Golfer\n")
    print("2: Updat Golfer Information\n")
    print("3: Add Round Score\n")
    print("4: Display Curent Ranking\n")
    
    option = input("pleas select an option. ")

    if option == "1":
        functions.add_new_golfer()
    elif option == "2":
        print("\nThis option has not ben implumented")
    elif option == "3":
        functions.Add_New_Score()
    elif option == "4":
        print("\nThis option has not ben implumented")
    elif option == "5":
        print("\nThis option has not ben implumented")

    continu = input("\nDo you want to chose another option?")

print("\nThank you for stoping by!")
