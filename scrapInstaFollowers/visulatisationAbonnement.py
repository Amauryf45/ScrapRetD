from collections import defaultdict
from itertools import combinations
import matplotlib.pyplot as plt
import networkx as nx

import os
import json

import pandas as pd

# Définir le répertoire contenant les fichiers JSON
directory = r'C:\Users\amaur\Desktop\Cours EMA\2IA\RetD\scrapInstaFollowers\data'

# listes des page,abonnées mais que les abonnés a plus d'une page
output_file_filtered_path = os.path.join(directory, 'abonnements_filtres2.txt')

# Vérifier si le fichier de sortie existe déjà
if os.path.exists(output_file_filtered_path):
    print(f"Le fichier {output_file_filtered_path} existe déjà. Aucune action requise.")
else:
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

    output_file_path = os.path.join(directory, 'abonnements_tuples.txt')

    # Vérifier si le fichier de sortie existe déjà
    if os.path.exists(output_file_path):
        print(f"Le fichier {output_file_path} existe déjà. Aucune action requise.")
    else:
        # Initialiser une liste pour stocker les tuples (page, follower)
        abonnements = []

        # Parcourir tous les fichiers dans le répertoire
        for filename in os.listdir(directory):
            if filename.startswith("instagram_results_") and filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                
                # Extraire le nom de la page à partir du nom du fichier
                page_name = filename.replace("instagram_results_", "").replace(".json", "")

                # Lire le contenu du fichier JSON avec un encodage spécifié
                with open(filepath, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # Extraire les noms d'utilisateur des followers et créer des tuples (page, follower)
                for follower in data['followers']:
                    abonnements.append((page_name, follower['username']))

        # Sauvegarder les tuples dans un fichier
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for item in abonnements:
                f.write(f"{item[0]}, {item[1]}\n")

        print(f"Tuples sauvegardés dans {output_file_path}")


    # Recupération des données d'abonnement : [('page1', 'user1'), ('page1', 'user2'), ...]
    abonnements = [(line.split(", ")[0], line.split(", ")[1]) for line in open(output_file_path, 'r', encoding='utf-8').read().splitlines()]

    # Filtrer pour obtenir les usernames des followers qui suivent plus d'une page
    followers_mult_pages = df_follower_counts[(df_follower_counts['Nombre de Pages Suivies'] > 1) & (df_follower_counts['Nombre de Pages Suivies'] < 20)]['Username']

    # Convertir le DataFrame filtré en un ensemble pour des vérifications plus rapides
    followers_mult_pages_set = set(followers_mult_pages)

    # Filtrer la liste d'abonnements pour ne garder que ceux avec des abonnés suivant plus d'une page
    abonnements_filtres = [(page, follower) for page, follower in abonnements if follower in followers_mult_pages_set]

    # À ce stade, `abonnements_filtres` contient uniquement les tuples où les abonnés suivent plus d'une page.
    # Vous pouvez choisir de sauvegarder cette nouvelle liste ou de procéder à d'autres traitements.

    # sauvegarder la nouvelle liste d'abonnements filtrés dans un fichier
    with open(output_file_filtered_path, 'w', encoding='utf-8') as f:
        for item in abonnements_filtres:
            f.write(f"{item[0]}, {item[1]}\n")

    print(f"Abonnements filtrés sauvegardés dans {output_file_filtered_path}")


# Recupération des données d'abonnement : [('page1', 'user1'), ('page1', 'user2'), ...]
abonnements_filtres = [(line.split(", ")[0], line.split(", ")[1]) for line in open(output_file_filtered_path, 'r', encoding='utf-8').read().splitlines()]

# print("Creation Graph")
# G = nx.Graph()

# # Ajouter les arêtes au graphe
# for page, follower in abonnements_filtres:
#     G.add_node(page, type='page')
#     G.add_node(follower, type='follower')
#     G.add_edge(page, follower)

# # Préparer les options de couleur et d'étiquette
# node_colors = ['red' if G.nodes[node]['type'] == 'page' else 'skyblue' for node in G]
# labels = {node: node if G.nodes[node]['type'] == 'page' else '' for node in G}

# # Définir la position des nœuds en utilisant l'algorithme de mise en page force-directed
# pos = nx.spring_layout(G)

# # Dessiner le réseau avec les options spécifiées
# nx.draw(G, pos, labels=labels, node_color=node_colors, with_labels=True, node_size=700, edge_color='lightgray', linewidths=0.1, font_size=10, alpha=0.5)

# # Obtenir les arêtes du graphe
# edges = G.edges()

# # Rendre les nœuds bleus transparents
# for node, color in zip(G.nodes(), node_colors):
#     if color == 'skyblue':
#         nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color=color, alpha=0.1)

# # Afficher le graphe
# plt.show()

# Créer un dictionnaire où chaque clé est un abonné et chaque valeur est la liste des pages suivies par cet abonné
followers_pages = defaultdict(list)
for page, follower in abonnements_filtres:
    followers_pages[follower].append(page)

# Créer un dictionnaire pour compter les abonnés communs entre chaque paire de pages
shared_followers = defaultdict(int)
for follower, pages in followers_pages.items():
    for page1, page2 in combinations(pages, 2):
        shared_followers[(page1, page2)] += 1
        shared_followers[(page2, page1)] += 1  # Assurez-vous que la relation est bidirectionnelle

# Créer le graphe de co-abonnement
G = nx.Graph()
for (page1, page2), count in shared_followers.items():
    G.add_edge(page1, page2, weight=count)

# Visualisation
pos = nx.spring_layout(G)  # Peut-être coûteux pour les grands graphes
nx.draw(G, pos, with_labels=True, node_color='red', edge_color='gray', width=1, node_size=700)

plt.show()