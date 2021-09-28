from scipy import integrate
import numpy as np
from services.hidrostatics.calculateCoordsBelowDraft import calculateCoordsBelowDraft


def calculateVCB(drafts: list, AWLs: list, volume: float) -> float:
    moments = []
    for key, value in enumerate(drafts):
        moments.append(AWLs[key] * value)

    VCB = round(integrate.simps(x=drafts, y=moments) / volume, 4)
    print(moments)
    return VCB
