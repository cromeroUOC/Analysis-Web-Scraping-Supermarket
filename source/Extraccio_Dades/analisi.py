import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Càrrega del conjunt de dades des del fitxer CSV situat dins d'una carpeta 'dataset'.
df = pd.read_csv('dataset/productos.csv')

# Estructura bàsica de la informació del dataframe
df_info = {
    'columns': df.columns.tolist(),  # Llista les columnes del dataframe
    'head': df.head().to_dict(orient='records'),  # Mostra les primeres cinc entrades en format de diccionari
    'description': df.describe(include='all'),  # Genera estadístiques descriptives per a totes les columnes
    'shape': df.shape  # Mostra la forma del dataframe, és a dir, el nombre de files i columnes
}

df_info_2 = {
    'total_entries': df.shape[0],
    'unique_products': df['Nombre'].nunique(),
    'unique_brands': df['Marca'].nunique(),
    'supermarkets_involved': df['Supermercado'].nunique(),
    'most_common_supermarket': df['Supermercado'].mode()[0],
    'most_common_brand': df['Marca'].mode()[0] if not df['Marca'].isnull().all() else "No brands"
}

print(df_info_2)

# Imprimeix la forma del dataframe
print(f"El dataframe té {df_info['shape'][0]} files i {df_info['shape'][1]} columnes.")

# Imprimeix el nom de les columnes
print("Les columnes del dataframe són:", df_info['columns'])

# Imprimeix les primeres cinc files del dataframe
print("Les primeres cinc files del dataframe són:")
print(df.head())

# Imprimeix una descripció del dataframe, incloent informació com ara valors únics, freqüència dels valors més comuns, etc.
print("Descripció estadística del dataframe:")
print(df.describe(include='all'))

# Comptem el nombre d'entrades per supermercat
print("\nEntrades per supermercat:")
supermarket_counts = df['Supermercado'].value_counts()
print(supermarket_counts)

# Visualització del nombre de productes per supermercat
plt.figure(figsize=(10, 6))
sns.barplot(x=supermarket_counts.index, y=supermarket_counts.values)
plt.title('Nombre de Productes per Supermercat')
plt.xlabel('Supermercat')
plt.ylabel('Nombre de Productes')
plt.show()

# Filtrar les entrades on el nom del producte és 'Nombre no disponible'
df_filtered = df[df['Nombre'] != 'Nombre no disponible']

# Anàlisi de la diversitat de marques per supermercat
print("\nDiversitat de Marques per Supermercat:")
for supermarket in df_filtered['Supermercado'].unique():
    unique_brands = df_filtered[df_filtered['Supermercado'] == supermarket]['Marca'].nunique()
    print(f"{supermarket}: {unique_brands} marques úniques")

# Diversitat de productes
product_diversity = df_filtered['Nombre'].value_counts().head(10)
plt.figure(figsize=(12, 8))
product_diversity.plot(kind='barh', color='skyblue')
plt.title('Top 10 Productes més Freqüents')
plt.xlabel('Freqüència')
plt.ylabel('Producte')
plt.gca().invert_yaxis()  # Inverteix l'eix y per mostrar el més freqüent a la part superior
plt.show()