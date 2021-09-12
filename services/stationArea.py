# RECEBE COMO PARÂMETROS UM ARRAY DE OBJETOS [{"vertical", "transversal"}] COM AS COORDENADAS DE MODO ORDENADO
def stationArea(coordinates, draft):
    if len(coordinates) == 0:
        return 0

    first_part = 0
    second_part = 0

    coordsBellowDraft = []

    for key, value in enumerate(coordinates):
        vertical = value["vertical"]

        if vertical < draft:
            coordsBellowDraft.append(value)
        else:
            upper = coordinates[key]
            lower = coordinates[key - 1]

            breadth = (
                (upper["transversal"] - lower["transversal"])
                * (draft - lower["vertical"])
                / (upper["vertical"] - lower["vertical"])
            ) + lower["transversal"]

            coordsBellowDraft.append({"vertical": draft, "transversal": breadth})
            coordsBellowDraft.append({"vertical": draft, "transversal": 0})

            break

    print(coordsBellowDraft)

    # for key, coord in enumerate(coordsBellowDraft):
    #     vert = coord["vertical"]
    #     i = key + 1

    #     if i > length:
    #         i = 0

    #     first_part += vert * coordsBellowDraft[i]["transversal"]

    # for key, coord in enumerate(coordsBellowDraft):
    #     trans = coord["transversal"]
    #     i = key + 1

    #     if i > length:
    #         i = 0

    #     second_part += trans * coordsBellowDraft[i]["vertical"]

    # area = abs(first_part - second_part) / 2

    return 10
