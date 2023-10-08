import pandas as pd
import os
from statsmodels.tsa.arima.model import ARIMA

#Loading data to dataframe
base_path = os.path.dirname(__file__)
df = pd.read_csv(base_path + '//Data//' + 'data.csv')

#Splitting into test and train
train_data_by_code = {}
test_data_by_code = {}
for i in df['Code'].drop_duplicates():
    code_df = df[df['Code'] == i].reset_index()
    msk = (code_df.index < len(code_df)-30)
    train_data_by_code[i] = code_df[msk].copy()
    test_data_by_code[i] = code_df[~msk].copy()

models = {}
#Fitting a model for each code
for i in list(train_data_by_code.keys()):
    model = ARIMA(train_data_by_code[i]['Value'], order=(2,1,0))
    model_fit = model.fit()
    models[i] = model_fit

#Forecasting Data
predictions = []
for i in df['Code'].drop_duplicates():
    forecast_test = models[i].forecast(len(test_data_by_code[i]))
    out_df = df[df['Code'] == i].reset_index()
    out_df['ARIMA Forecast'] = [None]*len(train_data_by_code[i]) + list(forecast_test)
    predictions.append(out_df)

#Concatting outputs into one output dataframe
output_df = pd.concat(predictions, ignore_index=True)
output_df = pd.melt(output_df, id_vars = ['Date', 'Code'],
                    value_vars = ['Value', 'ARIMA Forecast'])
output_df.to_csv(base_path + '//Data//' + "predictions.csv")