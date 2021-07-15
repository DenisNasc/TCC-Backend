import pandas as pd
from datetime import datetime
import pathlib


def input_data_to_excel(data_raw: dict):
    try:
        path_where_write = pathlib.Path().absolute()
        file_name = f"tabela-cotas-[{datetime.now()}].xlsx"

        columns = [
            "Station_ID",
            "Coordinate_ID",
            "Longitudinal",
            "Vertical",
            "Transversal",
        ]

        excel_sheet = []

        for value in data_raw.values():

            station_id = value["id"]
            longitudinal = value["longitudinal"]
            coordinates = value["coordinates"]

            for coordinate in coordinates:
                coordinate_id = coordinate["id"]
                vertical = coordinate["vertical"]
                transversal = coordinate["transversal"]

                excel_tuple = [
                    station_id,
                    coordinate_id,
                    longitudinal,
                    vertical,
                    transversal,
                ]
                excel_sheet.append(excel_tuple)

        sheet = pd.DataFrame(
            data=excel_sheet,
            columns=columns,
        )

        sheet.to_excel(
            f"{path_where_write}/static/sheets/{file_name}",
            index_label="ID",
        )

        return file_name

    except:
        return "Um problema ocorreu"