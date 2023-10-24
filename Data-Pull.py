import nasdaqdatalink
import pandas as pd
import os
import datetime

output_path = os.path.dirname(__file__)
query = True
out = ""

#Dates
start = str(datetime.date.today())
end = datetime.date.today() - datetime.timedelta(days=30)
print(start, end)
key1 = "7X8ExZzpppAn5RLGZ3Fc" #For use with the nasdaq API
nasdaqdatalink.read_key(key1)

#"https://data.nasdaq.com/api/v3/datasets/XNAS/ACIW/metadata.json?api_key=" + key1
#test = nasdaqdatalink.get("https://data.nasdaq.com/api/v3/datasets/XNAS/ACIW/metadata.json?api_key=" + key1)

if query:

    keys1 = {
            'ODA/PBEEF_USD': ['Farm and Fishery', 'Cattle, Beef'],
            'ODA/PPOULT_USD': ['Farm and Fishery', 'Poultry, Chicken'],
            'ODA/PWOOLC_USD': ['Farm and Fishery', 'Wool'],
            'ODA/POILDUB_USD': ['Crude Oil', 'Dubai Crude'],
            'ODA/POILBRE_USD': ['Crude Oil', 'Brent Crude'],
            'ODA/PNGASEU_USD': ['Natural Gas', 'German Natural Gas'],
            'ODA/PNGASUS_USD': ['Natural Gas', 'Henry Hub Natural Gas'],
            'ODA/PNGASJP_USD': ['Natural Gas', 'Japan Natural Gas'],
            'ODA/PBARL_USD': ['Grains', 'Barley, Western Canada'],
            'ODA/PWHEAMT_USD': ['Grains', 'Wheat, Gulf of Mexico'],
            'ODA/PRICENPQ_USD': ['Grains', 'Rice, Thailand'],
            'ODA/PALUM_USD': ['Metals', 'Aluminum'],
            'ODA/PCOPP_USD': ['Metals', 'Copper'],
            'ODA/PLEAD_USD': ['Metals', 'Lead']}
    

    
    dfs = []
    index = 0
    for product in list(keys1.keys()):
        print("here")
        #df = nasdaqdatalink.get(product, api_key = key1, collapse="daily",start_date="2021-01-01")
        df = nasdaqdatalink.get(product, api_key = key1,collapse="daily",start_date="2021-01-01")

        #Adding code and category as columns
        df['Code'] = product
        df['Category'] = keys1[product][0]
        df['Name'] = keys1[product][1]
        if index == 0:
            dfs = df
        else:
            dfs = pd.concat([dfs, df])
        index += 1
    out = dfs
    


'''PART2: Outputting Data'''
out['event_date'] = pd.to_datetime(out['event_date'])
out = out.rename(columns = {'Value': 'Open'})
out.to_csv(output_path + '//Data//' + 'data.csv')






