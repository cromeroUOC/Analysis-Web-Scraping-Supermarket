import builtwith
import whois
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from datetime import datetime  

# Crear un DataFrame para guardar los productos, variable global para poder acceder a ella desde las funciones
# df_productos = pd.DataFrame(columns=['Nombre', 'Marca', 'Precio', 'Supermercado', 'URL'])

# Para conocer el tipo de tecnologia con la que se creó la web
# builtwith.parse('https://www.supermercadosmas.com/')

# Identificar propietario de la web
# print(whois.whois('https://www.supermercadosmas.com/'))

# df_productos = pd.DataFrame(columns=['Nombre', 'Marca', 'Precio', 'Supermercado', 'URL', 'Fecha', 'Hora', 'unidad','precio_unidad', 'Categoria', 'Subcategoria', 'Estado'])

# url_SupermercadosMas= 'https://www.supermercadosmas.com/media/sitemap/sitemap.xml'

# Función para obtener los datos de un producto
def datosProducto(urlProducto,df_productos):
    # Desactiva los warnings de certificados SSL
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    response = http.request('GET', urlProducto)
    soup = BeautifulSoup(response.data, 'html.parser')

    # Obtener la fecha y hora actuales
    now = datetime.now()
    fecha = now.strftime("%Y-%m-%d")
    hora = now.strftime("%H:%M:%S")

    #Try para evitar errores en la ejecución, algunas url no tienen ya productos
    try:
        precio_meta_element = soup.find('meta', itemprop='price')
        precio = precio_meta_element['content'].strip() if precio_meta_element else 'Precio no disponible'

        #nombre con itemprop name
        nombre_element = soup.find('p', {'class': 'base title-font mb-0 xl:text-[2vw]'})
        nombre = nombre_element.text.strip() if nombre_element else 'Nombre no disponible'

        # #marca con clase product-item-attribute-brand
        marca_element = soup.find('div', {'class': 'my-1 flex text-xs text-grey-medium'}).find('span')
        marca = marca_element.text.strip() if marca_element else 'Marca no disponible'

        unidad_precio_unidad_element = soup.find('span', {'class': 'custom_field_3'})
        if unidad_precio_unidad_element:
            # Convertir el contenido interno a BeautifulSoup para poder parsearlo
            contenido_interno = BeautifulSoup(unidad_precio_unidad_element.text, 'html.parser')
            
            # Extraer la unidad
            div_unidad = contenido_interno.find('div')
            unidad = div_unidad.text.strip() if div_unidad else 'Unidad no disponible'
            
            # Extraer el precio por unidad
            span_precio_unidad = contenido_interno.find('span')
            precio_unidad = span_precio_unidad.text.strip() if span_precio_unidad else 'Precio por unidad no disponible'
        else:
            unidad = 'Unidad no disponible'
            precio_unidad = 'Precio por unidad no disponible'


        breadcrumbs = soup.find('ol', {'class': 'py-4 flex flex-wrap text-xs'})
        if breadcrumbs:
            links = breadcrumbs.find_all('a')
            if len(links) > 2:
                categoria = links[-2].text.strip()  # Penúltimo enlace como categoría
                subcategoria = links[-1].text.strip()  # Último enlace como subcategoría
            else:
                categoria = 'Categoría no disponible'
                subcategoria = 'Subcategoría no disponible'
        else:
            categoria = 'Categoría no disponible'
            subcategoria = 'Subcategoría no disponible'


        estado_elemento = soup.find('button', {'id': 'product-addtocart-button'})
        estado = estado_elemento.find('span').text.strip() if estado_elemento else 'Estado no disponible'

        # # Añadir a la lista de productos
        df_productos.loc[len(df_productos)] = [
            nombre, marca, precio, 'Supermercados Mas', urlProducto,
            fecha, hora, unidad, precio_unidad, categoria, subcategoria, estado
        ]
        print('Producto añadido:', nombre + ' Marca: ' + marca + ' Precio: ' + precio + ' Supermercado: Supermercados Mas' + ' URL: ' + urlProducto + ' Fecha: ' + fecha + ' Hora: ' + hora + ' Unidad: ' + unidad + ' Precio por unidad: ' + precio_unidad + ' Categoria: ' + categoria + ' Subcategoria: ' + subcategoria + ' Estado: ' + estado)
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


# crawl_sitemap_SupermercadosMas(url_SupermercadosMas,df_productos)
