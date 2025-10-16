import mysql.connector
import re
from datetime import datetime

conn = mysql.connector.connect(
    host = "rebeccaastclair.helioho.st",
    username = "rebeccastclair_golf",
    password = "BakuraCofh123",
    database = "rebeccastclair_handicap_calculator"
    ## ssl_ca = "path-to-ssl-certificate"  # often optional for simple setups
)
cursor = conn.cursor(dictionary=True)



def addNewGolfer():
    lastName = input("\nPleas enter last name.  ")
    firstName = input("\nPleas enter first name.  ")
    handicap = input("\nPleas enter handicap. ")
    roundsPlayed = input("\nPleas enter The number of rounds you have played. ")
    roundAvg = input("\nPleas enter Your Round Avereg. ")
    seasonTotal = input("\nPleas enter Your season total. ")
    ## cursor.execute("SELECT * FROM Golfers WHERE F_Name = %s AND L_Name = %s", (firstName, lastName))
    
    # Inset a new golfer into the database
    cursor.execute("INSERT INTO Golfer(firstName, lastName, handycap, roundsPlayed, roundAvg, seasonTotal) VALUES (%s, %s, %s, %s, %s, %s)",
               (firstName, lastName, handicap, roundsPlayed, roundAvg, seasonTotal))
    # Comit the insert to the database
    conn.commit()
    conn.close()

    farwell = "\nThank You " + firstName + " " + lastName + " for entering in your handicap of " + handicap + ".\n"
    print(farwell)




def addNewScore():
    total = 0  #Inisheat befoer referince
    holeNumber = 0

    corsePar = 29 # Hardcoded corse information till corse look up function Implumented                       FIX ME !!!
    corseRating = 58.2 #                                                                                              FIX ME !!!
    corseSlop = 97 #                                                                                                  FIX ME !!!

    #Enter Golfers name so they can get credit for the scores 
    firstName = input("Enter the players First name: ")
    lastName = input("enter the Players last name: ")
        
    #look up the golfer and the feilds that will be needed latter
    cursor.execute("""
        SELECT golferID,
               handycap,
               roundsPlayed,
               roundAvg,
               seasonTotal
        FROM Golfer g
        WHERE g.firstName = %s AND g.lastName = %s
        """, (firstName,lastName))
    
    #Creatingn the golfer item that holds the 5 variables with labes to their collum
    golfer = cursor.fetchone()
    
    if not golfer:
        conn.close()
        return None  # or raise ValueError("Golfer not found")

    # gets the golfer ID from the golfer item
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


    #Prompt wether its 9 or 18 holes then inishalize the array to the corect langth
    while holeNumber != 9 and holeNumber != 18:
        holeNumber = int(input("\nWas this 9 or 18 holes? "))
    
    scoresAll = [0]* holeNumber    
    
    # Run through each elument in the aray, prompt for the players score and add to a running total
    for i in range(holeNumber):
        scoresAll[i] = int(input("\nPlease enter the score for hole " + str(i + 1) + ". "))
        total = total + scoresAll[i]
        

    # Golfer contails 5 items (golferID, handycap, roundsPlayed, roundAvg, seasonTotal)   

    roundsPlayed = golfer['roundsPlayed'] + 1
    seasonTotal = golfer['seasonTotal'] + (total - corsePar) #Find out if the running totle is the Score Differenchal                                                   
    roundAvg = round((seasonTotal / roundsPlayed),2)



    ## calculateHandicap(): Calculate and update Handicap and Running Handicap                              FIX ME!!!

    handycap = 10 # Hard codding till calculation function implumented                                      FIX ME!!!
    runningHandicap = handycap



    # Update the Golfer Deta   
    cursor.execute("""
    UPDATE Golfer
    SET handycap = %s,
        roundsPlayed = %s,
         roundAvg = %s,
         seasonTotal = %s
    WHERE golferID = %s
    """, (handycap, roundsPlayed, roundAvg, seasonTotal, golferID))
    

    #Calculations Score Differenchal AND Insert new round into score table
    if holeNumber == 9:        
        # Calculate Score Differenchal
        scoreDiffer = round(((total * 2) - corseRating) * (113 / corseSlop), 2) 

        # Inset a new score set into the database
        cursor.execute("INSERT INTO Scores(golferID, playedOn, holes, total, scoreDiffer, runningHandicap, hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8, hole9) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (golferID, playedOn, 9, total, scoreDiffer, runningHandicap, scoresAll[0], scoresAll[1], scoresAll[2], scoresAll[3],scoresAll[4], scoresAll[5], scoresAll[6], scoresAll[7], scoresAll[8]))
        # Comit the insert to the database
        conn.commit()
        conn.close()
    else:
         # Calculate Score Differenchal         
        scoreDiffer = round((total - corseRating) * (113 / corseSlop), 2)    
        
        # Inset a new score set into the database
        cursor.execute("INSERT INTO Scores(( golferID, playedOn, holes, total, scoreDiffer, runningHandicap, hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8, hole9, hole10, hole11, hole12, hole13, Hole_14, Hole_15, hole16, hole17, hole18) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (golferID, playedOn, 18, total, scoreDiffer, runningHandicap, scoresAll[0], scoresAll[1], scoresAll[2], scoresAll[3],scoresAll[4], scoresAll[5], scoresAll[6], scoresAll[7], scoresAll[8],scoresAll[9], scoresAll[10], scoresAll[11], scoresAll[12], scoresAll[13], scoresAll[14], scoresAll[15], scoresAll[16], scoresAll[17]))
        # Comit the insert to the database
        conn.commit()
        conn.close()




#def printGolferReports():
    ## golferRank =  Add functionality to determin and assighn each golfer a rank                             FIX ME!!!


#def calculateHandicap():
    #handicap = calculate and update a players handicap                                                       FIX ME!!!
    ##  Rules for Calculataions
    #   Score Differentials
    #       Adjusted Gross Score: 
    #           gross score, 
    #           apply adjustments like net double bogey on holes you didn't complete
    #           apply any penalty strokes.
    #       Score Differential Formula:
    #           (Adjusted Gross Score - Course Rating - Playing Conditions Adjustment) x (113 / Slope Rating).
    #   Handicap index
    #       When a score is posted it is converted into a score diferenchal that acounts for the dificolty of the stores and the tees played. 
    #       Averege of the 8 best scores out of 20 rounds
    #       mesehrs demenstrated abuility on their better days
    #       Once a players index has incresed by 3 strokes the rate of increse slowes by 50%
    #       Can not increas more then 5 in one year
    #       if you post a scor with a score diferentchal of 7 - 9.9 strokes better then handicap index handicap is redused by an aditional stroke
    #       If 10 or better hadicap is redused by 2