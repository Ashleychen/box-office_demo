#coding=UTF-8
import os
import urlparse
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import json

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

import basic_funcs
import reading
import daily_pre
import get_history_box
import get_battle
import get_week

daily_dict = {}
daily_first_dict = {}
daily_next_dict = {}
summary = {}
#总票房预测
total_first_list = []
total_basic_list = []
total_basic_dict = {}
total_first_dict = {}
min_first_date = ''
max_first_date = ''
first_feas_dict = {}
basic_feas_dict = {}
first_movie_dict = {}
first_err_dict = {}
basic_anal_dict = {}
#当日误差
daily_min_date = ''
daily_max_date = ''
first_day_ids = {}
before_day_ids = {}
acc_dict = {}
dict_by_movie = {}
shuneng_dict = {}
first_start_date = ''
first_end_date = ''
#误差列表
top5_err_by_weekday = []
total_err_by_weekday = []
summary_err_total = 0.0
acc_err_total = []
mix_top5_err_total = []
mix_total_err_total = []
first_top5_err_total = []
first_total_err_total = []
next_top5_err_total = []
next_total_err_total = []
#echart旁边的列表
err_A_by_date = []
err_B_by_date = []
summary_err_by_date = 0.0
acc_err_A_by_date = 0.0
acc_err_B_by_date = 0.0
#排片率预测
scr_by_movie = {}
#巅峰对决
battle_daily_dict = {}
battle_first_date = ''
battle_last_date = ''
battleDateList = []
aveList = []
#周票房预测
boxoffice_summary_week_dict = {}
max_pre_date = ''
min_pre_date = ''
limit_boxoffice_mv_dict = {}
weekly_err_list = []

class MovieHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html')
    def post(self):
        choice = self.get_argument("choice")
	if choice == '1':
	    self.write({'maxDate': daily_max_date, 'minDate': daily_min_date})
	if choice == '2':
            the_day = self.get_argument("theDay")
    	    daily_list = daily_pre.get_daily_pre(daily_dict, summary, the_day)
    	    #首日票房预测->当日误差
    	    err_A_by_date, err_B_by_date, summary_err_by_date,\
            	acc_err_A_by_date, acc_err_B_by_date, range_list =\
            	daily_pre.get_err_by_date(daily_dict, summary, the_day, before_day_ids)
	    if the_day in first_day_ids.keys():
	    	first_day_list = first_day_ids[the_day]
	    else:
	    	first_day_list = []
	    if the_day in before_day_ids.keys():
	    	before_day_list = before_day_ids[the_day]
	    else:
	    	before_day_list = []
	    self.write({'firstDayList': first_day_list, 'beforeDayList': before_day_list,\
		'dailyList': daily_list, 'errADate': err_A_by_date, 'summaryErrDate': summary_err_by_date,\
		'accErrDate': acc_err_A_by_date, 'errRangeList': range_list})
	if choice == '3':
            self.write({'top5ErrWeekday': top5_err_by_weekday, 'totalErrWeekday': total_err_by_weekday,\
	    	'summaryErrTotal': summary_err_total, 'accErrTotal': acc_err_total,\
	    	'mixTop5ErrTotal': mix_top5_err_total, 'mixTotalErrTotal': mix_total_err_total,\
	    	'firstTop5ErrTotal': first_top5_err_total, 'firstTotalErrTotal': first_total_err_total,\
	    	'nextTop5ErrTotal': next_top5_err_total, 'nextTotalErrTotal': next_total_err_total,\
	    })

class wholeBoxHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('wholeBox.bak.html') 
    def post(self):
	choice = self.get_argument('choice').encode('utf-8')
	if choice == '1':
	    self.write({'firstMinDate': min_first_date, 'firstMaxDate': max_first_date, 'firstMovieDict': first_movie_dict, 'firstErrDict': first_err_dict, 'basicAnalDict': basic_anal_dict})
	if choice == '2':
	    pre_date = self.get_argument('preDate').encode('utf-8')
	    total_first_list = get_history_box.get_first_list(total_first_dict, shuneng_dict, pre_date)
	    self.write({'totalFirstList': total_first_list, 'firstFeasDict': first_feas_dict})

class deepHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('deepAnal.html') 
    def post(self):
	choice = self.get_argument('choice').encode('utf-8')
	if choice == '1':
	    basic_start_date = self.get_argument('startDate').encode('utf-8')
	    basic_end_date = self.get_argument('endDate').encode('utf-8')
	    total_basic_list = get_history_box.get_basic_list(total_basic_dict, basic_start_date, basic_end_date)
	    self.write({'totalBasicList': total_basic_list, 'basicFeasDict': basic_feas_dict, 'basicAnalDict': basic_anal_dict})

