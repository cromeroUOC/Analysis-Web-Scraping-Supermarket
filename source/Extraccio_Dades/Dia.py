import builtwith
import whois
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import re
from datetime import datetime

# Creació de un DataFrame per guardar els productes
# df_productos_dia = pd.DataFrame(columns=['Nombre', 'Marca', 'Precio', 'Supermercado', 'URL'])

# Url de Dia
# url_superMerca = 'https://www.supermercadosmas.com/'
# url_superMerca_map = 'https://www.dia.es/sitemap.xml'

# Funció per obtenir les dades d'un producte de Dia
def datosProducto(urlProducto,df_productos):
    # Desactivar advertencias de SSL
    urllib3.disable_warnings()
    # Realitzar la petició GET
    http = urllib3.PoolManager()
    response = http.request('GET', urlProducto)
    soup = BeautifulSoup(response.data, 'html.parser')

    now = datetime.now()  # Captura la fecha y hora actuales
    fecha = now.strftime("%Y-%m-%d")
    hora = now.strftime("%H:%M:%S")

    #Try per si no troba el producte a la pàgina
    try:
        #Troba l'element que conté el preu del producte
        precio_elemento = soup.find('p', class_='buy-box__active-price')
        if precio_elemento:
            # Extreu el preu del text i el formateja
            precio = precio_elemento.text.strip().replace('\xa0€', ' €').replace(',', '.')
        else:
            precio = 'Precio no disponible'

        # Troba l'element que conté el nom del producte
        nombre_elemento = soup.find('h1', class_='product-title')
        if nombre_elemento:
            nombre = nombre_elemento.text.strip()
        else:
            nombre = 'Nombre no disponible'

        # Troba l'element que conté la marca del producte
        marca_elemento = soup.find('p', class_='manufacturer-info__name')
        if marca_elemento:
            marca = marca_elemento.text.strip()
        else:
            marca = 'Marca no disponible'

        precio_unidad_elemento = soup.find('p', class_='buy-box__price-per-unit')
        if precio_unidad_elemento:
            precio_unidad_texto = precio_unidad_elemento.text.strip(' ()')  # Elimina espacios y paréntesis
            precio_unidad = precio_unidad_texto.split('/')[0].strip()
            unidad = precio_unidad_texto.split('/')[1].strip()
        else:
            precio_unidad = 'Precio por unidad no disponible'
            unidad = 'Unidad no disponible'
        
        # Extracción de categoría y subcategoría de los breadcrumbs
        breadcrumbs = soup.find_all('a', {'data-test-id': 'breadcrumb-item'})
        if breadcrumbs:
            categoria = breadcrumbs[-2].find('span', {'data-test-id': 'breadcrumb-item-title'}).text if len(breadcrumbs) > 1 else ''
            subcategoria = breadcrumbs[-1].find('span', {'data-test-id': 'breadcrumb-item-title'}).text
        else:
            categoria = 'Categoría no disponible'
            subcategoria = 'Subcategoría no disponible'

        # Extracción del texto del botón sin verificar el estado
        estado_elemento = soup.find('button', {'data-test-id': 'add2cart-basic-button'})
        estado = estado_elemento.text.strip() if estado_elemento else 'Estado no disponible'

        # Afegir les dades al DataFrame
        # df_productos.loc[len(df_productos)] = [nombre, marca, precio, 'Dia', urlProducto]
        # print('Producto:', nombre, 'Marca:', marca, 'Precio:', precio)
        df_productos.loc[len(df_productos)] = [
            nombre, marca, precio, 'Dia', urlProducto, fecha, hora, 
            unidad, precio_unidad, categoria, subcategoria, estado
        ]
        print('Producto:', nombre, 'Marca:', marca, 'Precio:', precio, 'Unidad:', unidad, 'Precio por Unidad:', precio_unidad, 'Estado:', estado)
    except AttributeError:
        print('Error en producto:', urlProducto)

# Funció per obtenir les dades dels productes de Dia
def crawl_sitemap_Dia(url,df_productos):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    
    if response.status == 200:
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Obtenir totes les URL del sitemap
        urls = soup.find_all('url')
        
        for url in urls:
            loc = url.find('loc').text 
            datosProducto(loc,df_productos) 
    else:
        print("Failed to fetch sitemap:", response.status)


# if __name__ == '__main__':
#     crawl_sitemap(url_superMerca_map,df_productos_dia)

#     # Guardar los datos en un archivo CSV
#     df_productos.to_csv('productos_supermercadosmas.csv', index=False)