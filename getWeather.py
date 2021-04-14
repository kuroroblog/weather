#!/usr/bin/env python

import urllib.request
from bs4 import BeautifulSoup
import requests

# アイコンが格納されているパス（絶対パスで入力する）
iconPath = "PATH"
# 本番用トークンID
lineNotifyToken = 'TOKEN'
# LINE Notify APIのURL
lineNotifyApi = 'https://notify-api.line.me/api/notify'
# 抽出対象のRSSとURL(デフォルトは東京都)
# 以下のリンクを参照して自身の天気を確認する。
# @link https://weather.yahoo.co.jp/weather/rss/
rssUrl = "https://rss-weather.yahoo.co.jp/rss/days/4410.xml"
URL = "https://weather.yahoo.co.jp/weather/jp/13/4410/13103.html"
# 探索したいキーワード
keyword = '東京'
# 取得したい天気の件数
perDay = 2

# 天気に関するタイトルリスト
titleList = []
# 天気に関する詳細リスト
descList = []

## parser : 天気情報WebページのHTMLタグから天気情報を抽出してパースするメソッド ##########################
def parser(rssUrl):
    with urllib.request.urlopen(rssUrl) as res:
        xml = res.read()
        soup = BeautifulSoup(xml, "html.parser")
        for item in soup.find_all("item"):
            title = item.find("title").string
            description = item.find("description").string
            if title.find(keyword) != -1:
                titleList.append(title)
                descList.append(description)

## ckWeather : 取得した天気情報とそれに応じた天気アイコンを出力するメソッド ################################
def ckWeather(detail):
    isFind = False
    for boolean, fileName in [
        [detail.find("晴") != -1 and (detail.find("曇")) == -1 and (detail.find("雨")) == -1 and (detail.find("雪")) == -1, "sunny.png"],
        [detail.find("晴一時曇") != -1 or (detail.find("晴のち曇")) != -1 or (detail.find("晴時々曇")) != -1, "sunnyToCloud.png"],
        [detail.find("晴一時雨") != -1 or (detail.find("晴のち雨")) != -1 or (detail.find("晴時々雨")), "sunnyToRain.jpg"],
        [detail.find("晴一時雪") != -1 or (detail.find("晴のち雪")) != -1 or (detail.find("晴時々雪")) != -1, "sunnyToSnow.jpg"],
        [detail.find("曇") != -1 and (detail.find("晴")) == -1 and (detail.find("雨")) == -1 and (detail.find("雪")) == -1, "cloud.png"],
        [detail.find("曇一時晴") != -1 or (detail.find("曇のち晴")) != -1 or (detail.find("曇時々晴")) != -1, "cloudToSunny.png"],
        [detail.find("曇一時雨") != -1 or (detail.find("曇のち雨")) != -1 or (detail.find("曇時々雨")) != -1, "cloudToRain.png"],
        [detail.find("曇一時雪") != -1 or (detail.find("曇のち雪")) != -1 or (detail.find("曇時々雪")) != -1, "cloudToSnow.jpg"],
        [detail.find("雨") != -1 and (detail.find("晴")) == -1 and (detail.find("曇")) == -1 and (detail.find("雪")) == -1, "rain.png"],
        [detail.find("雨一時晴") != -1 or (detail.find("雨のち晴")) != -1 or (detail.find("雨時々晴")) != -1, "rainToSunny.jpg"],
        [detail.find("雨一時曇") != -1 or (detail.find("雨のち曇")) != -1 or (detail.find("雨時々曇")) != -1, "rainToCloud.png"],
        [detail.find("雨一時雪") != -1 or (detail.find("雨のち雪")) != -1 or (detail.find("雨時々雪")) != -1, "rainToSnow.png"],
        [detail.find("雪") != -1 and (detail.find("晴")) == -1 and (detail.find("雨")) == -1 and (detail.find("曇")) == -1, "snow.png"],
        [detail.find("雪一時晴") != -1 or (detail.find("雪のち晴")) != -1 or (detail.find("雪時々晴")) != -1, "snowToSunny.jpg"],
        [detail.find("雪一時曇") != -1 or (detail.find("雪のち曇")) != -1 or (detail.find("雪時々曇")) != -1, "snowToCloud.jpg"],
        [detail.find("雪一時雨") != -1 or (detail.find("雪のち雨")) != -1 or (detail.find("雪時々雨")) != -1, "snowToRain.jpg"],
        [detail.find("暴風雨") == -1, "typhon.png"],
        [detail.find("暴風雪") == -1, "heavySnow.jpg"],
    ]:
        if boolean:
            files = {'imageFile': open(iconPath + fileName, "rb")}
            requests.post(lineNotifyApi, data=payload, headers=headers, files=files)
            isFind = True
            break

    if not isFind:
        requests.post(lineNotifyApi, data=payload, headers=headers)


## メイン処理 ###################################################################################

# 天気予報サイトのHTMLタグから天気情報を抽出
parser(rssUrl)
for idx in range(0, perDay):
    payload = {'message': "\n" + titleList[idx]}
    headers = {'Authorization': 'Bearer ' + lineNotifyToken}

    # 天気情報とそれに応じた天気アイコンを出力
    ckWeather(descList[idx])

# Notify URL
payload = {'message': URL}
headers = {'Authorization': 'Bearer ' + lineNotifyToken}
requests.post(lineNotifyApi, data=payload, headers=headers)

################################################################################################
