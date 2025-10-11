import mysql.connector
conn = mysql.connector.connect(
    host = "rebeccaastclair.helioho.st",
    username = "rebeccastclair_golf",
    password = "BakuraCofh123",
    database = "rebeccastclair_handicap_calculator"
    ## ssl_ca = "path-to-ssl-certificate"  # often optional for simple setups
)
cursor = conn.cursor()

def add_new_golfer():
    G_rank = input("\nPleas enter first rank.  ")
    l_Name = input("\nPleas enter last name.  ")
    f_Name = input("\nPleas enter first name.  ")
    handicap = input("\nPleas enter handicap. ")
    roundsPlayed = input("\nPleas enter The number of rounds you have played. ")
    roundAvg = input("\nPleas enter Your Round Avereg. ")
    seasonTotal = input("\nPleas enter Your season total. ")
    ## cursor.execute("SELECT * FROM Golfers WHERE F_Name = %s AND L_Name = %s", (f_Name, l_Name))
    
    # Inset a new golfer into the database
    cursor.execute("INSERT INTO Golfer(G_rank, F_Name, L_Name, Handycap, R_Played, R_Avg, SeasonTotal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
               (G_rank, f_Name, l_Name, handicap, roundsPlayed, roundAvg, seasonTotal))
    # Comit the insert to the database
    conn.commit()

    farwell = "\nThank You " + f_Name + " " + l_Name + " for entering in your handicap of " + handicap + ".\n"
    print(farwell)
    continu = input("do you wish to enter more handicaps?")

def Add_New_Score():
    total = 0  #Inisheat befoer referince
    H_number = 0

    # Find out Basick information like which Player, Date and Time.
    Golfer_ID = 1    ## Golfer ID hard set to 1, Add ID serch latter                                         FIX ME!!!
    date = input("\nWhat was the day for this round? ")
    time = input("\nWhat was the start time for this round? ")

    #Prompt wether its 9 or 18 holes then inishalize the array to the corect langth
    while H_number != 9 and H_number != 18:
        H_number = int(input("\nWas this 9 or 18 holes? "))
    
    scoresAll = [0]* H_number  
    
    # Run through each elument in the aray, prompt for the players score and add to a running total
    for i in range(H_number):
            scoresAll[i] = int(input("\nPlease enter the score for hole " + str(i + 1) + ". "))
            total = total + scoresAll[i]
    
    #Score Differenchal calculations diferent for 9 & 18 holes and each goes inton a diferent table. 
    if H_number == 9:
        # Calculate Score Differenchal         Hard codding corse information, Add Corse serch latter         FIX ME!!!
        Score_Differ = round(((total * 2) - 58.2) * (113 / 97), 2) 
        
        # Inset a new score set into the database
        cursor.execute("INSERT INTO scores(Holes,Golfer_ID, Date, Sart_Time, Hole_1, Hole_2, Hole_3, Hole_4, Hole_5, Hole_6, Hole_7, Hole_8, Hole_9, total, Score_Differ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (9, Golfer_ID, date, time, scoresAll[0], scoresAll[1], scoresAll[2], scoresAll[3],scoresAll[4], scoresAll[5], scoresAll[6], scoresAll[7], scoresAll[8], total, Score_Differ))
        # Comit the insert to the database
        conn.commit()
    else:
        # Calculate Score Differenchal         Hard codding corse information, Add Corse serch latter         FIX ME!!!
        Score_Differ = round((total - 58.2) * (113 / 97), 2)

        # Inset a new score set into the database
        cursor.execute("INSERT INTO scores(Holes,Golfer_ID, Date, Sart_Time, Hole_1, Hole_2, Hole_3, Hole_4, Hole_5, Hole_6, Hole_7, Hole_8, Hole_9, Hole_10, Hole_11, Hole_12, Hole_13, Hole_14, Hole_15, Hole_16, Hole_17, Hole_18,  total, Score_Differ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (18, Golfer_ID, date, time, scoresAll[0], scoresAll[1], scoresAll[2], scoresAll[3],scoresAll[4], scoresAll[5], scoresAll[6], scoresAll[7], scoresAll[8],scoresAll[9], scoresAll[10], scoresAll[11], scoresAll[12], scoresAll[13], scoresAll[14], scoresAll[15], scoresAll[16], scoresAll[17], total, Score_Differ))
        # Comit the insert to the database
        conn.commit()







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