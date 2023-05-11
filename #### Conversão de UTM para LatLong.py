import pandas as pd
import pyproj
import chardet

# Detectar a codificação do arquivo CSV
with open('C:/Users/luish/OneDrive/Desktop/inventario/Resultados Paraná/IFN-PR_unidades_amostrais_04-11-2020.csv', 'rb') as f:
    result = chardet.detect(f.read())
encoding = result['encoding']

# Ler o arquivo CSV com a codificação detectada
df = pd.read_csv('C:/Users/luish/OneDrive/Desktop/inventario/Resultados Paraná/IFN-PR_unidades_amostrais_04-11-2020.csv', sep=';', encoding=encoding)

# Para cada fuso UTM único no DataFrame
for fuso in df['FUSO'].unique():
    # Filtrar o DataFrame para o fuso atual
    df_fuso = df[df['FUSO'] == fuso]

    # Definir os sistemas de coordenadas de origem (UTM) e de destino (lat/long)
    utm = pyproj.Proj(proj='utm', zone=fuso, utmzone=df_fuso['ZONA'], ellps='WGS84', south=True)
    lat_long = pyproj.Proj(proj='latlong', datum='WGS84')

    # Converter as coordenadas UTM para lat/long
    lon, lat = pyproj.transform(utm, lat_long, df_fuso['E'], df_fuso['N'])

    # Adicionar as novas colunas de Latitude e Longitude no DataFrame para o fuso atual
    df.loc[df['FUSO'] == fuso, 'Latitude'] = lat
    df.loc[df['FUSO'] == fuso, 'Longitude'] = lon

# Salvar os dados de saída em um novo arquivo CSV
df.to_csv('C:/Users/luish/OneDrive/Desktop/inventario/Resultados Paraná/IFN-PR_unidades_amostrais_04-11-2020_dados_convertidos.csv', sep=';', index=False, decimal=',')

# Imprimir os cabeçalhos do arquivo convertido
print(df.head())