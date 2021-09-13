# RECEBE COMO PARÂMETROS UM ARRAY DE OBJETOS [{"vertical", "transversal"}] COM AS COORDENADAS DE MODO ORDENADO
import numpy as np


def stationArea(coordinates, draft):
    if len(coordinates) == 0:
        return 0

    coordsBellowDraft = []

    for key, value in enumerate(coordinates):
        vertical = value["vertical"]

        if vertical < draft:
            coordsBellowDraft.append(value)
        else:
            upper = coordinates[key]
            lower = coordinates[key - 1]

            breadth = np.interp(
                draft,
                [lower["vertical"], upper["vertical"]],
                [lower["transversal"], upper["transversal"]],
            )

            coordsBellowDraft.append(
                {"vertical": draft, "transversal": breadth, "type": "deck"}
            )
            coordsBellowDraft.append(
                {"vertical": draft, "transversal": 0, "type": "end"}
            )

            break

    coordsBellowDraft.append(coordsBellowDraft[0])

    area = 0

    for key in np.arange(len(coordsBellowDraft) - 1):
        xLower = coordsBellowDraft[key]["transversal"]
        xUpper = coordsBellowDraft[key + 1]["transversal"]

        yLower = coordsBellowDraft[key]["vertical"]
        yUpper = coordsBellowDraft[key + 1]["vertical"]

        part1 = xLower - yUpper
        part2 = xUpper - yLower

        area = part1 + part2

    area = abs(area / 2)

    return round(area, 4)
