import json
import os.path

# stations_info_divider = "-------------------------------"

# file_path = pathlib.Path().absolute()

# file_name = "tabela-cotas.txt"
# _, data_raw = input_data_to_json(file_path, file_name, stations_info_divider)


def format_text_to_json(file_path: str, file_name: str, stations_info_divider: str):

    path_to_file = os.path.join(file_path, file_name)

    textFileHandler = open(path_to_file, "r")
    textFileSplited = textFileHandler.read().strip().split(stations_info_divider)[:-1]

    stations = {}

    for i, line in enumerate(textFileSplited):
        station_infos = line.strip().split("\n")

        longitudinal = float(station_infos[0].strip().split(":")[1].replace(",", "."))
        coordinates = []

        for j, coordinate in enumerate(station_infos[3:]):
            vertical, transversal = coordinate.strip().replace(",", ".").split()[:2]
            new_coordinate = {
                "id": j,
                "vertical": float(vertical),
                "transversal": float(transversal),
            }
            coordinates.append(new_coordinate)

        new_station = {
            "longitudinal": longitudinal,
            "id": i,
            "coordinates": coordinates,
        }
        stations[f"station_{longitudinal}"] = new_station

    json_station = json.dumps(stations, indent=2)

    return json_station
