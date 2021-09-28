# RECEBE COMO PARÂMETROS UM ARRAY DE OBJETOS [{"vertical", "transversal"}] COM AS COORDENADAS DE MODO ORDENADO
import numpy as np
from services.hidrostatics.calculateCoordsBelowDraft import calculateCoordsBelowDraft


def calculateStationArea(coordinates: list, draft: float) -> float:
    if len(coordinates) == 0:
        return 0.0

    coordsBellowDraft = calculateCoordsBelowDraft(coordinates, draft)

    area = 0

    for key in np.arange(len(coordsBellowDraft) - 1):
        xLower = coordsBellowDraft[key]["transversal"]
        xUpper = coordsBellowDraft[key + 1]["transversal"]

        yLower = coordsBellowDraft[key]["vertical"]
        yUpper = coordsBellowDraft[key + 1]["vertical"]

        part1 = xLower * yUpper
        part2 = xUpper * yLower

        area += part1 - part2

    area = abs(area)
    print(draft, area, coordsBellowDraft)

    return round(area, 4)
