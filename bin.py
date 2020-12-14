# Written by: Nick Gerend, @dataoutsider
# Viz: "RaceDay", enjoy!

import numpy as np
import pandas as pd
import os
import math
from datetime import datetime

df = pd.read_csv(os.path.dirname(__file__) + '/marathon_results_2017.csv', engine='python')

data = df['Official Time']._values
data = [datetime.strptime(o, '%H:%M:%S').time() for o in data]
data = [o.hour + o.minute/60 + o.second/3600 for o in data]

tmax = int(max(data)) + 1
hr_res = 2
hmax = tmax * hr_res + 1
xbins = [x * (1/hr_res) for x in range(0, hmax)]
test = np.histogram(data, bins=xbins)
print(test)