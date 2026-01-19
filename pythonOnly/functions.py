import re
import difflib
import calculations

from tkinter import YES
import mysql.connector
conn = mysql.connector.connect(
    host = "rebeccaastclair.helioho.st",
    username = "rebeccastclair_golf",
    password = "BakuraCofh123",
    database = "rebeccastclair_handicap_calculator"
    ## ssl_ca = "path-to-ssl-certificate"  # often optional for simple setups
)
cursor = conn.cursor(buffered=True,dictionary=True)
from datetime import datetime, date, time

def dedupe(rows):
    seen, out = set(), []
    for r in rows:
        if r['golferID'] not in seen:
            seen.add(r['golferID'])
            out.append(r)
    return out


def lookUpCorse():
    courseRating = 58.2 #                                                                                 FIX ME !!!
    courseSlope = 97 #                                                                                     FIX ME !!! 
    coursePar = 58 # Hardcoded course information till course look up function Implemented                FIX ME !!! 

    return courseRating, courseSlope, coursePar
         # courseRating, courseSlope, coursePar = lookUpGolfer(option)


def lookUpGolfer(option):
    name_pattern = r"^[A-Za-z. '\-]+$"
    golfer = None
    
    # Option 1 means adding a new golfer 
    # Option 2 means updating a golfer's information
    # Option 3 means adding a new set of scores
    if option == 1:
        print("First, let's check if the golfer is already in the system. ")
    elif option == 2:
        print("First, we need to look up which golfer to update. ")
    elif option == 3:
        print("First, we need to look up which golfer the scores will be assigned to. ")
    elif option == 5:
        print("First, we need to look up which golfer to recalculate handicaps ")

    while golfer == None:
        #Variables set for repeating if names are entered with invaled symbols
        repetFirst = True
        repetLast = True

        #Enter Golfers First name and check if there are any invalid symbols 
        while repetFirst == True:
            firstName = input("Enter the player's first name: ").strip().title()
            if not re.match(name_pattern, firstName):
                print("Invalid first name. Please use only letters, spaces, or periods.")
            else:
                repetFirst = False

        #Enter Golfers Last name and check if there are any invalid symbols 
        while repetLast == True:
            lastName = input("enter the players last name: ").strip().title()
            if not re.match(name_pattern, lastName):
                print("Invalid last name. Please use only letters, spaces, or periods.")
            else:
                repetLast = False 

        #look up the golfer and the fields that will be needed later
        cursor.execute("""
            SELECT *
            FROM Golfer g
            WHERE g.firstName = %s AND g.lastName = %s
            """, (firstName,lastName))
    
        #Creating the golfer item that holds the 5 variables with labels to their column
        golfer = cursor.fetchone()
                
        # If the name combination was not found in the database
        if golfer == None:
            #Check if the First name is found
            cursor.execute("""
                SELECT *
                FROM Golfer g
                WHERE g.firstName = %s
            """, (firstName,))
            firstMatches = cursor.fetchall()
                       
            #Check if the Last name is found
            cursor.execute("""
            SELECT *
            FROM Golfer g
            WHERE g.lastName = %s
            """, (lastName,))
            lastMatches = cursor.fetchall()
            suggestion = []
            if not firstMatches and not lastMatches and lastName:
                cursor.execute("SELECT lastName FROM Golfer")
                allLastNames = [row['lastName'] for row in cursor.fetchall()]
                close = difflib.get_close_matches(lastName, allLastNames, n=5, cutoff=0.72)
                if close:
                    qmarks = ",".join(["%s"] * len(close))
                    cursor.execute(f"""
                        SELECT *
                        FROM Golfer
                        WHERE lastName IN ({qmarks})
                        ORDER BY lastName, firstName
                    """, tuple(close))
                    suggestionLast = cursor.fetchall()
                    suggestion = suggestionLast
            if not firstMatches and not lastMatches and firstName:
                cursor.execute("SELECT firstName FROM Golfer")
                allFisrtNames = [row['firstName'] for row in cursor.fetchall()]
                close = difflib.get_close_matches(firstName, allFisrtNames, n=5, cutoff=0.72)
                if close:
                    qmarks = ",".join(["%s"] * len(close))
                    cursor.execute(f"""
                        SELECT *
                        FROM Golfer
                        WHERE firstName IN ({qmarks})
                        ORDER BY lastName, firstName
                    """, tuple(close))
                    suggestionFirst = cursor.fetchall()
                    suggestion = suggestionFirst

            if suggestion:
                candidates = dedupe(firstMatches + lastMatches + suggestion)
            else:
                candidates = dedupe(firstMatches + lastMatches)

            if not candidates:
                print("No exact match found, and no close matches either.")
            else:
                print("\nNo exact match. Did you mean:")
                for i, g in enumerate(candidates, start=1):          
                    fn = g['firstName'].title()
                    ln = g['lastName'].title()
                    print(f"{i}. {fn} {ln}")
                print("0. None of these")

                # Prompt until valid selection
                repetList = True

                while repetList == True:
                    choice = input("Select a number: ").strip()
                    if choice.isdigit():
                        n = int(choice)
                        if n == 0:
                            if option == 1:
                                print("Since none of those options are what you are looking for lets add a new golfer.")
                                addNewGolfer(firstName,lastName)
                                return
                            if option == 2 or option == 3:
                                print("Since a match could not be found do you want to add the golfer")
                                selection = input ("enter Yes or No")
                                if selection.strip().lower() == "yes":
                                    addNewGolfer(firstName,lastName)
                                    return
                                else:
                                    repetList = False
                        if 1 <= n <= len(candidates):
                            chosen = candidates[n-1]
                            print(f"Selected: {chosen['firstName'].title()} {chosen['lastName'].title()}")
                            repetList = False
                        else:
                            print("Invalid selection. Please enter a number from the list.")
                    else:
                        print("Invalid selection. Please enter a number from the list.")
                    
                    # If the name combunation was not found in the database
                golfer = chosen

            if golfer == None:
                print("Would you like to\n")
                chose = input()
                if chose == '2':
                    addNewGolfer()
                    return
                elif chose == '3':
                    return

    if option == 1:
        print(f"handicap: {golfer['handicap']} | Number of Rounds Played: {golfer['roundsPlayed']} | Round Averege: {golfer['roundAvg']} | Season Total: {golfer['seasonTotal']}")
        print("No need to add them")
        return
    if option == 2:
        print("\nThis option has not been implemented 2")
        return
    if option == 3:
        addNewScore(golfer)
        return
    if option == 4:
        print("\nThis option has not been implemented 4")
        return
    if option == 5:
        calculateEmpty(golfer)
        return


