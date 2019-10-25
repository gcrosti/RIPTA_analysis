
#%%
#importing data and libraries
import pandas as pd
import numpy as np
trip_updates_df = pd.read_pickle('/Users/giuseppecrosti/Documents/RIPTA/analysis/trip_updates.pkl')
vehicle_positions_df = pd.read_pickle('/Users/giuseppecrosti/Documents/RIPTA/analysis/vehicle_positions.pkl')

#%%
#defining helper funcs
def timestamp_formatting(df):
    out = df
    out['timestamp_'] = df['timestamp_'].astype(int)
    return out

def find_delays(vp,tu):
    vp['timestamp_rounded'] = round(vp['timestamp_'],-1)
    tu['timestamp_rounded'] = round(tu['timestamp_'],-1)
    results = vp.merge(tu[['timestamp_rounded','trip_id','delay','stop_id']],on=['timestamp_rounded','trip_id','stop_id'],how='left')
    return results

def remove_dupes_vp(df):
    return df[df.duplicated(subset=['timestamp_','position_lat','position_lon'],keep='first')==False]

def remove_dupes_tu(df):
    return df[df.duplicated(subset=['timestamp_','trip_id','stop_id'],keep='first')==False]

#%%
#timestamp formatting
trip_updates_df = timestamp_formatting(trip_updates_df)
vehicle_positions_df = timestamp_formatting(vehicle_positions_df)

#%%
vehicle_positions_df['is_dupe'] = vehicle_positions_df.duplicated(subset=['timestamp_','position_lat','position_lon','trip_id','route_id','vehicle_id'],keep='first')
vehicle_positions_df.head()

#%%
trip_updates_df['is_dupe'] = trip_updates_df.duplicated(subset=['timestamp_','trip_id','stop_id'],keep='first')
trip_updates_df.head()

#%%
trip_updates_df['is_dupe'].value_counts()

#%% 
trip_updates_df['update_timestamp'].nunique()
vehicle_positions_df['timestamp_'].nunique()

#%%
vp_deduped = vehicle_positions_df[vehicle_positions_df['is_dupe']==False]
tu_deduped = trip_updates_df[trip_updates_df['is_dupe']==False]

#%%
#find delays
vp_delays = find_delays(vp=vp_deduped,tu=tu_deduped)
vp_delays.head()

#%%
vp_delays['delay'] = vp_delays['delay'].fillna(0)
vp_delays.head()


#%% Pickle VP_delays
vp_delays.to_pickle('vp_delays.pkl')

#%%
