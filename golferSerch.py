import difflib
import mysql.connector
from errorHandler import handleDbError

def sqlConector():
    try:
        conn = mysql.connector.connect(
            host="rebeccaastclair.helioho.st",
            user="rebeccastclair_golf",
            password="BakuraCofh123",
            database="rebeccastclair_handicap_calculator",
            autocommit=True,
        )
        return conn
    except Exception as e:
        return handleDbError(e)

def dedupe(rows, key_name='golferID'):
    seen, out = set(), []
    for r in rows or []:
        key = r.get(key_name)
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out

def lookUpGolfer(firstName, lastName):
    # ---------- Tier 1: Exact ----------
    conn = sqlConector()
    if isinstance(conn, dict) and "error" in conn:
        return conn

    try:
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(
                """
                SELECT *
                FROM Golfer g
                WHERE g.firstName = %s AND g.lastName = %s
                """,
                (firstName, lastName)
            )
            golfer = cursor.fetchone()
            if golfer is not None:
                # Exact match -> results = 1
                return {"results": 1, "golfer": golfer}
    except Exception as e:
        return handleDbError(e)
    finally:
        if conn and not isinstance(conn, dict) and conn.is_connected():
            conn.close()

    # ---------- Tier 2: Close (first-only, last-only, fuzzy) ----------
    closeCandidates = []
    conn = sqlConector()
    if isinstance(conn, dict) and "error" in conn:
        return conn

    try:
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            # First-only matches
            cursor.execute(
                """
                SELECT *
                FROM Golfer g
                WHERE g.firstName = %s
                """,
                (firstName,)
            )
            closeCandidates += cursor.fetchall()

            # Last-only matches
            cursor.execute(
                """
                SELECT *
                FROM Golfer g
                WHERE g.lastName = %s
                """,
                (lastName,)
            )
            closeCandidates += cursor.fetchall()

            # Fuzzy lastName suggestions (only if nothing found yet, optional)
            if not closeCandidates and lastName:
                cursor.execute("SELECT lastName FROM Golfer")
                allLastNames = [row['lastName'] for row in cursor.fetchall()]
                close = difflib.get_close_matches(lastName, allLastNames, n=5, cutoff=0.72)
                if close:
                    qmarks = ",".join(["%s"] * len(close))
                    # f-string REQUIRED here to inject placeholders count
                    cursor.execute(f"""
                        SELECT *
                        FROM Golfer
                        WHERE lastName IN ({qmarks})
                        ORDER BY lastName, firstName
                    """, tuple(close))
                    closeCandidates += cursor.fetchall()

            # Fuzzy firstName suggestions (only if still empty, optional)
            if not closeCandidates and firstName:
                cursor.execute("SELECT firstName FROM Golfer")
                allFirstNames = [row['firstName'] for row in cursor.fetchall()]
                close = difflib.get_close_matches(firstName, allFirstNames, n=5, cutoff=0.72)
                if close:
                    qmarks = ",".join(["%s"] * len(close))
                    cursor.execute(f"""
                        SELECT *
                        FROM Golfer
                        WHERE firstName IN ({qmarks})
                        ORDER BY lastName, firstName
                    """, tuple(close))
                    closeCandidates += cursor.fetchall()

            closeCandidates = dedupe(closeCandidates, key_name='golferID')  # adjust key if needed

            if closeCandidates:
                # Any non-exact match -> results = 2
                return {"results": 2, "candidates": closeCandidates}

            # Nothing found anywhere -> results = 3
            return {"results": 3, "message": "No matching golfer found."}

    except Exception as e:
        return handleDbError(e)
    finally:
        if conn and not isinstance(conn, dict) and conn.is_connected():
            conn.close()
