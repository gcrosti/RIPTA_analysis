def find_delays(vp,tu):
    vp['timestamp_rounded'] = round(vp['timestamp_'],-2)
    tu['timestamp_rounded'] = round(tu['timestamp_'],-2)
    results = vp.merge(tu[['timestamp_rounded','trip_id','delay','stop_id']],on=['timestamp_rounded','trip_id','stop_id'],how='left')
    return results
                
