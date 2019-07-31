from math import radians, cos, sin, asin, sqrt, log
from ipywidgets import IntSlider
from ipywidgets.embed import embed_minimal_html
import pandas as pd
import MySQLdb
import numpy as np
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import GridSearchCV
import gmaps


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
        dis[i] = c * r / 1.60934
    data['distance1'] = dis
    data = data.drop(['lon', 'lat', 'Block'], 1)
    return [dis,data]

def process_for_model(statement):
    cur = db.cursor()
    cur.execute('SELECT * FROM tidychampaign')
    champaign = pd.read_sql('SELECT * FROM tidychampaign', con=db)
    geo = pd.read_sql('SELECT * FROM geo', con=db)
    socio = pd.read_sql('SELECT * FROM socio', con=db)
    rate = pd.read_sql(statement, con = db)
    
    socio['educ'] = 0
    for i in list(range(5,29)):
        socio['educ'] = socio['educ'] + (socio[socio.columns[i]] * (i-1))
    socio['educ'] = socio['educ'] / socio[socio.columns[4]]
    socio = socio.drop(socio.columns[4:29], 1)
    
    champaign['Geography'] = champaign['Geography'].str.split(", ", 1, expand=True)[1]
    data = pd.merge(geo, champaign, on='GEOID', how='inner')
    data = pd.merge(data, socio, on='Geography', how='left')
    data = data.fillna(data.median())
    data['Median_rent'] = np.log(data.Median_rent)
    data = pd.merge(data, rate, on='Block', how='right')
    dist = distance(south)[1]
    dist['distance2'] = distance(main)[0]
    dist['distance3'] = distance(engin)[0]
    data = pd.merge(data, dist, on='GEOID', how='left')
    data = data.drop(['GEOID', 'lat', 'lon', 'Block', 'Geography'],1)
    
    for feature in data.columns:
        if data[feature].dtype == 'object' and feature != 'Username':
            X_ = pd.get_dummies(data[feature])
            data = pd.concat([data, X_], axis = 1).drop([feature], axis = 1)

    return data

def predictor(input_data):
    
    train = process_for_model('SELECT * FROM rate')
    
    parametersGrid = {"max_iter": [1, 5, 10],
                  "alpha": [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
                  "l1_ratio": np.arange(0.0, 1.0, 0.1)}
  
    X = train.drop(['Rate','Username'],1)
    Y = train['Rate']

    eNet = ElasticNet()
    grid = GridSearchCV(eNet, parametersGrid, scoring='r2', cv=10)
    grid.fit(X, Y)
    a = grid.predict(input_data.drop(['Rate','Username'],1))
    return a

def result_prediction(input_username):
    data = process_for_model('SELECT * FROM rate')
    data = data[data['Username'] == input_username]
    result = np.mean(predictor(data))
    return result

# input_data = [Pop, White, Black, Asian, OtherRace, Male, Female, Young, Middle, Old, Sdist, Ndist, Mdist]
def preference(input_data):
    cur = db.cursor()
    cur.execute('SELECT * FROM tidychampaign')
    champaign = pd.read_sql('SELECT * FROM tidychampaign', con=db)
    geo = pd.read_sql('SELECT * FROM geo', con=db)
    data = pd.merge(geo, champaign,
                    on='GEOID',
                    how='inner')
    data['south'] = distance(south)[0]
    data['north'] = distance(engin)[0]
    data['main'] = distance(main)[0]
    data = data.drop(['lat', 'lon', 'Block', 'Geography'],1)
    data['s_n'] = data['south']
    data['n_n'] = data['north']
    data['m_n'] = data['main']
    
    for i in [2,3,4,5,6,7,8,9,10]:
        data[data.columns[i]] = data[data.columns[i]]/data['Population']
        data = data.fillna(0)
        data = data.replace(np.inf, 0)
    
    def normalize(column):
        data[column] = (data[column] - min(data[column])) / (max(data[column]) - min(data[column]))
        return data[column]
    
    for i in [1,2,3,4,5,6,7,8,9,10, 14, 15, 16]:
        data[data.columns[i]] = normalize(data.columns[i])
    
    for i in [1,2,3,4,5,6,7,8,9,10]:
        data[data.columns[i]] = input_data[i] * data[data.columns[i]]
    
    opera = (data.south < input_data[10]) * (data.main < input_data[11]) * (data.north < input_data[12])
    data['score'] = (data.ix[:, [1,2,3,4,5,6,7,8,9,10]].T.apply(sum) + data.ix[:, [14,15,16]].T.apply(sum)/3) * opera
    data = data[['GEOID','score', 'south', 'north', 'main']]
    data = pd.merge(data, geo,
                    on='GEOID',
                    how='inner')
    return data

def score_final(input_username, input_data):
    data = preference(input_data)
    data['score'] = result_prediction(input_username) + data['score']
    data = data.sort_values(by = 'score', ascending=False)
    data['rank'] = range(1, len(data)+1)
    mark(data)
    heat(data)
    bashCommand = "mv export.html datamanager/templates/datamanager/. && mv heat.html datamanager/templates/datamanager/."
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)    
    return data  

def mark(score):
    gmaps.configure(api_key = 'AIzaSyBzozWYI3q9hIHEOh1arRxsMLLzYx83MLQ')
    champaign = (40.1112, -88.243)
    fig = gmaps.figure(center=champaign, zoom_level=14)

    index = score.index
    marker_locations = [
        (score.lat[index[0]], score.lon[index[0]]),
        (score.lat[index[1]], score.lon[index[1]]),
        (score.lat[index[2]], score.lon[index[2]]),
        (score.lat[index[3]], score.lon[index[3]]),
        (score.lat[index[4]], score.lon[index[4]]),
        (score.lat[index[5]], score.lon[index[5]]),
        (score.lat[index[6]], score.lon[index[6]]),
        (score.lat[index[7]], score.lon[index[7]]),
        (score.lat[index[8]], score.lon[index[8]]),
        (score.lat[index[9]], score.lon[index[9]])   
    ]
    markers = gmaps.marker_layer(marker_locations)
    fig.add_layer(markers)
    embed_minimal_html('export.html', views=[fig])

def heat(score):
    gmaps.configure(api_key = 'AIzaSyBzozWYI3q9hIHEOh1arRxsMLLzYx83MLQ')
    champaign = (40.1112, -88.243)
    fig = gmaps.figure(center=champaign, zoom_level=13)
    locations = score[['lat', 'lon']]
    weights = score['score']
    fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
    embed_minimal_html('heat.html', views=[fig])