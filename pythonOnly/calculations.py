

def scoreDiffer(ajustatedScoreTotal, holeNumber, corseRating, corseSlop):    
    
    if holeNumber == 9:
        # Calculate Score Differential
        scoreDiffer = round(((ajustatedScoreTotal * 2) - corseRating) * (113 / corseSlop), 2) 
    else:        
        # Calculate Score Differential         
        scoreDiffer = round((ajustatedScoreTotal - corseRating) * (113 / corseSlop), 2)  

    return scoreDiffer
         # scoreDiffer = calculations.scoreDiffer(ajustatedScoreTotal, holeNumber, corseRating, corseSlop)


def handicap(ScoreDiffer, proceeding20Scores, LowestHandicap):

    proceeding20Scores.append(ScoreDiffer)
    
    #Sort the aray then take only the best 8, avrage them out, and put that in a new variable. 
    proceeding20Scores.sort()
    Best8Set = proceeding20Scores[:8]    
    
    AvregeOf8 = sum(Best8Set)/ len(Best8Set)
    TepHandicap = round(AvregeOf8 * 0.96, 2)

    # else:
        # FIX ME !!!  Calculate temp Handicap with less then 8 scores

    # Calculate the soft and hard cap
    softCap = LowestHandicap + 3                                                                       # FIX ME!!!! (Problem Below)
    hardCap = LowestHandicap + 5                                                                       # FIX ME!!!! (Problem Below)
    #If the player has no preveas handicap data gives an errorCheck why"unsupported operand type(s) for +: 'NoneType' and 'int'"


    # Check if the new handicap goes over the soft or hard cap and set handicap index
    if TepHandicap > softCap:
        aboveSoftCap = round(((TepHandicap - softCap)*.5),2)
        handicapIndex = softCap + aboveSoftCap
        if handicapIndex > hardCap:
            handicapIndex = hardCap
    elif ScoreDiffer < (TepHandicap - 7):
        if ScoreDiffer < (TepHandicap - 9.9):
            handicapIndex = TepHandicap - 2
        else:
            handicapIndex = TepHandicap - 1
    else:
        handicapIndex = TepHandicap     
     
        # Return the results of the handicap calculations 
    return handicapIndex
         # handicapIndex = calculations.handicap(scoreDiffer, proceeding20Scores, LowestHandicap)

    #   Handicap index calculation rules
    #       When a score is posted, it is converted into a score differential that accounts for the difficulty of the course and the tees played. 
    #       Average of the 8 best scores out of 20 rounds
    #       Measures the demonstrated ability on their better days
    #       Once a player's index has increased by 3 strokes, the rate of increase slows by 50%
    #       Can not increase more than 5 in one year
    #       if you post a score with a score differential of 7 - 9.9 strokes better, the handicap index handicap is reduced by an additional stroke
    #       If it is 10 or better, the handicap is reduced by 2