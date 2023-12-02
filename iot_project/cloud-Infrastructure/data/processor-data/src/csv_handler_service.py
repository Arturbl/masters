import os
import pandas as pd
import db_handler_service as dbHandler


db_handler = dbHandler.DatabaseHandlerService()


def process_csv(file_path):
    try:
        df = pd.read_csv(file_path, sep=';')
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%y %H:%M:%S:%f')
        df['datetime'] = df['datetime'].dt.strftime('%d-%m-%Y %H:%M:%S')
        df = df.drop(['date', 'time'], axis=1)
        df = df.sort_values(by='datetime')
        df.to_csv(file_path, index=False, sep=';')
        print("Csv processed")
    except:
        print("Csv is already processed")


def insert_training_data(file_path):
    data_frame = pd.read_csv(file_path, sep=';')
    db_handler.save_data_frame(data_frame)


def main():
    file_path = os.path.join(os.path.dirname(__file__), "trainning.csv")
    process_csv(file_path)
    insert_training_data(file_path)


if __name__ == '__main__':
    main()
