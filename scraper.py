import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Function that extract elements from attribute data-oid
def extract_element_oid(soup, oid, tdchild=2):
    item = soup.select_one(f"tr[data-oid='{oid}'] > td:nth-child({tdchild})")
    if item:
        item_text = item.text.strip().replace("'", '')
        if '.' in item_text:
            item_text = item_text.replace('.', '')
            item = int(item_text)
        elif ',' in item_text:
            item_text = item_text.replace(',', '.')
            item = float(item_text)
        else:
            try:
                item = float(item_text)
            except ValueError:
                item = None
    else:
        item = None
    return item


def createdf_and_save(table_all, table_lt, table_lm, filename):
    # Create DataFrames
    df_all = pd.DataFrame(table_all)
    df_lt = pd.DataFrame(table_lt)
    df_lm = pd.DataFrame(table_lm)

    if filename is not None:
        # Save DataFrame
        with pd.ExcelWriter(filename) as writer:
            df_all.to_excel(writer, sheet_name='Tutti', index=False)
            df_lt.to_excel(writer, sheet_name='Triennale', index=False)
            df_lm.to_excel(writer, sheet_name='Magistrale', index=False)
        print(f"Results exported in {filename}.")
    return [df_all, df_lt, df_lm]


def row_constructor(soup, anno, tdchild, **kwargs):
    row = {
        "Anno": anno,
        **kwargs,
        "Numero laureati": extract_element_oid(soup, 1, tdchild),
        "Numero questionari": extract_element_oid(soup, 206, tdchild),
        "Tasso di compilazione": extract_element_oid(soup, 345, tdchild),
        "Almeno un genitore laureato": extract_element_oid(soup, 362, tdchild),
        "Entrambi con laurea": extract_element_oid(soup, 18, tdchild),
        "Uno solo con laurea": extract_element_oid(soup, 19, tdchild),
        "Nessun genitore laureato": extract_element_oid(soup, 363, tdchild),
        "Diploma di scuola secondaria di secondo grado": extract_element_oid(soup, 387, tdchild),
        "Qualifica professionale, titolo inferiore o nessun titolo": extract_element_oid(soup, 388, tdchild)
    }
    return row


def row_constructor_gender(soup, anno, tdchild, genere):
    row = {
        "Anno": anno,
        "Genere": genere,
        "Numero laureati": extract_element_oid(soup, 1, tdchild),
        "Numero questionari": extract_element_oid(soup, 206, tdchild),
        "Tasso di compilazione": extract_element_oid(soup, 345, tdchild),
        "Almeno un genitore laureato": extract_element_oid(soup, 362, tdchild),
        "Entrambi con laurea": extract_element_oid(soup, 18, tdchild),
        "Uno solo con laurea": extract_element_oid(soup, 19, tdchild),
        "Nessun genitore laureato": extract_element_oid(soup, 363, tdchild),
        "Diploma di scuola secondaria di secondo grado": extract_element_oid(soup, 387, tdchild),
        "Qualifica professionale, titolo inferiore o nessun titolo": extract_element_oid(soup, 388, tdchild)
    }
    return row


def disaggregation_all(anni, filename=None, ateneo="tutti"):
    print("disaggregazione: tutti")
    table_all = []
    table_lt = []
    table_lm = []
    for anno in tqdm(anni):
        # print("anno: ", anno)
        url = f"https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno={anno}&corstipo=tutti&ateneo={ateneo}&facolta=tutti&gruppo=tutti&livello=tutti&area4=tutti&classe=tutti&postcorso=tutti&isstella=0&presiui=tutti&disaggregazione=livello&LANG=it&CONFIG=profilo"
        # prepare the soup
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        # extract data
        row_all = row_constructor(soup, anno, 2)
        row_lt = row_constructor(soup, anno, 3)
        row_lm = row_constructor(soup, anno, 4)
        # append data
        table_all.append(row_all)
        table_lt.append(row_lt)
        table_lm.append(row_lm)
    df_all, df_lt, df_lm = createdf_and_save(table_all, table_lt, table_lm, filename)
    return [df_all, df_lt, df_lm]


def disaggregazione_genere(anni, filename=None, ateneo="tutti"):
    print("disaggregazione: genere")
    table_all = []
    table_lt = []
    table_lm = []
    livelli = ["tutti", 1, 2]

    for anno in tqdm(anni):
        # print("anno: ", anno)
        for livello in tqdm(livelli, leave=False):
            # print("livello: ", livello)
            url = f"https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno={anno}&corstipo=tutti&ateneo={ateneo}&facolta=tutti&gruppo=tutti&livello={livello}&area4=tutti&classe=tutti&postcorso=tutti&isstella=0&presiui=tutti&disaggregazione=genere&LANG=it&CONFIG=profilo"
            # prepare the soup
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            # extract data
            row_uomini = row_constructor(soup, anno, 3, **{"Genere": "uomini"})
            row_donne = row_constructor(soup, anno, 4, **{"Genere": "donne"})
            # append data
            if livello == "tutti":
                table_all.append(row_uomini)
                table_all.append(row_donne)
            elif livello == 1:
                table_lt.append(row_uomini)
                table_lt.append(row_donne)
            elif livello == 2:
                table_lm.append(row_uomini)
                table_lm.append(row_donne)
    df_all, df_lt, df_lm = createdf_and_save(table_all, table_lt, table_lm, filename)
    return [df_all, df_lt, df_lm]


