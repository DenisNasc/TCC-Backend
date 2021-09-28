from scipy import integrate

from services.hidrostatics.calculateCoordsBelowDraft import calculateCoordsBelowDraft


def calculateBM(longitudinals: list, stations: list, draft: float, volume: float):
    coordinates = [e["coordinates"] for e in stations]

    coordsBelowDraft = []
    for coords in coordinates:
        coordsBelowDraft.append(calculateCoordsBelowDraft(coords, draft))

    halfBreadths = [e[-3]["transversal"] for e in coordsBelowDraft]
    cubeHalfBreadths = [e ** 3 for e in halfBreadths]
    result = integrate.simps(x=longitudinals, y=cubeHalfBreadths)
    transversalInertia = result / 3

    return round(2 * transversalInertia / volume, 4)
