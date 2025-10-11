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
    

    cursor.execute("INSERT INTO Golfer(G_rank, F_Name, L_Name, Handycap, R_Played, R_Avg, SeasonTotal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
               (G_rank, f_Name, l_Name, handicap, roundsPlayed, roundAvg, seasonTotal))

    conn.commit()
    farwell = "\nThank You " + f_Name + " " + l_Name + " for entering in your handicap of " + handicap + ".\n"
    print(farwell)
    continu = input("do you wish to enter more handicaps?")

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