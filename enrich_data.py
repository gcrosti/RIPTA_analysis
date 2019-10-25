#%%
import pandas as pd 
import numpy as np 
import time
vp_delays = pd.read_pickle('/Users/giuseppecrosti/Documents/RIPTA/analysis/vp_delays.pkl')

#%%
vp_delays.head()

#%%
vp_delays['hr_of_day'] = [time.localtime(x).tm_hour for x in vp_delays['timestamp_']]
vp_delays.head()

#%%
vp_delays['day_of_week'] = [time.localtime(x).tm_wday for x in vp_delays['timestamp_']]
vp_delays.head()
#%%
def isweekday(num):
    if num==5 or num==6:
        return False
    return True

vp_delays['is_wkday'] = [isweekday(x) for x in vp_delays['day_of_week']]
vp_delays['is_wkday'].value_counts()
#%%
def isbeforeschool(num):
    if num > 1567396800:
        return False
    return True
vp_delays['isb4school'] = [isbeforeschool(x) for x in vp_delays['timestamp_']]
vp_delays.head()

#%%
vp_delays[['isb4school','delay']].groupby(['isb4school']).mean()

#%%
def inpvd(lon,lat):
    if -71.472716 < lon < -71.365464:
        if 41.787151 < lat < 41.858831:
            return True
    return False

vp_delays['position_lon'] = vp_delays['position_lon'].astype(float)
vp_delays['position_lat'] = vp_delays['position_lat'].astype(float)
vp_delays.head()
#%%
vp_delays['inpvd'] = [inpvd(x,y) for x,y in zip(vp_delays['position_lon'],vp_delays['position_lat'])]
vp_delays.head()


#%%
vp_delays.to_pickle('vp_delays_enriched')

#%%
