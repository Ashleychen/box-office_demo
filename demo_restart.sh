#!/bin/bash
#! /home/work/.jumbo/bin/python
source /etc/profile
cd /home/work/chenyaxue/movie/data
rm boxoffice_first_day1.txt
rm boxoffice_next_day1.txt
rm boxoffice_summary_day.txt
rm total_boxoffice_playdate_smooth.txt
rm total_boxoffice_playdate.txt
rm total_boxoffice_basic_info.txt
rm boxoffice_first_day2.txt
rm boxoffice_next_day2.txt
rm boxoffice_before_first_day.txt
rm shuneng_pred
rm shuneng_air
rm shuneng_week
rm boxoffice_summary_week.txt
rm boxoffice_week.txt
wget http://10.95.36.53:8888/boxoffice_first_day1.txt
wget http://10.95.36.53:8888/boxoffice_next_day1.txt
wget http://10.95.36.53:8888/boxoffice_summary_day.txt
wget http://10.95.36.53:8888/total_boxoffice_playdate_smooth.txt
wget http://10.95.36.53:8888/total_boxoffice_playdate.txt
wget http://10.95.36.53:8888/total_boxoffice_basic_info.txt
wget http://10.95.36.53:8888/boxoffice_first_day2.txt
wget http://10.95.36.53:8888/boxoffice_next_day2.txt
wget http://10.95.36.53:8888/boxoffice_before_first_day.txt
wget http://10.95.36.53:8888/boxoffice_summary_week.txt
wget http://10.95.36.53:8888/boxoffice_week.txt
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/shuneng/shuneng_pred
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/shuneng/shuneng_air
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/shuneng/shuneng_week
lines=$(ps aux | grep "python movie_start.py" | awk 'END{print NR}')
echo $lines
check_str="/home/work/.jumbo/bin/pythonmovie_start.py"
for((i=1;i<=$lines;i++))
do
    str1=$(ps aux | grep "python movie_start.py" | sed -n "$i, 1p" | awk -F' ' '{ print $11 }')
    str2=$(ps aux | grep "python movie_start.py" | sed -n "$i, 1p" | awk -F' ' '{ print $12 }')
    str="$str1""$str2"
    echo $str
    if [ "${str}" = "${check_str}" ];then
        pid=$(ps aux | grep "python movie_start.py" | sed -n "$i, 1p" | awk -F' ' '{ print $2 }')
        echo $pid
        kill $pid
    fi
done
cd /home/work/chenyaxue/movie
rm nohup.out
nohup /home/work/.jumbo/bin/python movie_start.py
