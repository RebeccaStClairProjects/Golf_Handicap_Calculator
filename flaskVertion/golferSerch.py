import difflib
from datetime import datetime, timedelta

import mysql.connector
from errorHandler import handleDbError


def _to_float(value, default=9999.0):
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


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


def _normalize_golfer_row(g):
    golfer_id = g.get("golferID", g.get("golferId"))
    first_name = g.get("firstName", "")
    last_name = g.get("lastName", "")
    handicap = g.get("handicap", g.get("handycap"))
    round_avg = g.get("roundAvg", g.get("roundAVG"))
    rounds_played = g.get("roundsPlayed", g.get("roundsplayed"))
    season_total = g.get("seasonTotal", g.get("seasontotal"))

    return {
        "golferID": golfer_id,
        "firstName": first_name,
        "lastName": last_name,
        "name": f"{first_name} {last_name}".strip(),
        "handicap": handicap if handicap is not None else "-",
        "roundAvg": round_avg if round_avg is not None else "-",
        "roundsPlayed": rounds_played if rounds_played is not None else "-",
        "seasonTotal": season_total if season_total is not None else "-",
    }


def _score_differ(total_score, hole_count, tee_rating, tee_slope):
    if hole_count == 9:
        return round(((total_score * 2) - tee_rating) * (113 / tee_slope), 2)
    return round((total_score - tee_rating) * (113 / tee_slope), 2)


def _calculate_handicap(score_differ, previous_differs, lowest_handicap):
    current_soft_cap = 3
    soft_cap_slow = 0.5
    current_hard_cap = 5
    handicap_drop = 7
    additional_handicap_drop = 9.9

    scores = list(previous_differs or [])
    scores.append(score_differ)

    provisional = len(scores) < 8
    scores.sort()
    best8 = scores[:8]
    if not best8:
        return 0.0, provisional

    average8 = sum(best8) / len(best8)
    temp_handicap = round(average8 * 0.96, 2)

    if lowest_handicap is None:
        lowest_handicap = temp_handicap

    soft_cap = lowest_handicap + current_soft_cap
    hard_cap = lowest_handicap + current_hard_cap

    if temp_handicap > soft_cap:
        above_soft = round((temp_handicap - soft_cap) * soft_cap_slow, 2)
        handicap_index = soft_cap + above_soft
        if handicap_index > hard_cap:
            handicap_index = hard_cap
    elif score_differ < (temp_handicap - handicap_drop):
        if score_differ < (temp_handicap - additional_handicap_drop):
            handicap_index = temp_handicap - 2
        else:
            handicap_index = temp_handicap - 1
    else:
        handicap_index = temp_handicap

    return round(handicap_index, 2), provisional


def lookUpGolfer(firstName, lastName):
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
                return {"results": 1, "golfer": golfer}
    except Exception as e:
        return handleDbError(e)
    finally:
        if conn and not isinstance(conn, dict) and conn.is_connected():
            conn.close()

    closeCandidates = []
    conn = sqlConector()
    if isinstance(conn, dict) and "error" in conn:
        return conn

    try:
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(
                """
                SELECT *
                FROM Golfer g
                WHERE g.firstName = %s
                """,
                (firstName,)
            )
            closeCandidates += cursor.fetchall()

            cursor.execute(
                """
                SELECT *
                FROM Golfer g
                WHERE g.lastName = %s
                """,
                (lastName,)
            )
            closeCandidates += cursor.fetchall()

            if not closeCandidates and lastName:
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
                    closeCandidates += cursor.fetchall()

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

            closeCandidates = dedupe(closeCandidates, key_name='golferID')

            if closeCandidates:
                return {"results": 2, "candidates": closeCandidates}

            return {"results": 3, "message": "No matching golfer found."}

    except Exception as e:
        return handleDbError(e)
    finally:
        if conn and not isinstance(conn, dict) and conn.is_connected():
            conn.close()