def disaggregazione_dipartimenti(anni, filename=None, ateneo='tutti'):
    print("disaggregazione: dipartimenti")
    table_all = []
    table_lt = []
    table_lm = []
    livelli = ["tutti", 1, 2]

    for anno in tqdm(anni):
        # print("anno: ", anno)
        for livello in tqdm(livelli, leave=False):
            table = []
            # print("livello: ", livello)
            url = f"https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno={anno}&corstipo=tutti&ateneo={ateneo}&facolta=tutti&gruppo=tutti&livello={livello}&area4=tutti&classe=tutti&postcorso=tutti&isstella=0&presiui=tutti&disaggregazione=facolta&LANG=it&CONFIG=profilo"
            # prepare the soup
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            # extract data
            if anno >= 2013:
                table.append(row_constructor(soup, anno, 3, **{"Dipartimento": "DAD"}))
                table.append(row_constructor(soup, anno, 4, **{"Dipartimento": "DAUIN"}))
                table.append(row_constructor(soup, anno, 5, **{"Dipartimento": "DET"}))
                table.append(row_constructor(soup, anno, 6, **{"Dipartimento": "DENERG"}))
                table.append(row_constructor(soup, anno, 7, **{"Dipartimento": "DIATI"}))
                table.append(row_constructor(soup, anno, 8, **{"Dipartimento": "DIGEP"}))
                table.append(row_constructor(soup, anno, 9, **{"Dipartimento": "DIMEAS"}))
                table.append(row_constructor(soup, anno, 10, **{"Dipartimento": "DISEG"}))
                table.append(row_constructor(soup, anno, 11, **{"Dipartimento": "DIST"}))
                table.append(row_constructor(soup, anno, 12, **{"Dipartimento": "DISAT"}))
                table.append(row_constructor(soup, anno, 13, **{"Dipartimento": "DISMA"}))
            elif anno >= 2010:
                table.append(row_constructor(soup, anno, 3, **{"Dipartimento": "Architettura 1"}))
                table.append(row_constructor(soup, anno, 4, **{"Dipartimento": "Architettura 2"}))
                table.append(row_constructor(soup, anno, 5, **{"Dipartimento": "Ingegneria 1"}))
                table.append(row_constructor(soup, anno, 6, **{"Dipartimento": "Ingegneria 3"}))
                table.append(row_constructor(soup, anno, 7, **{"Dipartimento": "Ingegneria 4"}))
            elif anno >= 2004:
                table.append(row_constructor(soup, anno, 3, **{"Dipartimento": "Architettura 1"}))
                table.append(row_constructor(soup, anno, 4, **{"Dipartimento": "Architettura 2"}))
                table.append(row_constructor(soup, anno, 5, **{"Dipartimento": "Ingegneria 1"}))
                table.append(row_constructor(soup, anno, 5, **{"Dipartimento": "Ingegneria 2"}))
                table.append(row_constructor(soup, anno, 6, **{"Dipartimento": "Ingegneria 3"}))
                table.append(row_constructor(soup, anno, 7, **{"Dipartimento": "Ingegneria 4"}))
            else:
                raise ValueError("Anno antecedente al 2004.")
            # append data
            if livello == "tutti":
                table_all.extend(table)
            elif livello == 1:
                table_lt.extend(table)
            elif livello == 2:
                table_lm.extend(table)
    df_all, df_lt, df_lm = createdf_and_save(table_all, table_lt, table_lm, filename)
    return [df_all, df_lt, df_lm]

def disaggregazione_lavoro(anni, filename=None, ateneo='tutti'):
    print("disaggregazione: lavoro")
    table_all = []
    table_lt = []
    table_lm = []
    livelli = ["tutti", 1, 2]

    for anno in tqdm(anni):
        # print("anno: ", anno)
        for livello in tqdm(livelli, leave=False):
            table = []
            # print("livello: ", livello)
            url = f"https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno={anno}&corstipo=tutti&ateneo={ateneo}&facolta=tutti&gruppo=tutti&livello={livello}&area4=tutti&classe=tutti&postcorso=tutti&isstella=0&presiui=tutti&disaggregazione=condlav&LANG=it&CONFIG=profilo"
            # prepare the soup
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            # extract data
            table.append(row_constructor(soup, anno, 3, **{"Lavoro": "lavoratori-studenti"}))
            table.append(row_constructor(soup, anno, 4, **{"Lavoro": "studenti-lavoratori"}))
            table.append(row_constructor(soup, anno, 5, **{"Lavoro": "nessuno"}))
            # append data
            if livello == "tutti":
                table_all.extend(table)
            elif livello == 1:
                table_lt.extend(table)
            elif livello == 2:
                table_lm.extend(table)
    df_all, df_lt, df_lm = createdf_and_save(table_all, table_lt, table_lm, filename)
    return [df_all, df_lt, df_lm]


anni = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,
        2022]

print("Start scraping...")

disaggregation_all(anni, 'results/disaggregazione_tutti.xlsx', ateneo="70032")
print("disaggregazione_tutti completata")
disaggregation_all(anni, 'results/disaggregazione_tutti_nazionale.xlsx', ateneo="tutti")
print("disaggregazione_tutti_nazionale completata")
disaggregazione_genere(anni, 'results/disaggregazione_genere.xlsx', ateneo="70032")
print("disaggregazione_genere completata")
disaggregazione_dipartimenti(anni, 'results/disaggregazione_dipartimenti.xlsx', ateneo="70032")
print("disaggregazione_dipartimenti completata")
disaggregazione_lavoro(anni, 'results/disaggregazione_lavoro.xlsx', ateneo="70032")
print("disaggregazione_lavoro completata")

