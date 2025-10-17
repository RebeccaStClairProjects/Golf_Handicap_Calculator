## This is The start of somthing new 
import functions

continu = "yes"  
option = 0

while continu == "Yes" or continu == "yes":
    
    print("Hello and welcome to Polo Park East Men's Club Handicap Calculator\n")
    print("Please select from the following options\n")
    print("1: Add new Golfer\n")
    print("2: Update Golfer Information\n")
    print("3: Add Round Score\n")
    print("4: Display Current Ranking\n")
    
    option = input("please select an option. ")

    if option == "1":
        functions.lookUpGolfer(1)
    elif option == "2":
        functions.lookUpGolfer(2)
    elif option == "3":
        functions.lookUpGolfer(3)
    elif option == "4":
        print("\nThis option has not been implemented")
    elif option == "5":
        print("\nThis option has not been implemented")

    continu = input("\nDo you want to chose another option?")

print("\nThank you for stoping by!")

functions.CloseCurser()