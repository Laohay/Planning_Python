# Importer les bibliothèques nécessaires
import pandas as pd
import numpy as np

# Fonction pour traiter les plages horaires dans les cellules du DataFrame
def fixed_process_time_range(time_range_str):
    # Remplacer tous les 'H', 'h' et les espaces pour normaliser la chaîne
    time_range_str = time_range_str.replace(' ', '').replace('H', ',').replace('h', ',')
    # Diviser la chaîne en une liste, en éliminant les chaînes vides
    time_values = list(filter(lambda x: x != '', time_range_str.split(',')))#dans le cadre des fonction python execute de droite a gauche surtout de l interieur vers l exterieur
                                                                            #on split les str avec separateur (,), pour on applique la lambda qui fait sauter les espaces vides
                                                                            #puis avec ce resultat on cree une liste avec list()
    # Convertir chaque élément de la liste en entier
    time_values = list(map(int, time_values))
    # Initialiser une liste de 17 zéros (pour les heures de 7 à 23)
    hour_flags = [0] * 17 #[0] est une list avec un 0 qui est multiplie 17 fois ce qui creer une liste de 17 zeros
    
    # Remplir la liste avec des 1 pour chaque plage horaire
    for i in range(0, len(time_values), 2):#boucle  avec un range dont le depart est 0 jusqu a la taille de l argument des horaire, avec un pas de 2 car les celule on deux horaire debut fin
        start_time = time_values[i]#en utilisant les indice de la liste on recupere logiquement les horaire de debut car c est toujours le premier indice dans un paire
        end_time = time_values[i + 1]#en utilisant les indice de la liste on recupere logiquement les horaire de fin avec le i+1 car c est toujours le second indice dans un paire
        start_index = start_time - 7#la valeur qu on as quelque soit dans la boucle -7 pour tjrs donner la valeur dans une plage de 7 a 23 plutot que 0 23
        end_index = end_time - 7#meme principe qu au dessus
        for i in range(start_index, end_index):#a chaque tour de boucle il recupere le range de start a end et rempli la list de 17 zero par des 1 en consequence du range
            hour_flags[i] = 1
            
    return hour_flags

# Charger le fichier Excel dans un DataFrame
input_df = pd.read_excel('algo_test.xlsx', sheet_name='Input')

# Initialiser un dictionnaire pour stocker les horaires de travail
schedule_dict = {}

# Itérer sur chaque ligne du DataFrame pour remplir le dictionnaire
for index, row in input_df.iterrows():#grace a la methode iterrows du package pandas on peut recuperer une paire de valeur en premier l index et en second la ligne sous forme
                                        #d objet serie pandas 
    name = row['Nom']#on recupere chaque valeur de la colone nom par ligne 
    schedule_dict[name] = {}#cette ligne permet de creer un dictionaire dont la clef sera les valeurs de [name] et dont les clefs seront vides pour le momentc est une technique syntaxique
                            #on ecrit le nom du dico on passe la clef entre crochet et on lui donne une valeur vide.
    
    # Traiter chaque jour de la semaine
    for day in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']:#cela cree a chaque tour une variable day qui va prendre commme valeur le jour de la semaine
                                                                                        #en cours  et qui sera utilise par la variable row pour recuperer la valeur de la cellule
        # Si c'est un jour de repos, remplir avec des zéros
        if row[day] == 'Repos':#ne pas oublier que c est une boucle interne donc row est deja une serie pandas determine dans day on a la colone du coup la cellule exacte si elle egale a repons on rempli de zero
            schedule_dict[name][day] = [0]*17
        else:
            # Sinon, utiliser la fonction pour obtenir une liste de 0 et de 1
            schedule_dict[name][day] = fixed_process_time_range(row[day])#si ce n est pas repos alors alors on recupere le nom et le jour qu on passe en argument a la 
                                                                        #fonction fixed_process_time_range pour recupre la series pandas

# Créer le DataFrame de sortie à partir du dictionnaire
output_rows = []
for name, days in schedule_dict.items():#ne pas oublie que le la methode .items des dictionaire permet de recuperer les clef et les valeurs sans avoir a creer de variable intermediaire appelant la valeur avec la clef 
    for i in range(17):#on cree une boucle qui va de 0 a 17 car on a 17 ligne par nom
        row = {'Nom': name}#nom et le nom de la colone du df de sortie et name la valeurqui sera place dans la colone nom pour la ligne en cours
        for day, hours in days.items():
            row[day] = hours[i]
        output_rows.append(row)

# Convertir la liste de dictionnaires en DataFrame
output_df_new = pd.DataFrame(output_rows)

# Ajouter la colonne "Horaire"
hour_range = list(range(7, 24))
hour_range_extended = hour_range * (len(output_df_new) // len(hour_range))
output_df_new['Horaire'] = hour_range_extended

# Réorganiser les colonnes
cols = ['Nom', 'Horaire'] + [day for day in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']]
output_df_new = output_df_new[cols]

# Sauvegarder le DataFrame dans un fichier Excel
output_df_new.to_excel('output_transformed.xlsx', index=False, sheet_name='Output')

"""Éléments complexes :
Traitement des chaînes de caractères pour les plages horaires : Les plages horaires sont écrites en divers formats (avec des 'H', 'h', des espaces, des virgules). Le défi était de normaliser ces chaînes pour en extraire les informations nécessaires.

Gestion des cas spéciaux ('Repos') : La gestion des jours de repos, où tous les horaires devaient être marqués comme '0', a nécessité une condition spéciale dans le code.

Réorganisation du DataFrame : Une fois le DataFrame généré, il a fallu réorganiser les colonnes et ajouter une colonne d'horaire pour chaque personne.

Algorithmes utilisés :
Traitement des chaînes de caractères : Conversion de toutes les variantes de 'h' en une seule et élimination des espaces pour normaliser les chaînes.

Mapping et réduction : Utilisation de la fonction map pour convertir des chaînes en entiers et remplissage d'une liste de 17 éléments (pour les heures de 7 à 23) avec des '0' ou des '1' en fonction des plages horaires.

Itération et remplissage du DataFrame : Itération sur chaque ligne de l'entrée et utilisation d'un dictionnaire pour stocker les valeurs temporaires avant de créer le DataFrame de sortie.

Compétences à travailler :
Manipulation de chaînes de caractères en Python : Le traitement efficace des chaînes est crucial pour des tâches comme celle-ci.

Pandas DataFrame Manipulation : Comprendre comment manipuler les DataFrames en utilisant des fonctions intégrées peut rendre le code plus efficace.

Débogage et résolution de problèmes : La capacité à identifier et résoudre les erreurs dans le code est inestimable."""
