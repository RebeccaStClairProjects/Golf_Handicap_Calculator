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

        suggestions = []


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
                suggestions += cursor.fetchall()
                

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
                suggestions += cursor.fetchall()
                
        combined = dedupe((firstMatches or []) + (lastMatches or []) + (suggestions or []))

        if combined:  # non-empty list → truthy
            return {"results": 2, "candidates": combined}

    return {"results": 3,}
