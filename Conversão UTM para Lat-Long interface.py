###Conversão UTM para Lat-Long interface Gráfica
 
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import pyproj
import chardet

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(tk.END, file_path)

def convert_coordinates():
    file_path = entry_path.get()
    
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    
    df = pd.read_csv(file_path, sep=';', encoding=encoding)
    
    for fuso in df['FUSO'].unique():
        df_fuso = df[df['FUSO'] == fuso]
        utm = pyproj.Proj(proj='utm', zone=fuso, utmzone=df_fuso['ZONA'], ellps='WGS84', south=True)
        lat_long = pyproj.Proj(proj='latlong', datum='WGS84')
        lon, lat = pyproj.transform(utm, lat_long, df_fuso['E'], df_fuso['N'])
        df.loc[df['FUSO'] == fuso, 'Latitude'] = lat
        df.loc[df['FUSO'] == fuso, 'Longitude'] = lon
    
    save_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
    if save_path:
        df.to_csv(save_path, sep=';', index=False, decimal=',')
        lbl_status.config(text='Dados convertidos e salvos com sucesso!')

# Cria a janela principal
window = tk.Tk()
window.title('Conversão de Coordenadas')
window.geometry('400x200')

# Cria os componentes da interface
lbl_path = tk.Label(window, text='Caminho do arquivo CSV:')
lbl_path.pack()

entry_path = tk.Entry(window, width=40)
entry_path.pack()

btn_browse = tk.Button(window, text='Procurar', command=browse_file)
btn_browse.pack()

btn_convert = tk.Button(window, text='Converter', command=convert_coordinates)
btn_convert.pack()

lbl_status = tk.Label(window, text='')
lbl_status.pack()

# Inicia o loop principal da interface gráfica
window.mainloop()
