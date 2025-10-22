import re
import difflib
import functions

import mysql.connector
conn = mysql.connector.connect(
    host = "rebeccaastclair.helioho.st",
    username = "rebeccastclair_golf",
    password = "BakuraCofh123",
    database = "rebeccastclair_handicap_calculator"
    ## ssl_ca = "path-to-ssl-certificate"  # often optional for simple setups
)
cursor = conn.cursor(dictionary=True)

from tkinter import YES


def dedupe(rows):
    seen, out = set(), []
    for r in rows:
        if r['golferID'] not in seen:
            seen.add(r['golferID'])
            out.append(r)
    return out

def lookUpGolfer(firstName, lastName):

    #look up the golfer and the fields that will be needed later
    cursor.execute("""
            SELECT golferID, firstName, lastName
            FROM Golfer g
            WHERE g.firstName = %s AND g.lastName = %s
            """, (firstName,lastName))
    
    #Creating the golfer item that holds the 5 variables with labels to their column
    golfer = cursor.fetchone()

    if golfer:
        golfer["results"] = 1
        return golfer

    if not golfer:
        #Check if the First name is found
        cursor.execute("""
                SELECT firstName, lastName, golferID
                FROM Golfer g
                WHERE g.firstName = %s
            """, (firstName,))
        firstMatches = cursor.fetchall()
                       
        #Check if the Last name is found
        cursor.execute("""
            SELECT firstName, lastName, golferID
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
                        SELECT firstName, lastName, golferID
                        FROM Golfer
                        WHERE lastName IN ({qmarks})
                        ORDER BY lastName, firstName
                    """, tuple(close))
                suggestionLast = cursor.fetchall()
                suggestion = suggestion | suggestionLast

        if not firstMatches and not lastMatches and firstName:
            cursor.execute("SELECT firstName FROM Golfer")
            allFisrtNames = [row['firstName'] for row in cursor.fetchall()]
            close = difflib.get_close_matches(firstName, allFisrtNames, n=5, cutoff=0.72)
            if close:
                qmarks = ",".join(["%s"] * len(close))
                cursor.execute(f"""
                        SELECT firstName, lastName, golferID
                        FROM Golfer
                        WHERE firstName IN ({qmarks})
                        ORDER BY lastName, firstName
                    """, tuple(close))
                suggestionFirst = cursor.fetchall()
                suggestion =  suggestion | suggestionFirst

        if suggestion:
            candidates = dedupe(firstMatches + lastMatches + suggestion)
            golfer = {"results": 2, "candidates": candidates}
        else:
            candidates = dedupe(firstMatches + lastMatches)
            golfer = {"results": 2, "candidates": candidates}

    if golfer == None:
        golfer["results"] = 3

    return golfer




def tempParching(option, firstName, lastName):                
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
                            functions.addNewGolfer(firstName,lastName)
                            return
                        if option == 2 or option == 3:
                            print("Since a match could not be found do you want to add the golfer")
                            selection = input ("enter Yes or No")
                            if selection.strip().lower() == "yes":
                                functions.addNewGolfer(firstName,lastName)
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
                functions.addNewGolfer()
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
        functions.addNewScore(golfer)
        return



