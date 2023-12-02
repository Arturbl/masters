import os
import pandas as pd


def process_csv():
    file_path = os.path.join(os.path.dirname(__file__), "../", "utils", "trainning.csv")
    df = pd.read_csv(file_path, sep=';')
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%y/%m/%d %H:%M:%S:%f')
    df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S:%f')
    df = df.drop(['date', 'time'], axis=1)
    df = df.sort_values(by='datetime')
    df.to_csv(file_path, index=False, sep=';')



if __name__ == '__main__':
    process_csv()
