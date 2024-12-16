import os
import dill
import pandas as pd
import json
from datetime import datetime

path = os.environ.get('PROJECT_PATH', os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def predictt():
    model_path = os.path.join(path, 'data/models/cars_pipe_202412161221.pkl')
    test_path = os.path.join(path, 'data/test')
    predict_path = os.path.join(path, 'data/predictions')

    with open(model_path, 'rb') as f:
        model = dill.load(f)

    prediction_list = []

    for item in os.listdir(test_path):
        file_path = os.path.join(test_path, item)
        with open(file_path, 'rb') as f:
            data = json.load(f)
        data_list = [data]
        df = pd.DataFrame(data_list)
        predicted = model.predict(df)
        predictions_df = pd.DataFrame(predicted, columns=["Prediction"])
        predictions_df['File'] = item
        prediction_list.append(predictions_df)


    all_predictions_df = pd.concat(prediction_list, ignore_index=True)

    df_to_csv_path = os.path.join(predict_path, f'predictions_file{datetime.now().strftime("%Y%m%d%H%M")}.csv')
    all_predictions_df.to_csv(df_to_csv_path, index=False)




if __name__ == '__main__':
    predictt()
