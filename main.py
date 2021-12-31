#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.request
from datetime import datetime
import os
import isodate


def checkYear(time, year):
    try:
        date_to_check = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        date_to_check = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

    return date_to_check.year == year


def getVideoLength(url):
    temp = url.split('?v=')
    video_id = temp[-1]
    api_key = "PutKeyHere!"  # get a key for free from https://console.developers.google.com/
    searchUrl = (
            "https://www.googleapis.com/youtube/v3/videos?id="
            + video_id
            + "&key="
            + api_key
            + "&part=contentDetails"
    )
    response = urllib.request.urlopen(searchUrl).read()
    data = json.loads(response)
    all_data = data["items"]
    try:
        contentDetails = all_data[0]["contentDetails"]
        duration = contentDetails["duration"]
        duration = isodate.parse_duration(duration)
        video_dur = duration.total_seconds()
        return video_dur
    except:
        return 0


def run(year, file):
    results = dict()
    with open(file, encoding='utf-8') as f:
        data = json.load(f)
    for video in data:
        try:
            url = video["titleUrl"]
        except KeyError:
            pass  # lazy handling, but usually video was deleted

        if checkYear(video["time"], year):
            if "subtitles" not in video:
                pass
            else:
                youtuber = video["subtitles"][0]["name"]
                if youtuber in results:
                    results[youtuber] += getVideoLength(url)
                else:
                    results[youtuber] = getVideoLength(url)
    top = sorted(results, key=results.get, reverse=True)
    for v in top:
        print(v, results[v])
    #get the sum of the video lengths
    sum = 0
    for v in top:
        sum += results[v]
    print("Sum:", sum)




if __name__ == "__main__":
    run(2021, "watch-history.json")  # get it from google takeout and copy the file path
