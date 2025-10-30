import re
import difflib
from tkinter import YES

from datetime import datetime, date, time


def calculateHandicap(golferID, newScoreDiffer):
     provitional = False
     minimumRounds = 8  # Hardcoded handicap information till look up function Implemented                        FIX ME !!!
     curentSoftCap = 3 #                                                                                          FIX ME !!!
     softCapSlow = .5 #                                                                                           FIX ME !!!
     curentHardCap = 5 #                                                                                          FIX ME !!!
     handicapDrop = 7 #                                                                                           FIX ME !!!
     aditionalHandicapDrop = 9.9 #                                                                                FIX ME !!!

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

     if len(recent20Scores) < minimumRounds:
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
     softCap = LowestHandicap + curentSoftCap                                                                       # FIX ME!!!! (Problem Below)
     hardCap = LowestHandicap + curentHardCap                                                                       # FIX ME!!!! (Problem Below)
     #If the player has no preveas handicap data gives an errorCheck why"unsupported operand type(s) for +: 'NoneType' and 'int'"


     # Check if the new handicap goes over the soft or hard cap and set handicap index
     if TepHandicap > softCap:
          aboveSoftCap = round(((TepHandicap - softCap)*softCapSlow),2)
          handicapIndex = softCap + aboveSoftCap
          if handicapIndex > hardCap:
                handicapIndex = hardCap
     elif newScoreDiffer < (TepHandicap - handicapDrop):
         if newScoreDiffer < (TepHandicap - aditionalHandicapDrop):
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



def addNewScore(curentRound):
    corsePar = 29 # Hardcoded course information till course look up function Implemented                       FIX ME !!!
    corseRating = 58.2 #                                                                                      FIX ME !!!
    corseSlop = 97 #                                                                                          FIX ME !!!
  
    # If Date is not entered this will use the current date.
    if not curentRound.roundDate:
        curentRound.roundDate = datetime.today().date()

    # If Time is not entered this will use the curent time.
    if curentRound.roundTime:
        curentRound.roundTime = datetime.now().time()

        if curentRound.holeCount == 9:
            total = curentRound.hole1 + curentRound.hole2 + curentRound.hole3 + curentRound.hole4 + curentRound.hole5 + curentRound.hole6 + curentRound.hole7 + curentRound.hole8 + curentRound.hole9
        else:
            total = curentRound.hole1 + curentRound.hole2 + curentRound.hole3 + curentRound.hole4 + curentRound.hole5 + curentRound.hole6 + curentRound.hole7 + curentRound.hole8 + curentRound.hole9 + curentRound.hole10 + curentRound.hole11 + curentRound.hole12 + curentRound.hole13 + curentRound.hole14 + curentRound.hole15 + curentRound.hole16 + curentRound.hole17 + curentRound.hole18
        

    # 5 golfer items inside curentRound (golferID, handycap, roundsPlayed, roundAvg, seasonTotal)   

    roundsPlayed = curentRound['roundsPlayed'] + 1
    seasonTotal = curentRound['seasonTotal'] + (total - corsePar)                                                    
    roundAvg = round((seasonTotal / roundsPlayed),2)

    if curentRound.holeCount == 9:
        # Calculate Score Differential
        scoreDiffer = round(((total * 2) - corseRating) * (113 / corseSlop), 2) 
    else:        
        # Calculate Score Differential         
        scoreDiffer = round((total - corseRating) * (113 / corseSlop), 2)    

    #Takes the Golfer ID and Score differentially and calculates the golfer's handicap index
    handicapIndex, provitional = calculateHandicap(curentRound.golferID, scoreDiffer) 
        
    # Update the Golfer Deta   
    cursor.execute("""
    UPDATE Golfer
    SET handycap = %s,
        roundsPlayed = %s,
         roundAvg = %s,
         seasonTotal = %s,
         provitional = %s
    WHERE golferID = %s
    """, (handicapIndex, roundsPlayed, roundAvg, seasonTotal,provitional, curentRound.golferID))
    conn.commit()
    

    #Insert new round into score table
    if curentRound.holeCount == 9:        
        # Inset a new score set into the database
        cursor.execute("INSERT INTO Scores(golferID, roundDate, roundTime, holes, total, scoreDiffer, runningHandicap, hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8, hole9) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (curentRound.golferID, curentRound.roundDate, curentRound.roundTime, 9, total, scoreDiffer, handicapIndex, curentRound.hole1, curentRound.hole2, curentRound.hole3, curentRound.hole4, curentRound.hole5, curentRound.hole6, curentRound.hole7, curentRound.hole8, curentRound.hole9))
        # Commit the insert to the database
        conn.commit()
    else:        
        # Inset a new score set into the database
        cursor.execute("INSERT INTO Scores(( golferID, roundDate, roundTime, holes, total, scoreDiffer, runningHandicap, hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8, hole9, hole10, hole11, hole12, hole13, Hole_14, Hole_15, hole16, hole17, hole18) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (curentRound.golferID, curentRound.roundDate, curentRound.roundTime, 18, total, scoreDiffer, handicapIndex, curentRound.hole1, curentRound.hole2, curentRound.hole3, curentRound.hole4, curentRound.hole5, curentRound.hole6, curentRound.hole7, curentRound.hole8, curentRound.hole9, curentRound.hole10, curentRound.hole11, curentRound.hole12, curentRound.hole13, curentRound.hole14, curentRound.hole15, curentRound.hole16, curentRound.hole17, curentRound.hole18))
        # Commit the insert to the database
        conn.commit()