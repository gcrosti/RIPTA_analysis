def timestamp_formatting(df):
    out = df
    out['timestamp_'] = df['timestamp_'].astype(int)
    return out

