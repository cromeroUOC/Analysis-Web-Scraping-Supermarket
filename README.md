# Web-Scraping-Supermarket-Prices
## Pràctica 2 - Tipologia i cicle de vida de les dades 
### Màster U. en Ciència de Dades - UOC

### Integrants del grup.
- Carlos Romero Matarin
- Enric Sintes Arguimbau
### Estructura del repositori

Aquest repositori inclou els components principals següents:
- `dataset/`
  - `productos.csv` - El fitxer CSV que conté les dades dels productes.
- `source/`
  - `Extracio_Dades/`
    - `Consum.py`: Script de web scraping per a la botiga en línia de Consum.
    - `Dia.py`: Script per extracció de dades de la botiga en línia de DIA.
    - `Supermercadosmas.py`: Script per extracció de dades de Supermercados Más.
    - `main.py`: Fitxer principal que executa les funcions de scraping i desa els resultats.
    - `requirements.txt`: Un fitxer que llista totes les biblioteques necessàries per executar els scripts.
    - `analisi.py`: Fitxer que conté les funcions per a l'anàlisi de les dades.
  - `Practica 2.rmd`: Fitxer per a l'anàlisi de dades.
- `README.md`: Documentació del projecte.
- `.gitignore` - Especifica els fitxers intencionadament no seguïts per ignorar.

### Cómo utilizar el código de análisis
**Configuració inicial:**
Abans d'executar l'script d'anàlisi, assegureu-vos que totes les dependències estiguin instal·lades correctament. Si treballeu amb R, podreu instal·lar els paquets necessaris des del fitxer 'Practica 2.rmd'.

**Execució de l'anàlisi:**
Per executar l'anàlisi, obriu el fitxer `Practica 2.rmd` amb RStudio i executeu les cel·les consecutivament. Aquest fitxer inclou tot el codi necessari per realitzar la neteja, transformació i visualització de les dades dels supermercats.


### Cómo utilizar el código de extracción:
**Instalación de dependencias:**
Instal·leu les dependències amb la següent comanda:

```bash
pip install -r requirements.txt
```

**Executeu l'script principal:**
Executeu l'script principal amb la següent comanda:

```bash
python main.py
```

L'script `main.py` realitzarà el raspall de totes els supermercats configurats i guardarà les dades raspades a `productos.csv`.

**Paràmetres**
Els scripts no accepten paràmetres a través de la línia de comandes tal com estan estructurats actualment; totes les configuracions es realitzen dins dels fitxers de codi ells mateixos.

**Exemples**
Per raspar dades de tots els supermercats i compilar-les en un fitxer CSV:
    
    ```bash
    python main.py
    ```
Recordeu que aquesta comanda ha de ser executada des del directori `source/`.

### Llicència
Aquest projecte està llicenciat sota la llicència MIT. Consulteu el fitxer de llicència per obtenir més informació.
