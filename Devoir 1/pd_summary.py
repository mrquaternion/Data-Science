"""
Ce devoir est basé sur [le cours de science des données de Greg Baker à SFU

Toutes les zones qui nécessitent des travaux sont marquées d'une étiquette "TODO".
"""
import pandas as pd


def city_lowest_precipitation(totals: pd.DataFrame) -> str:
    """
    Étant donné un dataframe où chaque ligne représente une ville et chaque colonne est un mois 
    de janvier à décembre d'une année particulière, retourne la ville avec les précipitations totales les plus faibles.
    """
    row_sums = totals.sum(axis=1)  # find sum of each row
    lowest_precipitations_index_label = row_sums.idxmin() # find index of the minimum row sum

    return lowest_precipitations_index_label


def avg_precipitation_month(totals: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    """
    Déterminez les précipitations moyennes à ces endroits pour chaque mois. Ce sera le total des précipitations pour 
    chaque mois, divisé par le total des observations pour ce mois.
    """

    return totals.sum(axis=0) / counts.sum(axis=0)


def avg_precipitation_city(totals: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    """
    Faites de même pour les villes : donnez la précipitation moyenne (précipitation quotidienne moyennes sur le mois) 
    pour chaque ville.
    """

    return totals.sum(axis=1) / counts.sum(axis=1)


# pas de trimestriel car c'est un peu pénible


def main():
    totals = pd.read_csv("data/totals.csv").set_index(keys=["name"])
    counts = pd.read_csv("data/counts.csv").set_index(keys=["name"])

    # You can use this to steer your code
    print(f"Rangée avec la précipitations la plus faible:\n{city_lowest_precipitation(totals)}")
    print(f"La précipitation moyenne par mois:\n{avg_precipitation_month(totals, counts)}")
    print(f"La précipitation moyenne par ville:\n{avg_precipitation_city(totals, counts)}")


if __name__ == "__main__":
    main()