def getMemberHandicaps():
    conn = sqlConector()
    if isinstance(conn, dict) and "error" in conn:
        return conn

    try:
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute("SELECT * FROM Golfer")
            golfers = cursor.fetchall() or []

            normalized = [_normalize_golfer_row(g) for g in golfers]
            normalized.sort(key=lambda x: (_to_float(x["handicap"]), x["name"]))

            ranked = []
            for idx, golfer in enumerate(normalized, start=1):
                ranked.append({"rank": idx, **golfer})

            return {"results": 1, "golfers": ranked}
    except Exception as e:
        return handleDbError(e)
    finally:
        if conn and not isinstance(conn, dict) and conn.is_connected():
            conn.close()


def getGolferByID(golfer_id):
    conn = sqlConector()
    if isinstance(conn, dict) and "error" in conn:
        return conn

    try:
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(
                """
                SELECT *
                FROM Golfer
                WHERE golferID = %s
                """,
                (golfer_id,)
            )
            golfer = cursor.fetchone()

            if golfer is None:
                return {"results": 2, "message": "Golfer not found."}

            golfer_normalized = _normalize_golfer_row(golfer)

            cursor.execute("SELECT * FROM Golfer")
            all_golfers = cursor.fetchall() or []
            normalized_all = [_normalize_golfer_row(g) for g in all_golfers]
            normalized_all.sort(key=lambda x: (_to_float(x["handicap"]), x["name"]))

            rank_map = {}
            for idx, g in enumerate(normalized_all, start=1):
                rank_map[g["golferID"]] = idx

            summary = {
                "rank": rank_map.get(golfer_normalized["golferID"], "-"),
                "firstName": golfer_normalized["firstName"],
                "lastName": golfer_normalized["lastName"],
                "handicap": golfer_normalized["handicap"],
            }

            rounds = []
            try:
                cursor.execute(
                    """
                    SELECT roundDate, roundTime, total, scoreDiffer, runningHandicap
                    FROM Rounds
                    WHERE golferID = %s
                    ORDER BY roundDate DESC, roundTime DESC
                    """,
                    (golfer_id,)
                )
                rows = cursor.fetchall() or []
                rounds = [
                    {
                        "playedOn": f"{row.get('roundDate')} {row.get('roundTime')}",
                        "total": row.get("total", "-"),
                        "scoreDiffer": row.get("scoreDiffer", "-"),
                        "runningHandicap": row.get("runningHandicap", "-"),
                    }
                    for row in rows
                ]
            except Exception:
                cursor.execute(
                    """
                    SELECT playedOn, total, scoreDiffer, runningHandicap
                    FROM Scores
                    WHERE golferID = %s
                    ORDER BY playedOn DESC
                    """,
                    (golfer_id,)
                )
                rows = cursor.fetchall() or []
                rounds = [
                    {
                        "playedOn": row.get("playedOn"),
                        "total": row.get("total", "-"),
                        "scoreDiffer": row.get("scoreDiffer", "-"),
                        "runningHandicap": row.get("runningHandicap", "-"),
                    }
                    for row in rows
                ]

            return {"results": 1, "summary": summary, "rounds": rounds}
    except Exception as e:
        return handleDbError(e)
    finally:
        if conn and not isinstance(conn, dict) and conn.is_connected():
            conn.close()


