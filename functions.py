import re
import difflib
from tkinter import YES
import mysql.connector
conn = mysql.connector.connect(
    host = "rebeccaastclair.helioho.st",
    username = "rebeccastclair_golf",
    password = "BakuraCofh123",
    database = "rebeccastclair_handicap_calculator"
    ## ssl_ca = "path-to-ssl-certificate"  # often optional for simple setups
)
cursor = conn.cursor(dictionary=True)
from datetime import datetime, date, time

def dedupe(rows):
    seen, out = set(), []
    for r in rows:
        if r['golferID'] not in seen:
            seen.add(r['golferID'])
            out.append(r)
    return out

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

    while golfer == None:
        #Variables set for repeating if names are entered with invaled symbols
        repetFirst = True
        repetLast = True

        #Enter Golfers First name and check if there are any invaled symbols 
        while repetFirst == True:
            firstName = input("Enter the player's first name: ").strip().title()
            if not re.match(name_pattern, firstName):
                print("Invalid first name. Please use only letters, spaces, or periods.")
            else:
                repetFirst = False

        #Enter Golfers Last name and check if there are any invaled symbols 
        while repetLast == True:
            lastName = input("enter the Players last name: ").strip().title()
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
                print("\n1: Try serching a new serch? \n2: Add a new golfer \n3: Exit")
                chose = input()
                if chose == '2':
                    addNewGolfer()
                    return
                elif chose == '3':
                    return
    if option == 1:

        print(f"Handycap: {golfer['handycap']} | Number of Rounds Played: {golfer['roundsPlayed']} | Round Averege: {golfer['roundAvg']} | Season Total: {golfer['seasonTotal']}")
        print("No need to add them")
        return
    if option == 2:
        print("\nThis option has not been implemented")
        return
    if option == 3:
        addNewScore(golfer)
        return



def addNewGolfer(firstName, lastName):
    #The user is sent to the lookUpGolfer function first, and if the golfer is not found, they are sent here to enter the remaining data
    handicap = input("\nPlease enter handicap. ")
    roundsPlayed = input("\nPlease enter The number of rounds you have played. ")
    roundAvg = input("\nPlease enter Your Round Averege. ")
    seasonTotal = input("\nPlease enter Your season total. ")
    
    # Inset a new golfer into the database
    cursor.execute("INSERT INTO Golfer(firstName, lastName, handycap, roundsPlayed, roundAvg, seasonTotal) VALUES (%s, %s, %s, %s, %s, %s)",
               (firstName, lastName, handicap, roundsPlayed, roundAvg, seasonTotal))
    # Commit the insert to the database
    conn.commit()



def calculateHandicap(golferID, newScoreDiffer):
     provitional = False
     #Pool the most recent 19 scores from the database, the new score makes 20
     cursor.execute("""
        SELECT scoreDiffer
        FROM Scores
        WHERE golferID = %s 
            AND scoreDiffer IS NOT NULL
        ORDER by playedOn DESC LIMIT 19
        """, (golferID,))
     
     # Put those 19 Dictionary items into a Variable then change the dictionary to an Array
     rows = cursor.fetchall()  
     recent20Scores = [row['scoreDiffer'] for row in rows]
     recent20Scores.append(newScoreDiffer)

     if len(recent20Scores) < 20:
         provitional = True
     
     #Sort the aray then take only the best 8, avrage them out, and put that in a new variable. 
     recent20Scores.sort()
     Best8Set = recent20Scores[:8]
     
     if Best8Set:        
         AvregeOf8 = sum(Best8Set)/ len(Best8Set)
         TepHandicap = round(AvregeOf8 * 0.96, 2)
     else:
         TepHandicap = 0

     # Poll the handicaps conected to each round for the last 365 days and store the lowest Value in a variable
     cursor.execute("""
        SELECT MIN(runningHandicap) AS lowHI
        FROM Scores
        WHERE golferID = %s AND playedOn >= (CURDATE() - INTERVAL 365 DAY)
        ORDER by playedOn DESC
        """, (golferID,))
     HandicapPast365 = cursor.fetchone()
     # Convert from a dictionary to a single variable
     LowestHandicap = HandicapPast365['lowHI']

     # Calculate the soft and hard cap
     softCap = LowestHandicap + 3
     hardCap = LowestHandicap + 5

     # Check if the new handicap goes over the soft or hard cap and set handicap index
     if TepHandicap > softCap:
          aboveSoftCap = round(((TepHandicap - softCap)*.5),2)
          handicapIndex = softCap + aboveSoftCap
          if handicapIndex > hardCap:
                handicapIndex = hardCap
     elif newScoreDiffer < (TepHandicap - 7):
         if newScoreDiffer < (TepHandicap - 9.9):
            handicapIndex = TepHandicap - 2
         else:
             handicapIndex = TepHandicap - 1
     else:
         handicapIndex = TepHandicap     
     
        # Return the results of the handicap calculations 
     return handicapIndex, provitional

    #   Handicap index calculation rules
    #       When a score is posted, it is converted into a score differential that accounts for the difficulty of the course and the tees played. 
    #       Average of the 8 best scores out of 20 rounds
    #       Measures the demonstrated ability on their better days
    #       Once a player's index has increased by 3 strokes, the rate of increase slows by 50%
    #       Can not increase more than 5 in one year
    #       if you post a score with a score differential of 7 - 9.9 strokes better, the handicap index handicap is reduced by an additional stroke
    #       If it is 10 or better, the handicap is reduced by 2



