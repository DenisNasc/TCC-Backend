from scipy import integrate
import numpy as np
from services.hidrostatics.calculateCoordsBelowDraft import calculateCoordsBelowDraft


def calculateLCF(
    longitudinals: list, stations: list, draft: float, AWL: float
) -> float:
    if len(stations) == 0:
        return 0.0

    coordinates = [e["coordinates"] for e in stations]

    coordsBelowDraft = []
    for coords in coordinates:
        coordsBelowDraft.append(calculateCoordsBelowDraft(coords, draft))

    halfBreadths = [e[-3]["transversal"] for e in coordsBelowDraft]
    moment = []

    for key, value in enumerate(halfBreadths):
        moment.append(value * longitudinals[key])

    LCF = 2 * integrate.simps(x=longitudinals, y=moment)

    return np.round(LCF / AWL, 4)
