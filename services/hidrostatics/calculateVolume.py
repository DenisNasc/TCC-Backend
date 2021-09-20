from scipy import integrate


def calculateVolume(longitudinals: list, stationsAreas: list) -> float:

    volume = round(integrate.simpson(y=stationsAreas, x=longitudinals), 4)

    return volume
