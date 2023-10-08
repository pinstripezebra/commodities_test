# Importing packages
from dash import Dash, dcc, html, dcc, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import os

#Loading data to dataframe
base_path = os.path.dirname(__file__)
df = pd.read_csv(base_path + '//Data//' + 'data.csv')
predictions_df = pd.read_csv(base_path + '//Data//' + 'predictions.csv')
print("hello")
# Initialize the app
app = Dash(__name__)
server = app.server
# App layout
app.layout = html.Div([
    html.Div(children= [
             html.H1('Commodities Forecasting'),

            dcc.Dropdown(
                id = 'Code-Filter',
                options = [{"label": i, "value": i} for i in df['Code'].drop_duplicates()] + 
                            [{"label": "Select All", "value": "all_values"}],
                value = "all_values"),

            dcc.Graph(id = 'Time-Series',
                    figure={}),
            dcc.Graph(id = 'ARIMA-Time-Series',
                    figure={})
            ])
])


@callback(
    [Output(component_id='Time-Series', component_property='figure'),
    Output(component_id='ARIMA-Time-Series', component_property='figure')],
    Input(component_id='Code-Filter', component_property='value')
)
def update_output_div(value):

    code_list = ""
    filtered_df = df
    arima_df = predictions_df

    if value == "all_values":
        code_list = filtered_df['Code'].drop_duplicates()
    else:
        code_list = [value]

    #filtering dataframes for selected codes
    filtered_df = filtered_df[filtered_df['Code'].isin(code_list)]
    arima_df =  arima_df[arima_df['Code'].isin(code_list)]

    #Plotting results
    fig=px.line(filtered_df, x='Date', y='Value', color = 'Code',
                title = "Closing Market Price Over Time by Category")
    arima_fig = px.line(arima_df, x='Date', y='value', color = 'Code', line_dash = 'variable',
                title = "ARIMA forecasting of closing market price")
    return fig, arima_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
