#coding=utf-8

import datetime
import heapq
import math

weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']

def get_date():
    cur_date = datetime.date.today()
    cur_weekday = cur_date.weekday()
    delta_days = datetime.timedelta(days=1)
    next_date = cur_date + delta_days
    next_weekday = next_date.weekday()
    after_date = next_date + delta_days
    after_weekday = after_date.weekday()
    return (str(cur_date), weekdays[cur_weekday],\
            str(next_date), weekdays[next_weekday],\
            str(after_date), weekdays[after_weekday])

def get_weekday(the_date):
    weekday_ind =  datetime.datetime.strptime(the_date, '%Y-%m-%d').weekday()
    return weekday_ind

def get_err_by_real(pre, real):
    err = math.fabs(float(pre) - float(real)) / float(real)
    return err

def get_err_by_min(pre, real):
    down = min(float(pre), float(real))
    err = math.fabs(float(pre) - float(real)) / float(down)
    return err

def get_err_by_list(baidu_list):
    tuple_list = [(item['basics'][4], item['basics'][5], item['basics'][7]) for item in baidu_list]
    err_A_list = [get_err_by_real(t[0], t[1]) for t in tuple_list if t[0] != '--' and t[1] != '--']
    err_B_list = [get_err_by_real(t[2], t[1]) for t in tuple_list if t[2] != '--' and t[1] != '--']
    err_A = 0.0
    err_B = 0.0
    err_A += sum(err_A_list)
    err_B += sum(err_B_list)
    return err_A, len(err_A_list), err_B, len(err_B_list)

def get_ave_err(total_err, err_size):
    if err_size != 0:
	return total_err / err_size
    else:
	return -1.0

def get_top5_by_ind(the_list, ind):
    top5_list = heapq.nlargest(5, the_list, key=lambda c: float(c['basics'][ind]))
    return top5_list

def update_winner(winner, winner_list, win_side, lose_side, ind):
    win_side.append(5 - ind)
    lose_side.append(0)
    winner_list.append(winner)

def get_trend_list(raw_list):
    trend_list = ['-' if x == '--' else x for x in raw_list]
    return trend_list

def is_name_existed(name_list, real_list, name):
    words_list = [set(n) for n in name_list]
    name_set = set(name)
    len_list = [len(name_set.intersection(w)) for w in words_list]
    pair_list = zip(len_list, range(len(len_list)))
    pair_list.sort(key=lambda x: x[0], reverse=True)
    if len(pair_list) > 0 and pair_list[0][0] >= len(name_set) * 0.6 and pair_list[0][0] >= len(words_list[pair_list[0][1]]) * 0.6:
	return True, real_list[pair_list[0][1]], pair_list[0][1]
    else:
	return False, '--', -1

def cmp_name_with_shuneng_list(name_list, data_list, name):
    name_list = [n.decode('utf-8') for n in name_list]
    words_list = [set(n) for n in name_list]
    name_set = set(name.decode('utf-8'))
    len_list = [len(name_set.intersection(w)) for w in words_list]
    pair_list = zip(len_list, range(len(len_list)))
    pair_list.sort(key=lambda x: x[0], reverse=True)
    if len(pair_list) > 0 and ((pair_list[0][0] >= len(name_set) * 0.6 and pair_list[0][0] >= len(words_list[pair_list[0][1]]) * 0.6) or pair_list[0][0] >= 4):
        return True, data_list[pair_list[0][1]], pair_list[0][1]
    else:
        return False, '--', -1

def get_days_delta(start_date, end_date):
    start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    return (end_datetime - start_datetime).days

def get_days_delta_from_today(start_date):
    start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    today_datetime = datetime.datetime.now()
    return (today_datetime - start_datetime).days

def is_float_zero(float_str, float_flag):
    if math.fabs(float(float_str) - float(float_flag)) < 1e-9:
	return True
    else:
	return False
