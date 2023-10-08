import nasdaqdatalink
import pandas as pd
import os

output_path = os.path.dirname(__file__)
query = True
out = ""
if query:
    key1 = "4Fs3wvoZsxgzwELXyckq"
    nasdaqdatalink.read_key(key1)
    keys = ['ODA/PBARL_USD',
            'ODA/PWHEAMT_USD'] 
    dfs = []
    index = 0
    for product in keys:
        print("here")
        df = nasdaqdatalink.get(product,start_date="2001-12-31", end_date="2005-12-31")
        df['Code'] = product
        if index == 0:
            dfs = df
        else:
            dfs = pd.concat([dfs, df])
        index += 1
    out = dfs
    


'''PART2: Outputting Data'''
out.to_csv(output_path + '//Data//' + 'data.csv')