def addNewScore(golfer):
    #Initiate before reference
    total = 0  
    holeNumber = 0
    
    corsePar = 29 # Hardcoded course information till course look up function Implemented                       FIX ME !!!
    corseRating = 58.2 #                                                                                      FIX ME !!!
    corseSlop = 97 #                                                                                          FIX ME !!!
  
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
    playedOn = datetime.combine(datePlayed, startTime)


    #Prompt whether its 9 or 18 holes then initialize the array to the corect langth
    while holeNumber != 9 and holeNumber != 18:
        holeNumber = int(input("\nWas this 9 or 18 holes? "))
    
    scoresAll = [0]* holeNumber    
    
    # Run through each element in the aray, prompt for the player's score and add to a running total
    for i in range(holeNumber):
        scoresAll[i] = int(input("\nPlease enter the score for hole " + str(i + 1) + ". "))
        total = total + scoresAll[i]        

    # Golfer contails 5 items (golferID, handycap, roundsPlayed, roundAvg, seasonTotal)   

    roundsPlayed = golfer['roundsPlayed'] + 1
    seasonTotal = golfer['seasonTotal'] + (total - corsePar)                                                    
    roundAvg = round((seasonTotal / roundsPlayed),2)

    if holeNumber == 9:
        # Calculate Score Differential
        scoreDiffer = round(((total * 2) - corseRating) * (113 / corseSlop), 2) 
    else:        
        # Calculate Score Differential         
        scoreDiffer = round((total - corseRating) * (113 / corseSlop), 2)    

    #Takes the Golfer ID and Score differentially and calculates the golfer's handicap index
    handicapIndex, provitional = calculateHandicap(golferID, scoreDiffer) 
        
    # Update the Golfer Deta   
    cursor.execute("""
    UPDATE Golfer
    SET handycap = %s,
        roundsPlayed = %s,
         roundAvg = %s,
         seasonTotal = %s,
         provitional = %s
    WHERE golferID = %s
    """, (handicapIndex, roundsPlayed, roundAvg, seasonTotal,provitional, golferID))
    conn.commit()
    

    #Insert new round into score table
    if holeNumber == 9:        
        # Inset a new score set into the database
        cursor.execute("INSERT INTO Scores(golferID, playedOn, holes, total, scoreDiffer, runningHandicap, hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8, hole9) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (golferID, playedOn, 9, total, scoreDiffer, handicapIndex, scoresAll[0], scoresAll[1], scoresAll[2], scoresAll[3],scoresAll[4], scoresAll[5], scoresAll[6], scoresAll[7], scoresAll[8]))
        # Commit the insert to the database
        conn.commit()
    else:        
        # Inset a new score set into the database
        cursor.execute("INSERT INTO Scores(( golferID, playedOn, holes, total, scoreDiffer, runningHandicap, hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8, hole9, hole10, hole11, hole12, hole13, Hole_14, Hole_15, hole16, hole17, hole18) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (golferID, playedOn, 18, total, scoreDiffer, handicapIndex, scoresAll[0], scoresAll[1], scoresAll[2], scoresAll[3],scoresAll[4], scoresAll[5], scoresAll[6], scoresAll[7], scoresAll[8],scoresAll[9], scoresAll[10], scoresAll[11], scoresAll[12], scoresAll[13], scoresAll[14], scoresAll[15], scoresAll[16], scoresAll[17]))
        # Commit the insert to the database
        conn.commit()

#def printGolferReports():
    ## golferRank =  Add functionality to determine and assign each golfer a rank                             FIX ME!!!


def CloseCurser():
    conn.close()
