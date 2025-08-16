import pandas as pd
import numpy as np
import os
from datetime import date

def load_data(path):
    print("Carregando o dataset")
    df = pd.read_parquet(path, engine='pyarrow')
    print(df.head(10))
    print(df.info())
    print('Dataset carregado com sucesso')
    return df

def insert_column_age_group (df):
    print('Separando as faixas etárias')
    bins = [0, 10, 20, 30, 40, 50, 60, 100]
    labels = ['0 a 10', '11 a 20', '21 a 30', '31 a 40', '41 a 50', '51 a 60', '60 +']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)
    return df

def agg_age_status (df):
    print("Criando um novo dataset com a contagem de usuários ativos e intivos por faixa etária.")
    user_count_by_group = df.groupby(['age_group', 'subscription_status']).size()
    df_user_count = pd.DataFrame(user_count_by_group, columns=['count']).reset_index()
    df_user_count = df_user_count.loc[df_user_count['count'] > 0].copy()
    print(df_user_count)
    return df_user_count


def upload_parquet (df_gold):
    print("Salvando o dataset na pasta gold no formato parquet")
    output_dir = './dw/gold'
    output_file = os.path.join(output_dir, 'gold_data.parquet')
    
    df_gold.to_parquet(output_file, engine='pyarrow')
    print('Arquivo salvo com sucesso na pasta Gold')

def upload_csv (user_count):
    print("Salvando o data set unser_count na pasta gold no formato csv")
    output_dir = './dw/gold'
    output_file = os.path.join(output_dir, 'user_count.csv')

    user_count.to_csv(output_file, sep=';', encoding='UTF-8', index='False')
    print('Arquivo salvo com sucesso na pasta Gold')

def process_silver_to_gold():
   df = load_data('./dw/silver')
   df = insert_column_age_group(df)

   print(df['subscription_status'].unique())
   print(df['age_group'].unique())

   df_user_count = agg_age_status(df)

   upload_parquet(df)
   upload_csv(df_user_count)