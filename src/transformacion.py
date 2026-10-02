import pandas as pd
import re

def limpiar_datos(df):
    df = df.drop_duplicates(subset=['ID'], keep='first').copy()
    df['Name'] = df['Name'].str.strip()
    
    def parsear_plata(v):
        v = str(v).replace('€', '').strip()
        if 'M' in v: return float(v.replace('M', '')) * 1000000
        if 'K' in v: return float(v.replace('K', '')) * 1000
        return 0.0
    
    df['Value_EUR'] = df['Value'].apply(parsear_plata)
    return df[['ID', 'Name', 'Value_EUR']]
