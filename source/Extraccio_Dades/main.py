
import pandas as pd
from Consum import crawl_sitemap_Consum
from Dia import crawl_sitemap_Dia
from Supermercadosmas import crawl_sitemap_SupermercadosMas

#Definició de les urls
url_consum = 'https://tienda.consum.es'
url_consum_map = 'https://tienda.consum.es/sitemap_product_es.xml'

url_Dia = 'https://www.supermercadosmas.com/'
url_Dia_map = 'https://www.dia.es/sitemap.xml'

url_SupermercadosMas_1 = 'https://www.supermercadosmas.com/pub/media/sitemap-1-1.xml'
url_SupermercadosMas_2 = 'https://www.supermercadosmas.com/pub/media/sitemap-1-2.xml'

# Funció principal
def main():
    #Revisar si el archiu existeix
    try:
        # Llegir el fitxer csv
        df_productos = pd.read_csv('../dataset/productos.csv')
        # Eliminem les dades anteriors
        df_productos.drop(df_productos.index, inplace=True)
    except:
        # Creació de un DataFrame per guardar els productes
        df_productos = pd.DataFrame(columns=['Nombre', 'Marca', 'Precio', 'Supermercado', 'URL'])

    # Cridar a les funcions per obtenir les dades
    try:
        crawl_sitemap_Consum(url_consum_map, df_productos)
    except:
        print('Error en Consum')
        df_productos.to_csv('productos.csv', index=False)
    try:    
        crawl_sitemap_SupermercadosMas(url_SupermercadosMas_1, df_productos)
        crawl_sitemap_SupermercadosMas(url_SupermercadosMas_2, df_productos)
    except:
        print('Error en SupermercadosMas')
        df_productos.to_csv('productos.csv', index=False)
    try:
        crawl_sitemap_Dia(url_Dia_map, df_productos)
    except:
        print('Error en Dia')
        df_productos.to_csv('productos.csv', index=False)
        
    try:
        # Guardar el DataFrame en un archiu csv
        df_productos.to_csv('productos.csv', index=False)
        # df_productos.to_csv('../dataset/productos.csv', index=False)
    except:
        print('Error al guardar el archivo csv')

# Executar la funció principal
if __name__ == "__main__":
    main()