def addNewGolfer(firstName, lastName):
    #The user is sent to the lookUpGolfer function first, and if the golfer is not found, they are sent here to enter the remaining data
    handicap = input("\nPlease enter handicap. ")
    roundsPlayed = input("\nPlease enter The number of rounds you have played. ")
    roundAvg = input("\nPlease enter your round average. ")
    seasonTotal = input("\nPlease enter your season total. ")
    
    # Inset a new golfer into the database
    cursor.execute("INSERT INTO Golfer(firstName, lastName, handicap, roundsPlayed, roundAvg, seasonTotal) VALUES (%s, %s, %s, %s, %s, %s)",
               (firstName, lastName, handicap, roundsPlayed, roundAvg, seasonTotal))
    # Commit the insert to the database
    conn.commit()


def findPreviasScoreDetails(golferID, roundDate):

    #Pool the most recent 19 scores from the database, the new score makes 20
    cursor.execute("""
       SELECT scoreDiffer
       FROM Rounds
       WHERE golferID = %s 
           AND roundDate < %s
       ORDER by roundDate DESC LIMIT 19
       """, (golferID, roundDate))
    
    # Put those 19 Dictionary items into a Variable then change the dictionary to an Array
    rows = cursor.fetchall()  
    proceeding20Scores = [row['scoreDiffer'] for row in rows]

    cursor.execute("""
         
        SELECT runningHandicap
        FROM Rounds
        WHERE golferID = %s 
          AND roundDate < (%s) 
        ORDER by runningHandicap ASC
        """, (golferID, roundDate))

    HandicapPast365 = cursor.fetchone()
    
    if HandicapPast365 is None:
        lowestProceedingHandicap = 15
    else:
        # Convert from a dictionary to a single variable
        lowestProceedingHandicap = HandicapPast365['runningHandicap']

    return proceeding20Scores, lowestProceedingHandicap 
         # proceeding20Scores, lowestProceedingHandicap = findPreviasScoreDetails(golferID, roundDate)


