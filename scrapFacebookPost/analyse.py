import json
from collections import Counter
import statistics
import re
import matplotlib.pyplot as plt


# Chargeons les données JSON depuis un fichier
with open('C:\\Users\\amaur\\Desktop\\Cours EMA\\2IA\\RetD\\scrapFacebookPost\\dataPosts.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Variables pour stocker les informations
authors = set()
total_length = 0
total_links = 0
total_emojis = 0

# Regex pour détecter les URLs et les emojis
url_pattern = re.compile(r'https?://\S+')
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
word_pattern = re.compile(r'\b\w+\b')
hashtag_pattern = re.compile(r'#\w+')

# Dictionnaire pour compter les posts par auteur
author_post_count = Counter()

# Analyse des données
for post in data:
    authors.add(post['postAuthor'])
    author_post_count[post['postAuthor']] += 1
    post_text = post['postText']
    
    # Calculs pour chaque post
    total_length += len(post_text)
    total_links += len(url_pattern.findall(post_text))
    total_emojis += len(emoji_pattern.findall(post_text))

# Calculs des statistiques
num_posts = len(data)
average_length = total_length / num_posts
median_length = statistics.median(len(post['postText']) for post in data)
average_links = total_links / num_posts
median_links = statistics.median(len(url_pattern.findall(post['postText'])) for post in data)
average_emojis = total_emojis / num_posts
median_emojis = statistics.median(len(emoji_pattern.findall(post['postText'])) for post in data)
average_posts_per_author = statistics.mean(author_post_count.values())
median_posts_per_author = statistics.median(author_post_count.values())

# Résultats
print("Nombre d'auteurs différents :", len(authors))
print("Longueur moyenne des posts :", average_length, "Médiane :", median_length)
print("Nombre moyen de liens par post :", average_links, "Médiane :", median_links)
print("Nombre moyen d'emojis par post :", average_emojis, "Médiane :", median_emojis)
print("Nombre moyen de posts par auteur :", average_posts_per_author, "Médiane :", median_posts_per_author)


# Comptage des auteurs
author_counts = Counter(post['postAuthor'] for post in data)

# Comptage des mots (en excluant les URLs)
word_pattern = re.compile(r'\b\w+\b')
word_counts = Counter(word.lower() for post in data for word in word_pattern.findall(post['postText']) if not url_pattern.match(word))

# Comptage des hashtags
hashtag_pattern = re.compile(r'#\w+')
hashtag_counts = Counter(hashtag for post in data for hashtag in hashtag_pattern.findall(post['postText']))

# Affichage des résultats additionnels
print("\nAuteurs les plus actifs :")
for author, count in author_counts.most_common(20):
    print(f"{author}: {count} posts")

print("\nMots les plus fréquents :")
for word, count in word_counts.most_common(50):
    print(f"{word}: {count}")



# Compter les auteurs ayant posté une seule fois ou deux fois
single_posts_authors = sum(1 for count in author_post_count.values() if count == 1)
double_posts_authors = sum(1 for count in author_post_count.values() if count == 2)
triple_posts_authors = sum(1 for count in author_post_count.values() if count == 3)
four_posts_authors = sum(1 for count in author_post_count.values() if count == 4)
five_posts_authors = sum(1 for count in author_post_count.values() if count == 5)


print("Nombre d'auteurs ayant posté une seule fois :", single_posts_authors)
print("Nombre d'auteurs ayant posté deux fois :", double_posts_authors)
print("Nombre d'auteurs ayant posté trois fois :", triple_posts_authors)
print("Nombre d'auteurs ayant posté quatres fois :", four_posts_authors)
print("Nombre d'auteurs ayant posté cinq fois :", five_posts_authors)

# Tri des auteurs par nombre de posts décroissant
sorted_author_post_count = {author: count for author, count in sorted(author_post_count.items(), key=lambda item: item[1], reverse=True)}

# Visualisation de la distribution des posts par auteur
plt.figure(figsize=(10, 6))
plt.bar(sorted_author_post_count.keys(), sorted_author_post_count.values(), color='skyblue')
plt.xlabel('Auteurs')
plt.ylabel('Nombre de posts')
plt.title('Distribution des posts par auteur')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()



# Collecte des données individuelles pour chaque post
lengths = [len(post['postText']) for post in data]
links_count = [len(url_pattern.findall(post['postText'])) for post in data]
emojis_count = [len(emoji_pattern.findall(post['postText'])) for post in data]

# Histogramme pour la longueur des posts
plt.figure(figsize=(10, 5))
plt.hist(lengths, bins=30, color='blue', alpha=0.7)
plt.axvline(average_length, color='r', linestyle='dashed', linewidth=1, label=f'Moyenne: {average_length:.2f}')
plt.axvline(median_length, color='g', linestyle='dashed', linewidth=1, label=f'Médiane: {median_length:.2f}')
plt.title('Distribution de la Longueur des Posts')
plt.xlabel('Longueur des Posts')
plt.ylabel('Fréquence')
plt.legend()
plt.show()

# Histogramme pour le nombre de liens
plt.figure(figsize=(10, 5))
plt.hist(links_count, bins=range(max(links_count)+2), color='orange', alpha=0.7)
plt.axvline(average_links, color='r', linestyle='dashed', linewidth=1, label=f'Moyenne: {average_links:.2f}')
plt.axvline(median_links, color='g', linestyle='dashed', linewidth=1, label=f'Médiane: {median_links:.2f}')
plt.title('Distribution du Nombre de Liens par Post')
plt.xlabel('Nombre de Liens')
plt.ylabel('Fréquence')
plt.legend()
plt.show()

# Histogramme pour le nombre d'emojis
plt.figure(figsize=(10, 5))
plt.hist(emojis_count, bins=range(max(emojis_count)+2), color='purple', alpha=0.7)
plt.axvline(average_emojis, color='r', linestyle='dashed', linewidth=1, label=f'Moyenne: {average_emojis:.2f}')
plt.axvline(median_emojis, color='g', linestyle='dashed', linewidth=1, label=f'Médiane: {median_emojis:.2f}')
plt.title('Distribution du Nombre d\'Emojis par Post')
plt.xlabel('Nombre d\'Emojis')
plt.ylabel('Fréquence')
plt.legend()
plt.show()

# Histogramme pour le nombre de posts par auteur
plt.figure(figsize=(10, 5))
plt.hist(author_post_count.values(), bins=range(max(author_post_count.values())+2), color='green', alpha=0.7)
plt.axvline(average_posts_per_author, color='r', linestyle='dashed', linewidth=1, label=f'Moyenne: {average_posts_per_author:.2f}')
plt.axvline(median_posts_per_author, color='g', linestyle='dashed', linewidth=1, label=f'Médiane: {median_posts_per_author:.2f}')
plt.title('Distribution du Nombre de Posts par Auteur')
plt.xlabel('Nombre de Posts')
plt.ylabel('Fréquence')
plt.legend()
plt.show()
