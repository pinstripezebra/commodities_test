# Importing packages
from dash import Dash, dcc, html, dcc, Input, Output, ctx, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import os


#loading commodities data to dataframe
base_path = os.path.dirname(__file__)
df = pd.read_csv(base_path + '//Data//' + 'data.csv')
predictions_df = pd.read_csv(base_path + '//Data//' + 'predictions.csv')
df['Date'] = pd.to_datetime(df['Date'])
predictions_df['Date'] = pd.to_datetime(predictions_df['Date'])

#loading conflict data to dataframe
file_name = 'conflict_aggregate.csv'
base_path = os.path.dirname(__file__)
total_path = base_path + '//Data//' + file_name
conflict_df = pd.read_csv(total_path)
px.set_mapbox_access_token("pk.eyJ1IjoibHVjYXNzZWUiLCJhIjoiY2xuejhzeDNxMHRsejJtcWIxOWo0ZGg1eiJ9.FUIBVWbJjEwE0SS-CYAaHg")

colors = {
        'background': '#A5D8DD',
        'text': '#7FDBFF'}

# Initialize the app
dash_app = Dash(__name__)
app = dash_app.server

# App layout
dash_app.layout = html.Div(style={'backgroundColor': colors['background']}, children =[
    html.Div(children= [
             html.H1('Commodities Price and Global Conflict Correlation'),
             dcc.Markdown('A comprehensive tool for examining commodities price fluctuations in relation to world conflict.'),
            
            #Filters
             html.Div(children = [ 
                html.Label('Stock Ticker'),
                dcc.Dropdown(
                    id = 'Code-Filter',
                    options = [{"label": i, "value": i} for i in df['Code'].drop_duplicates()] + 
                                [{"label": "Select All", "value": "all_values"}],
                    value = "all_values"),

                html.Label('Commodity Category'),
                dcc.Dropdown(
                    id = 'Category-Filter',
                    options = [{"label": i, "value": i} for i in df['Category'].drop_duplicates()] + 
                                [{"label": "Select All", "value": "all_values"}],
                    value = "all_values"),
                html.Label('Conflict Region'),
                dcc.Dropdown(
                    id = 'Conflict-Region-Filter',
                    options = [{"label": i, "value": i} for i in conflict_df['region'].drop_duplicates()] + 
                                [{"label": "Select All", "value": "all_values"}],
                    value = "all_values")
             ],style={'width': '50%', 'display': 'inline-block'}),

             

             #Time Series Filtering Buttons
             html.Div([
                dbc.Button('All Time', id='btn-nclicks-1', n_clicks=0,className="me-1"),
                dbc.Button('1 Year',  id='btn-nclicks-2', n_clicks=0,className="me-1"),
                dbc.Button('6 months',  id='btn-nclicks-3', n_clicks=0,className="me-1"),
                dbc.Button('1 Month',  id='btn-nclicks-4', n_clicks=0,className="me-1")
            ],className="row"),

            #First row of graphs
            html.Div([

                #First column
                html.Div([
                    dcc.Graph(id = 'Time-Series',
                            figure={})
                ],style={'width': '49%', 'display': 'inline-block'}),

                #Second column
                html.Div([
                    dcc.Graph(id = 'geographic_plot',
                            figure={})
                ],style={'width': '49%', 'display': 'inline-block'})


            ], style={'padding': 10, 'flex': 1}),

            #Second row of graphs
            html.Div([

                #First column
                html.Div([
                    dcc.Graph(id = 'conflict_time_series',
                            figure={})
                ], style={'width': '49%', 'display': 'inline-block'}),
                #second column
                html.Div([
                    dcc.Graph(id = 'ARIMA-Time-Series',
                            figure={})
                ], style={'width': '49%', 'display': 'inline-block'})
            ],className="row"),

            html.Div([
                html.H3('Data Sources:'),
                html.Div([
                    html.Div(children = [
                        html.Div([
                            dcc.Markdown('Commodities Data: ')
                        ], style={'display': 'inline-block'}),
                        html.Div([
                            html.A("nasdaq api", href='https://data.nasdaq.com/tools/python', target="_blank")
                        ], style={'display': 'inline-block'})
                    ], className="row"
                )
                ]),

                html.Div([
                    html.Div(children = [
                        html.Div([
                            dcc.Markdown('Conflict data from: ')
                        ], style={'display': 'inline-block'}),
                        html.Div([
                            html.A("ACLED", href='https://acleddata.com/', target="_blank")
                        ], style={'display': 'inline-block'})
                    ], className="row"
                )
                ])

             ])
        ])
])

