from scipy import integrate
import numpy as np
from services.hidrostatics.calculateCoordsBelowDraft import calculateCoordsBelowDraft


def calculateVCB(drafts: list, stations: list, AWL: float) -> float:

    moments = []

    coordinates = [e["coordinates"] for e in stations]

    for draft in drafts:
        coordsBelowDraft = []
        for coords in coordinates:
            coordsBelowDraft.append(calculateCoordsBelowDraft(coords, draft))

        halfBreadths = [e[-3]["transversal"] for e in coordsBelowDraft]
        moments.append(np.round(np.max(halfBreadths) * draft, 4))

    VCB = np.round(integrate.simpson(y=moments, x=drafts) / AWL, 4)
    return VCB