class seqTrendHandler(tornado.web.RequestHandler):
    def get(self):
	mv_name = self.get_argument('filmName').encode('utf-8')
	date_list = [item[0] for item in scr_by_movie[mv_name]]
	seq_list = [item[4] for item in scr_by_movie[mv_name]]
	self.write({'dateList': date_list, 'seqRate': seq_list})

class weekHandler(tornado.web.RequestHandler):
    def get(self):
	self.render('week.html')
    def post(self):
	self.write({'boxofficeSummaryWeekDict':boxoffice_summary_week_dict, 'maxPreDate': max_pre_date, 'minPreDate':min_pre_date, 'limitBoxofficeMVDict': limit_boxoffice_mv_dict, 'weeklyErrList': weekly_err_list})

class battleHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('battle.html') 
    def post(self):
	self.write({'firstDate':battle_first_date, 'lastDate': battle_last_date, 'dates': battleDateList, 'bdRates': aveList, 'dict':battle_daily_dict})

class battleErrHandler(tornado.web.RequestHandler):
    def get(self):
	err_start_date = self.get_argument('startDate').encode('utf-8')
	err_end_date = self.get_argument('endDate').encode('utf-8')
	battle_err_list = get_battle.battle_errs(summary, daily_dict, first_day_ids, before_day_ids, err_start_date, err_end_date)
	self.write({'battleErrs':battle_err_list})

class lmainHandler(tornado.web.RequestHandler):
    def get(self):
	film_name = self.get_argument('filmName').encode('utf-8')
	date_list, pre_A_list, pre_B_list, real_list = daily_pre.get_multiple_list(film_name, dict_by_movie, summary, acc_dict)
	self.write({'dateList':date_list, 'preAList':pre_A_list, 'realList':real_list, 'preBList':pre_B_list})

if __name__ == "__main__":
    tornado.options.parse_command_line()
    #首日票房预测
    #排片率预测
    daily_dict, daily_first_dict, daily_next_dict, summary, \
	total_basic_dict, total_first_dict, daily_min_date, daily_max_date, \
	first_day_ids, before_day_ids = reading.read_files()
    #单部电影票房趋势
    acc_dict = daily_pre.get_acc_dict(daily_dict, summary)
    dict_by_movie = daily_pre.group_by_film(daily_dict, before_day_ids)
    #首日票房预测->TOP5误差
    top5_err_by_weekday = daily_pre.get_top5_err_by_weekday(daily_dict, before_day_ids)
    #首日票房预测->电影整体误差
    total_err_by_weekday = daily_pre.get_total_err_by_weekday(daily_dict, before_day_ids)
    #首日票房预测->其余误差指标
    summary_err_total, acc_err_total, mix_top5_err_total,\
        mix_total_err_total, first_top5_err_total, first_total_err_total,\
        next_top5_err_total, next_total_err_total = \
	daily_pre.get_err_total(daily_dict, daily_first_dict, daily_next_dict, summary, first_day_ids, before_day_ids)
    #总票房预测
    total_first_dict = get_history_box.get_total_boxoffice_dict(total_first_dict)
    shuneng_dict = get_history_box.get_shuneng_dict()
    min_first_date = min(total_first_dict.keys())
    max_first_date = max(total_first_dict.keys())
    first_feas_dict = get_history_box.get_feas(total_first_dict)
    basic_feas_dict = get_history_box.get_feas(total_basic_dict)
    first_movie_dict = get_history_box.get_movie_multi_pre_dict(total_first_dict, shuneng_dict)
    first_err_dict = get_history_box.get_on_days_errs(total_first_dict, shuneng_dict)
    basic_anal_dict = get_history_box.get_analysis(total_basic_dict)
    #巅峰对决
    battle_daily_dict, battle_first_date, battle_last_date = get_battle.battle_score(daily_dict)
    battleDateList, aveList = get_battle.movingAve(battle_daily_dict)
    #周票房预测
    boxoffice_summary_week_dict = get_week.append_shuneng_pre()
    max_pre_date, min_pre_date = get_week.get_max_date_range(boxoffice_summary_week_dict)
    limit_boxoffice_mv_dict = get_week.get_boxoffice_week() 
    weekly_err_list = get_week.getWeekLlyErrList(boxoffice_summary_week_dict)
    app = tornado.web.Application(handlers=[
	(r"/", MovieHandler), (r"/lmain", lmainHandler),\
	(r"/wholeBox", wholeBoxHandler),\
	(r"/seqTrend", seqTrendHandler),\
	(r"/battle", battleHandler),\
	(r"/battleErr", battleErrHandler),\
	(r"/week", weekHandler),\
	(r"/deep", deepHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "src", "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "src", "static"),
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
