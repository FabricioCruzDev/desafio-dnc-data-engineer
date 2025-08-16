import pandas as pd
import numpy as np
import os
from datetime import date

def load_data(path):
    print('Carregando dataset')
    df_bronze = pd.read_parquet(path, engine='pyarrow')
    df_bronze.head(10)
    df_bronze.info()
    return df_bronze

def clean (df_bronze):
    print("Convertendo o tipo data")
    df_bronze['date_of_birth'] = pd.to_datetime(df_bronze['date_of_birth'])
    
    print("Dados nulos")
    df_bronze = df_bronze.dropna(axis=0, subset=['name', 'email', 'date_of_birth', 'signup_date'])
    
    print("Corrigindo e-mails")
    df_bronze['email'].loc[~df_bronze['email'].str.contains('@')] = df_bronze['email'].loc[~df_bronze['email'].str.contains('@')].apply(lambda x : str(x).replace('example.com', '@example.com'))
    df_bronze['email'].loc[~df_bronze['email'].str.contains('@')] = df_bronze['email'].loc[~df_bronze['email'].str.contains('@')].apply(lambda x : str(x).replace('example.net', '@example.net'))
    df_bronze['email'].loc[~df_bronze['email'].str.contains('@')] = df_bronze['email'].loc[~df_bronze['email'].str.contains('@')].apply(lambda x : str(x).replace('example.org', '@example.org'))
    
    print(
        f'Dados nulos: {df_bronze.isna().sum()}\n'
        #f'E-mails inválidos: {df_bronze['email'].loc[~df_bronze['email'].str.contains('@')].count()}\n'    
    )
    return df_bronze

def calculate (df_clean):
    print("Incluindo cálculos")
    today = date.today()
    df_clean['age'] = np.floor((pd.Timestamp(today) - df_clean['date_of_birth']).dt.days / 365.25)
    print(df_clean.head(5))
    print(df_clean.info())
    return df_clean

def load (df_silver):
    print("Salvando o dataset na pasta silver no formato parquet")
    output_dir = './dw/silver'
    output_file = os.path.join(output_dir, 'silver_data.parquet')
    #os.makedirs(output_dir, exist_ok=True)
    df_silver.to_parquet(output_file, engine='pyarrow')
    print('Arquivo salvo com sucesso na pasta Silver')

def process_bronze_to_silver():
    df_bronze = load_data('./dw/bronze')
    df_clean = clean(df_bronze)
    df_silver = calculate(df_clean)
    load(df_silver)
