import os
import json
import pandas as pd

# Définir le répertoire contenant les fichiers JSON
directory = r'C:\Users\amaur\Desktop\Cours EMA\2IA\RetD\scrapInstaFollowers\data'

# Initialiser un dictionnaire pour stocker le nombre d'apparitions de chaque follower
follower_counts = {}

# Parcourir tous les fichiers dans le répertoire
for filename in os.listdir(directory):
    if filename.startswith("instagram_results_") and filename.endswith(".json"):
        filepath = os.path.join(directory, filename)

        # Lire le contenu du fichier JSON avec un encodage spécifié
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extraire les noms d'utilisateur des followers
        followers = [follower['username'] for follower in data['followers']]

        # Mettre à jour le nombre d'apparitions de chaque follower
        for follower in followers:
            follower_counts[follower] = follower_counts.get(follower, 0) + 1

# Convertir le dictionnaire en DataFrame
df_follower_counts = pd.DataFrame(list(follower_counts.items()), columns=['Username', 'Nombre de Pages Suivies'])

# Trier le DataFrame par 'Nombre de Pages Suivies' dans un ordre décroissant
df_follower_counts.sort_values(by='Nombre de Pages Suivies', ascending=False, inplace=True)

# Sauvegarder le DataFrame dans un fichier CSV
csv_file_path = os.path.join(directory, 'resultat_compte_followers.csv')
df_follower_counts.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print(f"Résultat sauvegardé dans {csv_file_path}")
