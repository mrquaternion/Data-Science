"""
Toutes les sections qui requièrent du travail sont marqués par "TODO".
"""
import numpy as np
import pandas as pd
from pathlib import Path
import shutil
from tqdm.autonotebook import tqdm
from typing import Tuple
import xml.etree.ElementTree as ET


# TODO - complétez cette méthode
def parse_xml(path: str) -> pd.DataFrame:
    """
    Parsez le fichier XML obtenu à partir de la base de données du lecteur FIDE qui peut être trouvé ici :

        http://ratings.fide.com/download.phtml?period=2022-10-01

    Notez que les scores sont mises à jour assez régulièrement, nous utilisons donc l'horodatage fixe de
    06 Oct 2022, qui vous est fourni dans le répertoire de données. Vous ne devriez pas avoir besoin de télécharger quoi que ce soit

    Arguments:
        path (str) : chemin d'accès au fichier .xml souhaité ; s'il n'existe pas, cherche automatiquement pour le fichier .zip correspondant à extraire

    Retour:
        pd.DataFrame : DataFrame contenant les données brutes du fichier xml, avec les colonnes :
            ["nom", "classement", "sexe", "anniversaire", "pays", "drapeau", "titre"]
    """
    path = Path(path)

    # unzip xml data if unavailable
    if not path.is_file():
        if path.with_suffix(".zip").is_file():
            shutil.unpack_archive(path.with_suffix(".zip"), path.parent)
        else:
            raise FileNotFoundError("%s nor an archive exists." % path)

    # define function to extract value, define tags to extract 
    _get_val = lambda entry, tag: entry.find(tag).text
    TARGET_ATTRIBUTES = ["name", "rating", "sex", "birthday", "country", "flag", "title"]

    # ----------  NE MODIFIEZ PAS LA FONCTION AU-DESSUS DE CETTE LIGNE ---------- #

    # TODO: 
    # Arbre d'élément XML (utilisez xml.etree.ElementTree)
    tree = ET.parse(path)
    root = tree.getroot() # Source : https://docs.python.org/3/library/xml.etree.elementtree.html

    # TODO: itérez sur le root node, pour obtenir les valeurs désirées pour les étiquettes désirées
    # Assurez-vous de chargez toutes les valeurs de TARGET_ATTRIBUTES (utilisez le même nom de colonne dans le dataframe comme nom d'étiquette!). Vous pouvez utilisez la méthode _get_val(person, tag) fournie définie en haut pour obtenir l'étiquette correspondante
    my_dict = {}
    for column_name in TARGET_ATTRIBUTES:
        my_dict[column_name] = []

    for child in root:
        for sub_child in child:
            if sub_child.tag in TARGET_ATTRIBUTES:
                my_dict[sub_child.tag].append(sub_child.text)

    # TODO: Convertir en dataframe

    return pd.DataFrame.from_dict(my_dict)


# TODO - complétez cette méthode
def clean_data(df: pd.DataFrame, year_cutoff: int) -> pd.DataFrame:
    """

    Arguments :
        df (pd.DataFrame) : la trame de données brute renvoyée par la méthode parse_xml()
        year_cutoff (entier) : supprimer les joueurs dont les anniversaires sont SUPÉRIEURS À (>) cette valeur; c'est-à-dire seulement
            inclure les joueurs nés jusqu'à (et y compris) cette année

    Retour:
        pd.DataFrame : Dataframe nettoyé
    """
    tmp_df = df.copy()

    # TODO: Enlever données sans information de date de naissance
    tmp_df = tmp_df.dropna(subset=['birthday'])

    # TODO: Convertissez les types numériques en entiers
    tmp_df['rating'] = tmp_df['rating'].astype(int)
    tmp_df['birthday'] = tmp_df['birthday'].astype(int)

    # TODO: Gardez juste les joueurs avec une date de naissance jusqu'à year_cutoff (inclusivement)
    tmp_df = tmp_df[tmp_df['birthday'] <= year_cutoff]

    return tmp_df


