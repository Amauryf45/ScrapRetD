import json

# Charger le fichier JSON
with open('C:\\Users\\amaur\\Desktop\\Cours EMA\\2IA\\RetD\\scrapFacebookPost\\facebookGroupPostsAndComments.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filtrer les données avec postText non vide
filtered_data = [entry for entry in data if (entry.get('postText') != "")]

# Écrire les données filtrées dans un nouveau fichier JSON
with open('dataPosts.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, indent=2, ensure_ascii=False)