#callback for commodities data
@callback(
    [Output(component_id='Time-Series', component_property='figure'),
    Output(component_id='ARIMA-Time-Series', component_property='figure')],
    Input(component_id='Code-Filter', component_property='value'),
    Input(component_id='Category-Filter', component_property='value'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks')
)
def update_output_div(value, category, all_time, five_years, one_year, one_month):

    code_list = ""
    category_list = ""
    filtered_df = df
    arima_df = predictions_df

    #Filtering for stock tickers
    if value == "all_values":
        code_list = filtered_df['Code'].drop_duplicates()
    else:
        code_list = [value]

    #Filtering for categories
    if category == "all_values":
        category_list = filtered_df['Category'].drop_duplicates()
    else:
        category_list = [category]

    earliest_date = filtered_df['Date'].min()

    #button filtering
    if "btn-nclicks-2" == ctx.triggered_id:
        earliest_date = filtered_df['Date'].max() - pd.Timedelta(weeks=52)
    elif "btn-nclicks-3" == ctx.triggered_id:
        earliest_date = filtered_df['Date'].max() - pd.Timedelta(weeks=26)
    elif "btn-nclicks-4" == ctx.triggered_id:
        earliest_date = filtered_df['Date'].max() - pd.Timedelta(weeks=4)
    
    #Applying button filter
    filtered_df = filtered_df[filtered_df['Date'] > earliest_date]
    arima_df = arima_df[arima_df['Date'] > earliest_date]

    #filtering dataframes for selected codes and categories
    filtered_df = filtered_df[(filtered_df['Code'].isin(code_list)) &
                              (filtered_df['Category'].isin(category_list))]
    arima_df =  arima_df[arima_df['Code'].isin(code_list) &
                         (arima_df['Category'].isin(category_list))]

    #Plotting results
    fig=px.line(filtered_df, x='Date', y='Open', color = 'Name', line_group = 'Category',
                title = "Closing Market Price Over Time by Category")
    arima_fig = px.line(arima_df, x='Date', y='value', color = 'Name', line_dash = 'variable',
                title = "ARIMA forecasting of closing market price")

    return fig, arima_fig


#callback for conflict data
@callback(
    [Output(component_id='geographic_plot', component_property='figure'),
    Output(component_id='conflict_time_series', component_property='figure')],
    Input('Conflict-Region-Filter', 'value'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks')
)
def update_output_div(conflict_region,all_time, five_years, one_year, one_month):

    filtered_df = conflict_df
    filtered_df['event_date'] = pd.to_datetime(filtered_df['event_date'])
    filtered_df['Month-Year'] = filtered_df['Year'].astype(str) + '-' + filtered_df['Month'].astype(str) + '-' + '01'
    #filtered_df['Month-Year'] =  filtered_df['Month-Year'].astype('datetime')
    earliest_date = filtered_df['event_date'].min()

    conflict_region_list = ""
    #Filtering for stock tickers
    if conflict_region == "all_values":
        conflict_region_list = filtered_df['region'].drop_duplicates()
    else:
        conflict_region_list = [conflict_region]

    #button filtering
    if "btn-nclicks-2" == ctx.triggered_id:
        earliest_date = filtered_df['event_date'].max() - pd.Timedelta(weeks=52)
    elif "btn-nclicks-3" == ctx.triggered_id:
        earliest_date = filtered_df['event_date'].max() - pd.Timedelta(weeks=26)
    elif "btn-nclicks-4" == ctx.triggered_id:
        earliest_date = filtered_df['event_date'].max() - pd.Timedelta(weeks=4)
    
    #Applying filters to dataframe
    filtered_df = filtered_df[(filtered_df['event_date'] > earliest_date) &
                              (filtered_df['region'].isin(conflict_region_list))]

    top_df = filtered_df.sort_values(by = ['fatalities'], ascending= False).head(1000)

    map_fig = px.scatter_mapbox(top_df, 
                            lat="latitude", lon="longitude", color="disorder_type", size="fatalities",
                            hover_data=["fatalities", "disorder_type", "event_date"],
                            zoom = 2)
    
    timeseries_conflict_fig = px.bar(filtered_df[['fatalities', 'region', 'Month-Year']].groupby(['Month-Year', 'region']).sum().reset_index(),
                                      x="Month-Year", y="fatalities",color = 'region', title = "Fatalities from Global Conflicts")
    
    return map_fig, timeseries_conflict_fig

# Run the app
if __name__ == '__main__':
    dash_app.run_server(debug=False)
