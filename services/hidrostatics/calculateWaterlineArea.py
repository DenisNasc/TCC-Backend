from scipy import integrate
import numpy as np
from services.hidrostatics.calculateCoordsBelowDraft import calculateCoordsBelowDraft


def calculateWaterlineArea(longitudinals: list, stations: list, draft: float) -> list:
    if len(stations) == 0:
        return 0.0

    coordinates = [e["coordinates"] for e in stations]

    coordsBelowDraft = []
    for coords in coordinates:
        coordsBelowDraft.append(calculateCoordsBelowDraft(coords, draft))

    halfBreadths = [e[-3]["transversal"] for e in coordsBelowDraft]
    waterlineArea = 2 * integrate.simps(x=longitudinals, y=halfBreadths)

    return np.round(waterlineArea, 4)
