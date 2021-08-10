# RECEBE COMO PARÂMETROS UM ARRAY DE OBJETOS [{"vertical", "transversal"}] COM AS COORDENADAS DE MODO ORDENADO
def stationArea(coordinates):
    if len(coordinates) == 0:
        return 0

    length = len(coordinates) - 1
    first_part = 0
    second_part = 0

    for key, coord in enumerate(coordinates):
        vert = coord["vertical"]
        i = key + 1

        if i > length:
            i = 0

        first_part += vert * coordinates[i]["transversal"]

    for key, coord in enumerate(coordinates):
        trans = coord["transversal"]
        i = key + 1

        if i > length:
            i = 0

        second_part += trans * coordinates[i]["vertical"]

    area = abs(first_part - second_part) / 2
    return area
