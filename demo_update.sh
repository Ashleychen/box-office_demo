#!/bin/bash
#! ~/liuchu/tools/scmtools/usr/bin/python
source /etc/profile
cd /home/work/chenyaxue/movie/
rm demo_start.py
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/demo_start.py
rm get_data.py
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/get_data.py
#rm get_error.py
#wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/get_error.py
#rm get_history_box.py
#wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/get_history_box.py
#cd /home/work/chenyaxue/movie/src/templates/
#rm test.html
#wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/templates/test.html
#rm wholeBox.html
#wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/templates/wholeBox.html
#rm screening.html
#wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/templates/screening.html
cd /home/work/chenyaxue/movie/src/static/screening
rm basic.function.js
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/static/screening/basic.function.js
rm daily.screening.js
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/static/screening/daily.screening.js
rm display.table.js
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/static/screening/display.table.js
rm screening.chart.js
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/static/screening/screening.chart.js
cd /home/work/chenyaxue/movie/src/static/
rm basic.function.js
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/static/basic.function.js
rm daily.predict.box.error.js
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/static/daily.predict.box.error.js
rm display.table.js
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/static/display.table.js
rm trend_chart.js
wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/static/trend_chart.js
#cd /home/work/chenyaxue/movie/src/static/wholeBox/
#rm *
#wget ftp://szwg-rp-nlp345.szwg01.baidu.com/home/work/chenyaxue/iter/src/static/wholeBox/*
cd /home/work/chenyaxue/movie/data
rm boxoffice_day.txt
rm boxoffice_day1.txt
rm boxoffice_day2.txt
rm total_boxoffice_day.txt
rm boxoffice_first_day.txt
rm boxoffice_first_day1.txt
rm boxoffice_first_day2.txt
rm nor_seq_num_rate_first_day_single_movie.txt
wget http://10.95.36.53:8888/boxoffice_day.txt
wget http://10.95.36.53:8888/boxoffice_day1.txt
wget http://10.95.36.53:8888/boxoffice_day2.txt
wget http://10.95.36.53:8888/total_boxoffice_day.txt
wget http://10.95.36.53:8888/boxoffice_first_day1.txt
wget http://10.95.36.53:8888/boxoffice_first_day2.txt
wget http://10.95.36.53:8888/nor_seq_num_rate_first_day_single_movie.txt
lines=$(ps aux | grep "python demo_start.py" | awk 'END{print NR}')
echo $lines
check_str="/home/work/liuchu/tools/scmtools/usr/bin/pythondemo_start.py"
for((i=1;i<=$lines;i++))
do
    str1=$(ps aux | grep "python demo_start.py" | sed -n "$i, 1p" | awk -F' ' '{ print $11 }')
    str2=$(ps aux | grep "python demo_start.py" | sed -n "$i, 1p" | awk -F' ' '{ print $12 }')
    str="$str1""$str2"
    echo $str
    if [ "${str}" = "${check_str}" ];then
        pid=$(ps aux | grep "python demo_start.py" | sed -n "$i, 1p" | awk -F' ' '{ print $2 }')
        echo $pid
        kill $pid
    fi
done
cd /home/work/chenyaxue/movie
nohup ~/liuchu/tools/scmtools/usr/bin/python demo_start.py