def addNewScore(golfer):
    #Initiate before reference
    total = 0  
    holeNumber = 0

    courseRating, courseSlope, coursePar = lookUpCorse()
  
    # gets the golfer ID from the golfer item
    #firstName = golfer['firstName']
    #lastName = golfer['lastName']
    golferID = golfer['golferID']

    #Prompt the user for the date and time of the game played.
    userDate = input("\nEnter the date for this round (MM-DD-YYYY or MM/DD/YYYY)? ")
    userTime = input("\nEnter the start time for this round (HH:MM, 24-hour format): ")

    # If Date is not entered this will use the current date.
    if userDate:
        userDate = re.sub(r"[/-]", "-", userDate)  # normalize separators
        datePlayed = datetime.strptime(userDate, "%m-%d-%Y").date()
    else:
        datePlayed = datetime.today().date()

    # If Time is not entered this will use the curent time.
    if userTime:
        startTime = datetime.strptime(userTime, "%H:%M").time()
    else:
        startTime = datetime.now().time()

    #Combines the date and time into one date time variable
    roundDate = datetime.combine(datePlayed, startTime)


    #Prompt whether its 9 or 18 holes then initialize the array to the corect langth
    while holeNumber != 9 and holeNumber != 18:
        holeNumber = int(input("\nWas this 9 or 18 holes? "))
    
    scoresAll = [0]* holeNumber    
    
    # Run through each element in the aray, prompt for the player's score and add to a running total
    for i in range(holeNumber):
        scoresAll[i] = int(input("\nPlease enter the score for hole " + str(i + 1) + ". "))
        total = total + scoresAll[i]        

    # FIX ME!!! Add functionality for max hole bassed on Net +2. May need two tables to track actual scores and maximum hole score for calculateding hadicap. 

    # Golfer contains 5 items (golferID, handicap, roundsPlayed, roundAvg, seasonTotal)   

    # FIX ME !!! Pull Out to its own function
    roundsPlayed = golfer['roundsPlayed'] + 1
    seasonTotal = golfer['seasonTotal'] + (total - coursePar)                                                    
    roundAvg = round((seasonTotal / roundsPlayed),2)

    scoreDiffer = calculations.scoreDiffer(total, holeNumber, courseRating, courseSlope)  

    proceeding20Scores, lowestProceedingHandicap = findPreviasScoreDetails(golferID, roundDate)

    #Takes the Golfer ID and Score differential and calculates the golfer's handicap index
    handicapIndex = calculations.handicap(scoreDiffer, proceeding20Scores, lowestProceedingHandicap) 
        
    # Update the Golfer Deta   
    cursor.execute("""
    UPDATE Golfer
    SET handicap = %s,
        roundsPlayed = %s,
         roundAvg = %s,
         seasonTotal = %s,
         provitional = %s
    WHERE golferID = %s
    """, (handicapIndex, roundsPlayed, roundAvg, seasonTotal,provitional, golferID))
    conn.commit()
    # FIX ME.  Remove provitional

    #Insert new round into score table
    if holeNumber == 9:        
        # Inset a new score set into the database
        cursor.execute("""INSERT INTO Rounds(golferID, roundDate, holes, total, scoreDiffer, runningHandicap, hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8, hole9) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
               (golferID, roundDate, 9, total, scoreDiffer, handicapIndex, scoresAll[0], scoresAll[1], scoresAll[2], scoresAll[3],scoresAll[4], scoresAll[5], scoresAll[6], scoresAll[7], scoresAll[8]))
        # Commit the insert to the database
        conn.commit()
    else:        
        # Inset a new score set into the database
        cursor.execute("""INSERT INTO Rounds(( golferID, roundDate, holes, total, scoreDiffer, runningHandicap, hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8, hole9, hole10, hole11, hole12, hole13, Hole_14, Hole_15, hole16, hole17, hole18) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
               (golferID, roundDate, 18, total, scoreDiffer, handicapIndex, scoresAll[0], scoresAll[1], scoresAll[2], scoresAll[3],scoresAll[4], scoresAll[5], scoresAll[6], scoresAll[7], scoresAll[8],scoresAll[9], scoresAll[10], scoresAll[11], scoresAll[12], scoresAll[13], scoresAll[14], scoresAll[15], scoresAll[16], scoresAll[17]))
        # Commit the insert to the database
        conn.commit()

        # Chage the reference to receive the golfer dictionary.


def calculateTotal():

    return


def calculateAll(golfer):

    golferID = golfer #['golferID']
    
    cursor.execute("""
       SELECT * FROM Rounds
       WHERE golferID = %s 
       ORDER by roundDate ASC
       """, (golferID, ))

    allGolferRounds = cursor.fetchall()

    for dictionary in allGolferRounds:
    # 'dictionary' is a variable representing the current dictionary in the loop
        courseRating, courseSlope, coursePar = lookUpCorse()
        roundTotal = (dictionary['hole1'] + dictionary['hole2'] + dictionary['hole3'] + dictionary['hole4'] + dictionary['hole5'] + dictionary['hole6'] + dictionary['hole7'] + dictionary['hole8'] + dictionary['hole9'])
        # Right now it is only set to calculate on the first 9 holes beacuse most of the10-18 holes are null
        scoreDiffer = calculations.scoreDiffer(roundTotal, 9, courseRating, courseSlope)
        
        proceeding20Scores, lowestProceedingHandicap = findPreviasScoreDetails(golferID, dictionary['roundDate'])

        handicapIndex = calculations.handicap(scoreDiffer, proceeding20Scores, lowestProceedingHandicap)

      
        cursor.execute("""
            UPDATE Rounds
            SET runningHandicap = %s,
                scoreDiffer = %s
            WHERE roundID = %s
            """, (handicapIndex, scoreDiffer, dictionary['roundID']))
        conn.commit()

        print("roundDate = ", dictionary['roundDate'],", scoreDiffer = ", scoreDiffer, ", handicapIndex = ", handicapIndex)
    return

#def printGolferReports():
    ## golferRank =  Add functionality to determine and assign each golfer a rank                             FIX ME!!!


def CloseCurser():
    conn.close()
