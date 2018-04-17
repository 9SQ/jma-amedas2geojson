import sys, shutil
import csv, json
import urllib.request
import sqlite3

argvs = sys.argv
argc = len(argvs)

if (argc > 1):
    datetime = argvs[1]
else:
    datetime = 'rct'

# SQLiteにアメダス観測地点テーブルを展開
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("CREATE TABLE amedas (code TEXT PRIMARY KEY, pref TEXT, name TEXT, kana TEXT, address TEXT, lat_d INTEGER, lat_m REAL, lon_d INTEGER, lon_m REAL);")
with open("amedas_point.csv",'r') as fin:
    dr = csv.DictReader(fin, fieldnames = ('code', 'pref', 'name', 'kana', 'address', 'lat_d', 'lat_m', 'lon_d', 'lon_m'))
    to_db = [(c['code'], c['pref'], c['name'], c['kana'], c['address'], c['lat_d'], c['lat_m'], c['lon_d'], c['lon_m']) for c in dr]
cursor.executemany("INSERT INTO amedas(code, pref, name, kana, address, lat_d, lat_m, lon_d, lon_m) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
connection.commit()

# 気象庁Webサイトからcsvを取得
data_url = 'http://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/preall00_'+datetime+'.csv'
data_req = urllib.request.Request(data_url)
with urllib.request.urlopen(data_req) as response:
    reader = csv.reader(response.read().decode('shift-jis').splitlines())
    header = next(reader)

features = []

for r in reader:
    cursor.execute("SELECT lat_d, lat_m, lon_d, lon_m FROM amedas WHERE code=" + r[0])
    row = cursor.fetchone()
    lat = float(row[0]) + float(row[1])/60
    lon = float(row[2]) + float(row[3])/60
    value1h = float(r[19]) if r[19] else None
    value3h = float(r[23]) if r[23] else None
    value24h = float(r[27]) if r[27] else None
    value48h = float(r[31]) if r[31] else None
    value72h = float(r[35]) if r[35] else None

    feature = {
        "geometry": {
            "type": "Point",
            "coordinates": [
                float(lon),
                float(lat)
            ]
        },
        "type": "Feature",
        "properties": {
            "code": r[0],
            "pref": r[1],
            "name": r[2],
            "value1h": value1h,
            "value3h": value3h,
            "value24h": value24h,
            "value48h": value48h,
            "value72h": value72h
        }
    }
    features.append(feature)

featurecollection = {"type":"FeatureCollection","features":features}

f = open(datetime + ".json", "w")
f.write(json.dumps(featurecollection, ensure_ascii=False))
f.close()
shutil.copy(datetime + ".json", "recent.json")
print("save to " + datetime + ".json")