def getCorseOptions():
    conn = sqlConector()
    if isinstance(conn, dict) and "error" in conn:
        return conn

    try:
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(
                """
                SELECT courseID, courseName
                FROM Corse
                ORDER BY courseName ASC
                """
            )
            courses = cursor.fetchall() or []

            cursor.execute(
                """
                SELECT teeID, corseID, teeColor, teeSlope, teeRating, teePar
                FROM Tees
                ORDER BY corseID ASC, teeColor ASC
                """
            )
            tees = cursor.fetchall() or []

            tees_by_course = {}
            for tee in tees:
                course_id = tee.get("corseID")
                tees_by_course.setdefault(course_id, []).append({
                    "teeID": tee.get("teeID"),
                    "teeColor": tee.get("teeColor"),
                    "teeSlope": tee.get("teeSlope"),
                    "teeRating": float(tee.get("teeRating")) if tee.get("teeRating") is not None else None,
                    "teePar": tee.get("teePar"),
                })

            payload = []
            for course in courses:
                course_id = course.get("courseID")
                payload.append({
                    "courseID": course_id,
                    "courseName": course.get("courseName"),
                    "tees": tees_by_course.get(course_id, []),
                })

            return {"results": 1, "courses": payload}
    except Exception as e:
        return handleDbError(e)
    finally:
        if conn and not isinstance(conn, dict) and conn.is_connected():
            conn.close()


