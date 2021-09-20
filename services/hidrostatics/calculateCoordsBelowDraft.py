import numpy as np


def calculateCoordsBelowDraft(coordinates: list, draft: float) -> list:
    coordsBellowDraft = []
    for key, value in enumerate(coordinates):

        vertical = value.vertical
        transversal = value.transversal
        type = value.transversal

        if vertical < draft:
            coordsBellowDraft.append(
                {
                    "vertical": vertical,
                    "transversal": transversal,
                    "type": type,
                }
            )
        else:
            upper = coordinates[key]
            lower = coordinates[key - 1]

            breadth = np.interp(
                draft,
                [lower.vertical, upper.vertical],
                [lower.transversal, upper.transversal],
            )

            coordsBellowDraft.append(
                {"vertical": draft, "transversal": breadth, "type": "deck"}
            )
            coordsBellowDraft.append(
                {"vertical": draft, "transversal": 0, "type": "end"}
            )

            break

    coordsBellowDraft.append(coordsBellowDraft[0])

    return coordsBellowDraft
