import mysql.connector
conn = mysql.connector.connect(
    host = "rebeccaastclair.helioho.st",
    username = "rebeccastclair_golf",
    password = "BakuraCofh123",
    database = "rebeccastclair_handicap_calculator"
    ## ssl_ca = "path-to-ssl-certificate"  # often optional for simple setups
)
cursor = conn.cursor()



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

    farwell = "\nThank You " + firstName + " " + lastName + " for entering in your handicap of " + handicap + ".\n"
    print(farwell)




def addNewScore():
    total = 0  #Inisheat befoer referince
    holeNumber = 0

    # Find out Basick information like which Player, Date and Time.
    golferID = 1    ## Golfer ID hard set to 1, Add ID serch latter                                         FIX ME!!!
    
    date = input("\nWhat was the day for this round? ")
    time = input("\nWhat was the start time for this round? ")

    #Prompt wether its 9 or 18 holes then inishalize the array to the corect langth
    while holeNumber != 9 and holeNumber != 18:
        holeNumber = int(input("\nWas this 9 or 18 holes? "))
    
    scoresAll = [0]* holeNumber  
    
    # Run through each elument in the aray, prompt for the players score and add to a running total
    for i in range(holeNumber):
        scoresAll[i] = int(input("\nPlease enter the score for hole " + str(i + 1) + ". "))
        total = total + scoresAll[i]
         

    ## roundsPlayed = Serch for the player and incrument number of rounds played                            FIX ME!!!
    ## roundAvg = Calculate and update golfers avrege                                                       FIX ME!!!
    ## seasonTotal = Calculate and update golfers season totle                                              FIX ME!!!

    #Score Differenchal calculations diferent for 9 & 18 holes and each goes inton a diferent table. 
    if holeNumber == 9:
        # Calculate Score Differenchal         Hard codding corse information, Add Corse serch latter       FIX ME!!!
        scoreDiffer = round(((total * 2) - 58.2) * (113 / 97), 2) 
        
        # Inset a new score set into the database
        cursor.execute("INSERT INTO Scores(holes, golferID, date, sartTime, hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8, hole9, total, scoreDiffer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (9, golferID, date, time, scoresAll[0], scoresAll[1], scoresAll[2], scoresAll[3],scoresAll[4], scoresAll[5], scoresAll[6], scoresAll[7], scoresAll[8], total, scoreDiffer))
        # Comit the insert to the database
        conn.commit()
    else:
        # Calculate Score Differenchal         Hard codding corse information, Add Corse serch latter         FIX ME!!!
        Score_Differ = round((total - 58.2) * (113 / 97), 2)

        # Inset a new score set into the database
        cursor.execute("INSERT INTO Scores((holes, golferID, date, sartTime, hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8, hole9, hole10, hole11, hole12, hole13, Hole_14, Hole_15, hole16, hole17, hole18,  total, scoreDiffer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (18, golferID, date, time, scoresAll[0], scoresAll[1], scoresAll[2], scoresAll[3],scoresAll[4], scoresAll[5], scoresAll[6], scoresAll[7], scoresAll[8],scoresAll[9], scoresAll[10], scoresAll[11], scoresAll[12], scoresAll[13], scoresAll[14], scoresAll[15], scoresAll[16], scoresAll[17], total, scoreDiffer))
        # Comit the insert to the database
        conn.commit()




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