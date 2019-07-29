from math import radians, cos, sin, asin, sqrt
import pandas as pd
import MySQLdb

db = MySQLdb.connect(host="127.0.0.1",  
                     user="root",         
                     passwd="database", 
                     db="cs411") 

engin = [-88.227240, 40.113910]
main = [-88.227240, 40.107936]
south = [-88.230845, 40.102291]

def distance(part):
    cur = db.cursor()
    cur.execute('SELECT * FROM tidychampaign')
    champaign = pd.read_sql('SELECT GEOID, Block FROM tidychampaign', con=db)
    geo = pd.read_sql('SELECT GEOID, lon, lat FROM geo', con=db)
    data = pd.merge(geo, champaign,
                    on='GEOID',
                    how='inner')
    dis = list(range(len(data)))
    for i in range(len(data)):        
        lon1, lat1, lon2, lat2 = map(radians, [part[0], part[1], data['lon'][i], data['lat'][i]])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371
        dis[i] = c * r
        data['distance'] = dis
    return data