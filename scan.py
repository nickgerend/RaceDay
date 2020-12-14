# Written by: Nick Gerend, @dataoutsider
# Viz: "RaceDay", enjoy!

import os
import pandas as pd

directory = os.path.dirname(__file__) + '/Boston-Marathon-Data-Project-master'
firstentry = True
df1 = pd.DataFrame()
for entry in os.scandir(directory):
    if entry.path.endswith(".csv") and entry.is_file() and len(entry.name) == 15:
        print(entry.name)
        year = entry.name[7:-4]
        df2 = pd.read_csv(os.path.dirname(__file__) + '\\Boston-Marathon-Data-Project-master\\' + entry.name)
        df2['year'] = year
        df1 = pd.concat([df1, df2])
        print(df1.shape)

df1.reset_index(inplace=True)
df1 = df1[['index','display_name','age','gender','official_time','seconds','overall','year']]
df1.reset_index(inplace=True)
print(df1)
df1.to_csv(os.path.dirname(__file__) + '/allyears.csv', encoding='utf-8', index=False)