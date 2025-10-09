## This is The start of somthing new 
import mysql.connector
conn = mysql.connector.connect(
    host= "localhost",
    username = "root",
    password = "BakuraCofh123",
    database = "golf"
)

    ## ssl_ca = "path-to-ssl-certificate"  # often optional for simple setups

cursor = conn.cursor()
print("Hello and welcome to polo Park East Men's Club Handicap Calculator")
continu = "yes"

while continu == "Yes" or continu == "yes":
    G_rank = input("\nPleas enter first rank.  ")
    l_Name = input("\nPleas enter last name.  ")
    f_Name = input("\nPleas enter first name.  ")
    handicap = input("\nPleas enter handicap. ")
    roundsPlayed = input("\nPleas enter The number of rounds you have played. ")
    roundAvg = input("\nPleas enter Your Round Avereg. ")
    seasonTotal = input("\nPleas enter Your season total. ")
    farwell = "\nThank You " + f_Name + " " + l_Name + " for entering in your handicap of " + handicap + ".\n"
    print(farwell)
    
    cursor.execute("INSERT INTO Golfer(G_rank, F_Name, L_Name, Handycap, R_Played, R_Avg, SeasonTotal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
               (G_rank, f_Name, l_Name, handicap, roundsPlayed, roundAvg, seasonTotal))
    conn.commit()

    continu = input("do you wish to enter more handicaps?")

print("Thank you for stoping by!")
