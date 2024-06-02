import builtwith
import whois
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

# Crear un DataFrame para guardar los productos, variable global para poder acceder a ella desde las funciones
# df_productos = pd.DataFrame(columns=['Nombre', 'Marca', 'Precio', 'Supermercado', 'URL'])

# Para conocer el tipo de tecnologia con la que se creó la web
# builtwith.parse('https://www.supermercadosmas.com/')

# Identificar propietario de la web
# print(whois.whois('https://www.supermercadosmas.com/'))

# Función para obtener los datos de un producto
def datosProducto(urlProducto,df_productos):
    # Desactiva los warnings de certificados SSL
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    response = http.request('GET', urlProducto)
    soup = BeautifulSoup(response.data, 'html.parser')

    #Try para evitar errores en la ejecución, algunas url no tienen ya productos
    try:
        # Encuentra el precio y la referencia/nombre del producto
        precio_wrapper = soup.find('span', {'class': 'price-wrapper'})
        #precio con clase price
        precio = precio_wrapper.find('span', {'class': 'price'}).text.strip()
        #nombre con itemprop name
        nombre = soup.find('span', {'itemprop': 'name'}).text.strip()
        # #marca con clase product-item-attribute-brand
        brand_element = soup.find('p', {'class': 'product-item-attribute-brand'})
        if brand_element:
            marca = brand_element.text.strip()
        else:
            marca = 'No disponible'

        # # Añadir a la lista de productos
        df_productos.loc[len(df_productos)] = [nombre, marca, precio, 'Supermercados Mas', urlProducto]
        print('Producto:', nombre, 'Marca:', marca, 'Precio:', precio)
    except AttributeError:
        print('Error en producto:', urlProducto)

# Función para sacar las urls de todos los artículos del supermercado
def crawl_sitemap_SupermercadosMas(url,df_productos):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    
    # Comprobar si el request es correcto (200)
    if response.status == 200:
        soup = BeautifulSoup(response.data, 'html.parser')
        # Encontrar todos los tags url
        urls = soup.find_all('url')
        # Extraer todas las urls con priority 1.0 (son los artículos)
        for url in urls:
            priority = url.find('priority')
            if priority and priority.text == '1.0':
                loc = url.find('loc').text
                print(loc)
                datosProducto(loc,df_productos)
    else:
        print("Failed to fetch sitemap:", response.status)


# crawl_sitemap("https://www.supermercadosmas.com/pub/media/sitemap-1-1.xml")
# crawl_sitemap("https://www.supermercadosmas.com/pub/media/sitemap-1-2.xml")

# #Descargar los precios de los productos en excel
# df_productos.to_excel('productos_supermercados_mas.xlsx', index=False)

