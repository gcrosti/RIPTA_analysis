def remove_dupes_vp(df):
    return df[df.duplicated(subset=['timestamp','position_lat','position_lon'],keep=False)==True]

def remove_dupes_tu(df):
    return df[df.duplicated(subset=['timestamp','trip_id','stop_id'],keep=False)==True]