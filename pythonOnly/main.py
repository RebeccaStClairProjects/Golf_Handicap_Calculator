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
    print("4: Calculare Missing Handicaps\n")
    print("5: Recalculare All Handicaps For One Golfer\n")
    
    option = input("please select an option. ")

    if option == "1":
        functions.lookUpGolfer(1)
    elif option == "2":
        functions.lookUpGolfer(2)
    elif option == "3":
        functions.lookUpGolfer(3)
    elif option == "4":
        # functions.lookUpGolfer(4)
        functions.calculateEmpty() #Hardcoded for testing, use above code for implimenting golfer search first.
    elif option == "5":
        # functions.lookUpGolfer(5)
        golferInput = input("Select a golfer by ID between 1 and 29 ")
        functions.calculateAll(golferInput) #Hardcoded for testing, use above code for implimenting golfer search first.

    continu = input("\nDo you want to chose another option?")

print("\nThank you for stoping by!")

functions.CloseCurser()