import mysql.connector
conn = mysql.connector.connect(
    host= "localhost",
    username = "root",
    password = "BakuraCofh123",
    database = "golf"
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