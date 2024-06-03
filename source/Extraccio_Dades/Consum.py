import builtwith
import whois
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime  

#Url de Consum
# url_consum = 'https://tienda.consum.es'
# url_consum_map = 'https://tienda.consum.es/sitemap_product_es.xml'

# Creació de un DataFrame per guardar els productes
# df_productos_Consum = pd.DataFrame(columns=['Nombre', 'Marca', 'Precio', 'Supermercado', 'URL'])

# Funció per obtenir les dades d'un producte de Consum
def datosProducto(driver, df_productos, urlProducto):

    try:
        
        # Navega a la página
        driver.get(urlProducto)

        # Captura la fecha y hora actuales
        now = datetime.now()  # Obtiene el momento actual
        fecha = now.strftime("%Y-%m-%d")  # Formato de fecha YYYY-MM-DD
        hora = now.strftime("%H:%M:%S")  # Formato de hora HH:MM:SS

        # Espera fins que el preu sigui visible
        precio = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "infoproduct-content--price"))
        )
        # Espera fins que el nom sigui visible
        nombre = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "u-title-3"))
        )
        # Espera fins que la marca sigui visible
        marca = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "infoproduct-content--brand"))
        )
        
        precio_unidad_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "infoproduct-content--unitprice"))
        )

        # Procesar el texto del precio por unidad para extraer el precio y la unidad
        precio_unidad_texto = precio_unidad_element.text  # Ejemplo: "(1,35 € / 1 L)"
        precio_unidad = precio_unidad_texto.split('/')[0].strip('() ')  # Ejemplo: "1,35 €"
        unidad = precio_unidad_texto.split('/')[1].strip().strip(')')  # Ejemplo: "1 L", elimina el paréntesis derecho

        # Captura el texto del botón que indica si se puede añadir el producto
        estado_elemento = driver.find_element(By.CSS_SELECTOR, ".essential-unitselector__btn-add")
        estado = estado_elemento.text if estado_elemento else 'Estado no disponible'

        # Agrega les dades al DataFrame
        # df_productos.loc[len(df_productos)] = [nombre.text, marca.text, precio.text, 'Consum', urlProducto]
        df_productos.loc[len(df_productos)] = [
            nombre.text, marca.text, precio.text, 'Consum', urlProducto,
            fecha,  # Fecha de obtención
            hora,   # Hora de obtención
            unidad,  # Unidad de medida
            precio_unidad,  # Precio por unidad
            '', 
            '',
            estado
        ]
        print(df_productos)
    except Exception as e:
        # Si hi ha un error, mostra'l per pantalla
        print("Error al obtener los datos del producto:", e)
        driver.quit()
        driver = webdriver.Chrome(ChromeDriverManager().install())

# Funció per obtenir les dades dels productes de Consum
def crawl_sitemap_Consum(url, df_productos):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    
    if response.status == 200:
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Obtenir totes les URL del sitemap
        urls = soup.find_all('url')
        
        # Iniciar el navegador
        driver = webdriver.Chrome(ChromeDriverManager().install())

        # Recorre totes les URL del sitemap
        for url in urls:
            loc = url.find('loc').text 
            print(loc)
            datosProducto(driver, df_productos, loc) 

        # Tancar el navegador
        driver.quit()

    else:
        print("Failed to fetch sitemap:", response.status)


# if __name__ == '__main__':
#     crawl_sitemap(url_consum_map, df_productos_Consum)
#     #Cerrar el navegador
#     driver.quit()
#     # Guardar los datos en un archivo CSV
#     df_productos.to_csv('productos_supermercadosmas.csv', index=False)