# TODO - complétez cette méthode
def bin_counts(df: pd.DataFrame, bins: list, bin_centers: list) -> pd.DataFrame:
    """ Renvoie un DataFrame avec les `ratings` regroupés entre les valeurs données dans `bins`, et
    avec une étiquette donnée par `bin_centers`. En plus du nombre brut, ajoutez également une colonne normalisée nommée "count_norm" obtenu en divisant les comptes par la somme des comptes.

    Ex : Donné
        >> x = pd.DataFrame({'rating' : [1, 2, 4, 6, 6, 7, 8, 11]})
        >> bacs = [0, 5, 10, 15]
        >> bin_centers = [2.5, 7.5, 12.5]
    
    bin_counts(x, bins, bin_centers) doit renvoyer :
        >>      rating  count  count_norm
        >>  0    7.5      4       0.500
        >>  1    2.5      3       0.375
        >>  2   12.5      1       0.125

    Arguments :
        df (pd.DataFrame): Dataframe nettoyé avec au moins la colonne 'rating'
        bacs (liste) : définit les bords des bacs ; c'est-à-dire que [0, 5, 10] définit deux classes : [0, 5) et [5, 10]
        bin_centers (liste) : Définit les étiquettes qui seront utilisées ; c'est-à-dire [2,5, 7,5] pour ce qui précède
        va mettre les valeurs comme [0, 5) -> 2.5, et [5, 10) -> 7.5.

    Retour:
        pd.DataFrame : dataframe avec des valeurs groupées ; doit avoir les colonnes
            ['rating', 'count', 'count_norm']. Renommez-les si nécessaire.
    """
    if 'rating' not in df.keys():
        raise ValueError("Incorrect input format; 'rating' must be a column in the input dataframe")

    tmp_df = df.copy()

    # TODO: Astuce - utilisez pd.cut, et assurez-vous d'utiliser reset_index() quand utile
    tmp_df['bins'] = pd.cut(tmp_df['rating'], bins=bins, labels=bin_centers, right=False)
    hist = tmp_df['bins'].value_counts().reset_index()

    # TODO: Renommer les colonnes, assurez qu'ils ont encore du sens (nous voulons 'rating', 'count')
    # Note: Vous ne devriez pas avoir à renommer les colonnes. Si vous devez, vous avez peut-être une version vielle de Pandas ce qui pourrait amener à des problèmes avec le autograder.
    hist.columns = ['rating', 'count']

    # TODO: Ajoutez la colonne 'count_norm'
    count_total = len(tmp_df['rating'])
    hist['count_norm'] = hist['count'].apply(lambda x : x / count_total)

    return hist


class PermutationTest:
    def __init__(self, df: pd.DataFrame, n_overrep: int, n_underrep: int):
        """ Implémente l'expérience de test de permutation.

         Arguments :
             df (pd.DataFrame) : trame de données complète à partitionner (c'est-à-dire inclut les deux groupes)
             n_overrep (entier) : nombre d'éléments dans le groupe surreprésenté
             n_underrep (entier) : nombre d'éléments dans le groupe sous-représenté
        
         n_overrep + n_underrep devrait être == len(df) ! Techniquement < len(df) est correct aussi...
         """
        if len(df) < n_overrep + n_underrep:
            raise ValueError(f"Sum of n_overrep + n_underrep must be <= len(df)")
        self.df = df
        self.n_overrep = n_overrep
        self.n_underrep = n_underrep
    
    # TODO - complétez cette méthode
    def job(self, seed: int = None) -> Tuple[int, int]:
        """ Échantillonne deux groupes de taille n_overrep, n_underrep et renvoie la note maximale pour chacun des
        groupe dans cet ordre (overrep, underrep)

        Arguments :
            seed (int, optionnel) : définit l'état aléatoire, si spécifié.

        Retour:
            Tuple[int, int] : les notes maximales pour chacun des deux groupes, dans l'ordre (max(surreprésentation), max(sous-représentation))
         """
        if seed is not None:
            np.random.seed(seed)
            
        # TODO : échantillonnez deux groupes de taille n_overrep, n_underrep et renvoyez la note maximale pour chacun
        # des groupe dans l'ordre (overrep, underrep)
        permutation = np.random.permutation(self.df.rating.values)
        permutation_overrep = permutation[:self.n_overrep]
        permutation_underrep = permutation[self.n_overrep:self.n_overrep + self.n_underrep]
        
        # Astuce : pensez à utiliser np.random.permutation sur un choix approprié de tableau
        return np.max(permutation_overrep), np.max(permutation_underrep)


# TODO - complétez cette méthode
def sample_two_groups(
    df: pd.DataFrame, n_overrep: int, n_underrep: int, n_iter: int=1000
) -> Tuple[np.array, np.array]:
    """Exécutez des tests de permutation n_iter sur df, divisé en deux groupes (échantillonnés SANS remplacement) de
    taille n_overrep et n_underrep. Renvoyez deux tableaux numpy de longueur n_iter, ou les éléments correspondent à la
    note maximale dans les groupes surreprésentés et sous-représentés respectivement.

    Arguments :
        df (pd.DataFrame) : dataframe nettoyé à traiter
        n_overrep (entier) : nombre d'échantillons pour le groupe surreprésenté
        n_underrep (entier) : nombre d'échantillons pour le groupe sous-représenté
        n_iter (entier, facultatif) : le nombre total d'itérations à exécuter

    Retour:
        Tuple[np.array, np.array] : Deux tableaux contenant les maximums pour le groupe surreprésenté et le groupe sous-représenté pour chacune des expériences n_iter.
    """
    best_over = []
    best_under = []

    # TODO : exécutez n_iter runs de cette expérience et renvoyez un tableau numpy contenant les valeurs maximales des groupes surreprésentés et sous-représentés respectivement.
    permutation_test = PermutationTest(df, n_overrep, n_underrep)
    for _ in tqdm(range(n_iter)):
        max_over, max_under = permutation_test.job()
        best_over.append(max_over)
        best_under.append(max_under)

    # Astuce : enveloppez votre itérateur avec tqdm pour obtenir une barre de progression, par exemple :
    # >>> for i in tqdm(range(10)):
    # >>>     print(i)

    return np.array(best_over), np.array(best_under)


