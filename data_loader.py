import pandas as pd

class DataLoader:
    def __init__(self, csv_file):
        self.df = self.load_data(csv_file)

    def load_data(self, csv_file):
        # Cargar datos desde CSV a un DataFrame de Pandas
        df = pd.read_csv(csv_file)
        # Convertir la columna 'FECHA_REGISTRO' a tipo datetime si es necesario
        if 'FECHA_REGISTRO' in df.columns:
            df['FECHA_REGISTRO'] = pd.to_datetime(df['FECHA_REGISTRO'])
        return df

# Reemplaza 'inversiones.csv' con la ruta a tu archivo CSV
loader = DataLoader('data/inversiones.csv')

# DataFrame para el Panel de Resumen
#resumen_df = loader.df[['DEPARTAMENTO', 'FECHA_REGISTRO', 'MONTO_VIABLE', 'COSTO_ACTUALIZADO', 'SECTOR', 'ENTIDAD', 'AVANCE_FISICO']]
# DataFrame para el Panel de Resumen
resumen_df = loader.df[loader.df['DEPARTAMENTO'].notnull()][['DEPARTAMENTO', 'FECHA_REGISTRO', 'MONTO_VIABLE', 'COSTO_ACTUALIZADO', 'SECTOR', 'ENTIDAD', 'AVANCE_FISICO']]