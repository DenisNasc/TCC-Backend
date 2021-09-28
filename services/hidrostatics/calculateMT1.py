def calculateMT1(displacement: float, LPP: float, GML: float):
    MTC1 = (displacement * GML) / (100 * LPP)
    return round(MTC1, 4)
