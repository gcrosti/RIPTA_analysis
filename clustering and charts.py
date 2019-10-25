#%% IMPORTING LIBRARIES AND DATA
import pandas as pd
import numpy as np
import hdbscan
from sklearn.preprocessing import StandardScaler
vpd_enriched = pd.read_pickle('/Users/giuseppecrosti/Documents/RIPTA/analysis/vp_delays_enriched.pkl')
import geopandas as gpd
import matplotlib.pyplot as plt
stops = pd.read_csv('/Users/giuseppecrosti/Downloads/Static data/google_transit/stops.txt')
from shapely.geometry import Point, Polygon
ri_map = gpd.read_file('/Users/giuseppecrosti/Documents/RIPTA/tl_2016_44_tract/tl_2016_44_tract.shp')
import descartes

#%% SEPARATING DELAY DATA
only_delays = vpd_enriched[vpd_enriched['delay'] != 0]
only_delays.head()

#%% CREATING ABSOLUTE DELAYS
only_delays['abs_delay'] = only_delays['delay'].abs()
only_delays['islate'] = [x > 0 for x in only_delays['delay']]
#%% CHECKING DISTRIBUTION OF DELAYS

plt.scatter(only_delays['position_lon'],only_delays['position_lat'],s=0.5)
plt.show
#%% CHECKING DISTRIBUTION OF ON-SCHEDULE BUSES
only_ontime = vpd_enriched[vpd_enriched['delay'] == 0]
plt.scatter(only_ontime['position_lon'],only_ontime['position_lat'],s=0.5)
plt.show

#%% Z-SCORING CONTINUOUS VARIABLES BEFORE HDBSCAN
scaler = StandardScaler()
variables = ['position_lat','position_lon','speed','bearing','timestamp_']
scaler.fit(only_delays[variables])
vars_std = scaler.transform(only_delays[variables])
#%% SANITY CHECK AFTER Z-SCORING
l = len(vars_std)
position_la = [vars_std[x][0] for x in range(l)]
position_lo = [vars_std[x][1] for x in range(l)]

plt.scatter(position_lo,position_la,s=0.5)
#%% HDBSCAN
clusterer = hdbscan.HDBSCAN(min_cluster_size=20,min_samples=1)
clusterer.fit(vars_std)
only_delays['labels'] = clusterer.labels_
only_delays['labels_probabilities'] = clusterer.probabilities_
only_delays['labels'].value_counts()
#%% LABELING PROBABILITIES
only_delays[only_delays['labels']!=-1]['labels_probabilities'].describe()
#%% PLOTTING DELAYS BY HDBSCAN LABELS
import seaborn as sns
sns.scatterplot(x='position_lon',y='position_lat',data=only_delays[only_delays['labels']!=-1],hue='labels',style='labels')
#%% BUILDING POINTS OBJECTS FOR MAPPING
geometry_stops = [Point(xy) for xy in zip(stops['stop_lon'],stops['stop_lat'])]
geometry_delays = [Point(xy) for xy in zip(only_delays['position_lon'],only_delays['position_lat'])]

#%% BUILDING GEO_DFs
crs = {'init':'espg:4326'}
geo_df = gpd.GeoDataFrame(only_delays,crs=crs,geometry=geometry_delays)
geo_df_stops = gpd.GeoDataFrame(stops,crs=crs,geometry=geometry_stops)
#%% BUILDING OUT MAP OF DELAYS BY HDBSCAN CAT
fig,ax = plt.subplots(figsize=(15,15))
ri_map.plot(ax=ax,color='grey')
geo_df_stops.plot(ax=ax,markersize=0.1,color='white',marker='x',label='stops')
geo_df[geo_df['labels']==-1].plot(ax=ax,markersize=5,color='yellow',marker='o',label='uncategorized')
geo_df[geo_df['labels']==0].plot(ax=ax,markersize=5,color='red',marker='o',label='category 1')
geo_df[geo_df['labels']==1].plot(ax=ax,markersize=5,color='blue',marker='o',label='category 2')
legend = plt.legend(prop={'size':15})
frame = legend.get_frame()
frame.set_facecolor('grey')
#%% BUILDING OUT MAP OF DELAYS BY GROUPING
fig,ax = plt.subplots(figsize=(15,15))
ri_map.plot(ax=ax,color='grey')
geo_df_stops.plot(ax=ax,markersize=0.1,color='white',marker='x',label='stops')
geo_df[geo_df['delay']<300].plot(ax=ax,markersize=5,color='yellow',marker='o',label='<5 min')
geo_df[geo_df['delay']>300][geo_df['delay']<600].plot(ax=ax,markersize=5,color='orange',marker='o',label='<10 min')
geo_df[geo_df['delay']>600].plot(ax=ax,markersize=5,color='red',marker='o',label='>10 min')
legend = plt.legend(prop={'size':15})
frame = legend.get_frame()
frame.set_facecolor('grey')