def addRound(payload):
    conn = sqlConector()
    if isinstance(conn, dict) and "error" in conn:
        return conn

    try:
        golfer_id = int(payload.get("golferID"))
        tee_id = int(payload.get("teeID"))
        hole_count = int(payload.get("holeCount"))
        if hole_count not in (9, 18):
            return {"error": "holeCount must be 9 or 18"}

        round_date_raw = (payload.get("date") or "").strip()
        round_time_raw = (payload.get("time") or "").strip()

        if round_date_raw:
            date_played = datetime.strptime(round_date_raw, "%Y-%m-%d").date()
        else:
            date_played = datetime.now().date()

        if round_time_raw:
            time_played = datetime.strptime(round_time_raw, "%H:%M").time()
        else:
            time_played = datetime.now().time().replace(microsecond=0)

        hole_scores = []
        for i in range(1, hole_count + 1):
            raw = payload.get(f"hole{i}")
            if raw is None or str(raw).strip() == "":
                return {"error": f"hole{i} is required"}
            hole_scores.append(int(raw))

        total = sum(hole_scores)
    except (TypeError, ValueError) as e:
        return {"error": f"Invalid input: {e}"}

    try:
        conn.autocommit = False
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute("SELECT * FROM Golfer WHERE golferID = %s", (golfer_id,))
            golfer = cursor.fetchone()
            if not golfer:
                conn.rollback()
                return {"error": "Golfer not found"}

            cursor.execute(
                """
                SELECT teeID, teeSlope, teeRating, teePar
                FROM Tees
                WHERE teeID = %s
                """,
                (tee_id,)
            )
            tee = cursor.fetchone()
            if not tee:
                conn.rollback()
                return {"error": "Tee not found"}

            tee_slope = float(tee["teeSlope"])
            tee_rating = float(tee["teeRating"])
            tee_par = int(tee["teePar"])

            score_differ = _score_differ(total, hole_count, tee_rating, tee_slope)

            cursor.execute(
                """
                SELECT scoreDiffer
                FROM Rounds
                WHERE golferID = %s
                  AND scoreDiffer IS NOT NULL
                  AND (roundDate < %s OR (roundDate = %s AND roundTime < %s))
                ORDER BY roundDate DESC, roundTime DESC
                LIMIT 19
                """,
                (golfer_id, date_played, date_played, time_played)
            )
            previous_differs = [float(r["scoreDiffer"]) for r in cursor.fetchall() if r["scoreDiffer"] is not None]

            low_start_date = date_played - timedelta(days=365)
            cursor.execute(
                """
                SELECT MIN(runningHandicap) AS lowHI
                FROM Rounds
                WHERE golferID = %s
                  AND runningHandicap IS NOT NULL
                  AND roundDate >= %s
                  AND roundDate <= %s
                """,
                (golfer_id, low_start_date, date_played)
            )
            low_row = cursor.fetchone()
            lowest_handicap = float(low_row["lowHI"]) if low_row and low_row["lowHI"] is not None else None

            handicap_index, provisional = _calculate_handicap(score_differ, previous_differs, lowest_handicap)

            rounds_played_prev = int(golfer.get("roundsPlayed") or 0)
            season_total_prev = int(golfer.get("seasonTotal") or 0)

            rounds_played = rounds_played_prev + 1
            season_total = season_total_prev + (total - tee_par)
            round_avg = round(season_total / rounds_played, 2) if rounds_played > 0 else 0

            cursor.execute(
                """
                UPDATE Golfer
                SET handicap = %s,
                    roundsPlayed = %s,
                    roundAvg = %s,
                    seasonTotal = %s,
                    provitional = %s
                WHERE golferID = %s
                """,
                (handicap_index, rounds_played, round_avg, season_total, provisional, golfer_id)
            )

            hole_values = list(hole_scores) + ([None] * (18 - hole_count))
            cursor.execute(
                """
                INSERT INTO Rounds (
                    golferID, teeID, holes, roundDate, roundTime, total, scoreDiffer, runningHandicap,
                    hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8, hole9,
                    hole10, hole11, hole12, hole13, hole14, hole15, hole16, hole17, hole18
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    golfer_id, tee_id, hole_count, date_played, time_played, total, score_differ, handicap_index,
                    hole_values[0], hole_values[1], hole_values[2], hole_values[3], hole_values[4], hole_values[5], hole_values[6], hole_values[7], hole_values[8],
                    hole_values[9], hole_values[10], hole_values[11], hole_values[12], hole_values[13], hole_values[14], hole_values[15], hole_values[16], hole_values[17],
                )
            )

            conn.commit()
            return {
                "results": 1,
                "message": "Round saved successfully.",
                "handicap": handicap_index,
                "scoreDiffer": score_differ,
                "roundsPlayed": rounds_played,
                "roundAvg": round_avg,
                "seasonTotal": season_total,
            }
    except Exception as e:
        conn.rollback()
        return handleDbError(e)
    finally:
        if conn and not isinstance(conn, dict) and conn.is_connected():
            conn.close()


def addGolfer(payload):
    conn = sqlConector()
    if isinstance(conn, dict) and "error" in conn:
        return conn

    try:
        first_name = (payload.get("firstName") or "").strip().title()
        last_name = (payload.get("lastName") or "").strip().title()
        if not first_name or not last_name:
            return {"error": "firstName and lastName are required"}

        pre_existing = str(payload.get("preExistingInformation", "False")).strip().lower() == "true"

        if pre_existing:
            handicap = float(payload.get("handicap") or 0)
            rounds_played = int(payload.get("roundsPlayed") or 0)
            season_total = int(payload.get("seasonTotal") or 0)
            round_avg = float(payload.get("roundAvg") or 0)
            provisional = rounds_played < 8
        else:
            handicap = 0.0
            rounds_played = 0
            season_total = 0
            round_avg = 0.0
            provisional = True
    except (TypeError, ValueError) as e:
        return {"error": f"Invalid input: {e}"}

    try:
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(
                """
                SELECT golferID
                FROM Golfer
                WHERE firstName = %s AND lastName = %s
                """,
                (first_name, last_name)
            )
            existing = cursor.fetchone()
            if existing:
                return {"error": "Golfer already exists."}

            cursor.execute(
                """
                INSERT INTO Golfer (firstName, lastName, handicap, roundsPlayed, roundAvg, seasonTotal, provitional)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (first_name, last_name, handicap, rounds_played, round_avg, season_total, provisional)
            )
            golfer_id = cursor.lastrowid

            return {
                "results": 1,
                "message": "Golfer saved successfully.",
                "golferID": golfer_id,
                "firstName": first_name,
                "lastName": last_name,
                "handicap": handicap,
                "roundsPlayed": rounds_played,
                "roundAvg": round_avg,
                "seasonTotal": season_total,
            }
    except Exception as e:
        return handleDbError(e)
    finally:
        if conn and not isinstance(conn, dict) and conn.is_connected():
            conn.close()
