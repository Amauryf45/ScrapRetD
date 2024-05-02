import json
import os
import pandas as pd

# Définir le répertoire contenant les fichiers JSON
directory = '/chemin/vers/le/repertoire'

# Parcourir tous les fichiers dans le répertoire
for filename in os.listdir(directory):
    if filename.startswith("instagram_results_") and filename.endswith(".json"):
        filepath = os.path.join(directory, filename)
        # Extraire le nom de l'utilisateur de chaque fichier
        username = filename.replace("instagram_results_", "").replace(".json", "")

        # Lire le contenu du fichier JSON
        with open(filepath, 'r') as file:
            data = json.load(file)

        # Créer un dataframe pour les followers
        followers_df = pd.DataFrame(data['followers'])

        # Renommer les colonnes pour éviter les conflits de noms
        followers_df.columns = [f"follower_{col}" for col in followers_df.columns]

        # Nommez le dataframe avec le nom de l'utilisateur
        dataframe_name = "DataFrame_" + username
        globals()[dataframe_name] = followers_df

# Vous pouvez maintenant accéder à chaque dataframe par son nom, par exemple DataFrame_NOMASSO
