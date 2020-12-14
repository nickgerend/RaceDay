# Written by: Nick Gerend, @dataoutsider
# Viz: "RaceDay", enjoy!

import numpy as np
import pandas as pd
import os
import math
from datetime import datetime

df = pd.read_csv(os.path.dirname(__file__) + '/allyears.csv', engine='python')

data = df['seconds']._values / 3600

tmax = int(max(data)) + 1
hr_res = 2
hmax = tmax * hr_res + 1
xbins = [x * (1/hr_res) for x in range(0, hmax)]
test = np.histogram(data, bins=xbins)
print(test)