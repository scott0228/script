#!/bin/bash
# 先取得 SSID
ssid=$(networksetup -getairportnetwork en1 | cut -c 24-)

# 依 SSID 決定要用哪個 location ，可利用 scselect 指令來列出所有的 location
if [ $ssid = "ScottAP" ]
then
    location="Work"
else
    location="Automatic"
fi

# 更新 location
newloc=`/usr/sbin/scselect ${location} | sed 's/^.*(\(.*\)).*$/\1/'`
echo ${newloc}

# 辨斷是否正確來回撌值
if [ ${location} != ${newloc} ]
then
    exit 1
fi

exit 0