#%% DELAY DISTRIBUTION BY HDBSCAN LABEL
hdb_cats = [-1,0,1]
cats_delays = {}
for x in hdb_cats:
    cats_delays[x] = []
    x_delays = only_delays[only_delays['labels']==x]
    x_tot = x_delays['id'].count()
    cats_delays[x].append(x_delays[only_delays['delay']<300]['id'].count()/x_tot)
    cats_delays[x].append(x_delays[only_delays['delay']>300][only_delays['delay']<600]['id'].count()/x_tot)
    cats_delays[x].append(x_delays[only_delays['delay']>600]['id'].count()/x_tot)

fig,ax = plt.subplots(figsize=(10,10))
ind = np.arange(len(cats_delays[-1]))
width = 0.2
plt.bar(ind,cats_delays[-1],width,label='cat -1 delays')
plt.bar(ind+width,cats_delays[-0],width,label='cat 0 delays')
plt.bar(ind+2*width,cats_delays[1],width,label='cat 1 delays')

#%% DAY OF WEEK DISTRIBUTION BY HDBSCAN LABEL
dayofweek_cats = only_delays['day_of_week'].unique()
dayofweek_cats.sort()
dcats_delays = {}
for day in dayofweek_cats:
    dcats_delays[day] = []
    d_delays = only_delays[only_delays['day_of_week']==day]
    dcats_delays[day].append(d_delays[d_delays['labels']==-1]['delay'].mean())
    dcats_delays[day].append(d_delays[d_delays['labels']==0]['delay'].mean())
    dcats_delays[day].append(d_delays[d_delays['labels']==1]['delay'].mean())

dcats_delays

#%%
fig,ax = plt.subplots(figsize=(15,15))
ind = np.arange(len(dcats_delays[0]))
width = 0.1
counter = 0
for day in dcats_delays:
    plt.bar(ind+width*counter,dcats_delays[day],width,label='delays at {}hrs'.format(str(day)))
    counter += 1


#%%
dcats_delays_school = {}
for day in dayofweek_cats:
    dcats_delays_school[day] = []
    d_delays = only_delays[only_delays['day_of_week']==day]
    dcats_delays_school[day].append(d_delays[d_delays['isb4school']==True]['delay'].mean())
    dcats_delays_school[day].append(d_delays[d_delays['isb4school']==False]['delay'].mean())

#%%
fig,ax = plt.subplots(figsize=(15,15))
ind = np.arange(len(dcats_delays_school[0]))
width = 0.1
counter = 0
for day in dcats_delays_school:
    plt.bar(ind+width*counter,dcats_delays_school[day],width,label='delays at {}hrs'.format(str(day)))
    counter += 1

#%%
fig,ax = plt.subplots(figsize=(15,15))
ri_map.plot(ax=ax,color='grey')
geo_df_stops.plot(ax=ax,markersize=0.1,color='white',marker='x',label='stops')
geo_df[geo_df['isb4school']==True].plot(ax=ax,markersize=5,color='yellow',marker='o',label='before school')
geo_df[geo_df['isb4school']==False].plot(ax=ax,markersize=5,color='red',marker='o',label='during school')
legend = plt.legend(prop={'size':15})
frame = legend.get_frame()
frame.set_facecolor('grey')


#%%
