jma-amedas2geojson
======

気象庁 [最新の気象データCSVダウンロード](http://www.data.jma.go.jp/obd/stats/data/mdrr/docs/csv_dl_readme.html)よりアメダス降水量データを取得し、GeoJSONを生成する

## How to use

```
python get_amedas.py [datetime]
```

* datetimeには欲しい日時の年月日時分を結合した数値を与える (例: 201804180100)
* datetimeにrctを与えると最新の情報を取得する


## 観測地点情報

気象庁 [地域気象観測システム アメダスの概要](http://www.jma.go.jp/jma/kishou/know/amedas/kaisetsu.html)にて公開されている CSV形式 地域気象観測所一覧 より生成

