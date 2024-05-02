import json

# Chargement des données JSON à partir d'un fichier
def load_json_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# Générer la requête SQL pour un sous-ensemble de données
def generate_sql_insert(data):
    base_sql = """insert into public.post (created_at, user_id, page_id, repost, circle_id, data, content, type) values """
    values_list = []
    
    for item in data:
        post_author = item['postAuthor'].replace("'", "''")  # Échappement des apostrophes dans SQL
        post_text = item['postText'].replace("'", "''")
        content_value = f"Posté par : {post_author}; contenu : {post_text}"
        sql_value = f"(now(), 'f43df1d6-232c-4bc5-99a3-dc79a438218e', 2, false, 2, '{{}}', '{content_value}', 0)"
        values_list.append(sql_value)
    
    full_sql = base_sql + ",\n  ".join(values_list) + ";"
    return full_sql

# Écriture de la requête SQL dans un fichier texte
def write_sql_to_file(sql_query, output_filepath):
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write(sql_query)

# Diviser les données en groupes de 50 éléments et générer des fichiers SQL
def split_data_and_generate_files(data, output_folder):
    chunk_size = 20  # Nombre d'éléments par fichier
    for i in range(0, len(data), chunk_size):
        chunk_data = data[i:i+chunk_size]
        sql_query = generate_sql_insert(chunk_data)
        output_filepath = f"{output_folder}/output_sql_query_part_{i//chunk_size + 1}.txt"
        write_sql_to_file(sql_query, output_filepath)
        print(f"La requête SQL pour le groupe {i//chunk_size + 1} a été écrite dans {output_filepath}")

# Utilisation des fonctions
if __name__ == "__main__":
    json_filepath = 'C:\\Users\\amaur\\Desktop\\Cours EMA\\2IA\\RetD\\scrapFacebookPost\\dataPosts.json'  # Chemin vers votre fichier JSON
    output_folder = 'C:\\Users\\amaur\\Desktop\\Cours EMA\\2IA\\RetD\\scrapFacebookPost\\sqlQuerries'  # Dossier de sortie pour les fichiers de requête SQL
    
    json_data = load_json_data(json_filepath)
    split_data_and_generate_files(json_data, output_folder)
