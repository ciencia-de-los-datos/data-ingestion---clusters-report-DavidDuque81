"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd
import re


def ingest_data():
    df_raw = pd.read_fwf('./clusters_report.txt', skiprows=4,
            names = ['cluster','cantidad_de_palabras_clave','porcentaje_de_palabras_clave','principales_palabras_clave'])
    
    df_raw.fillna(method='ffill', inplace=True)
    df_raw1 = df_raw.groupby(['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave'])['principales_palabras_clave'].apply(' '.join).reset_index()
    
    percent = []
    for i in range(len(df_raw1)):
        a = df_raw1['porcentaje_de_palabras_clave'][i].replace(' %','').replace(',','.')
        percent.append(float(a))
    df_raw1['porcentaje_de_palabras_clave'] = percent
    df_raw1['cluster'] = df_raw1['cluster'].apply(lambda x: int(x))
    df_raw1['cantidad_de_palabras_clave'] = df_raw1['cantidad_de_palabras_clave'].apply(lambda x: int(x))
    
    key = {}
    for i in range(len(df_raw1)):
        key_words = df_raw1['principales_palabras_clave'][i].split('.')[0].split(',')
        key[i] = []
        for j in range(len(key_words)):
            key[i].append(re.sub('\s+', ' ', key_words[j].strip()))
    
    for i in key:
        key[i] = ", ".join(key[i])
        df_raw1.loc[i, 'principales_palabras_clave'] = key[i]
        
    df = df_raw1
    return df
