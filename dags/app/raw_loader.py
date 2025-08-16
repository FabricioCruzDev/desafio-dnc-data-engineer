import pandas as pd
import os

   
def upload_raw_data_to_bronze():
    df_bronze = pd.read_csv('./raw/raw_data.csv', sep=',', encoding='UTF-8', index_col='id')
    print(df_bronze.sample(10))
    df_bronze.info()
    
    print("Salvando o dataset na pasta bronze no formato parquet")
    output_dir = './dw/bronze'
    output_file = os.path.join(output_dir, 'bronze_data.parquet')

    os.makedirs(output_dir, exist_ok=True)

    df_bronze.to_parquet(output_file, engine='pyarrow')


