#coding=utf-8

import basic_funcs

def get_acc(daily_dict, summary, the_day, ind, real_seq):
    acc = '--'
    pre_list = [float(daily_dict[the_day][item]['basics'][ind]) for item in daily_dict[the_day].keys() if daily_dict[the_day][item]['basics'][ind] != '--' and daily_dict[the_day][item]['basics'][6] != '-']
    mv_seqs = [float(daily_dict[the_day][item]['basics'][6]) for item in daily_dict[the_day].keys() if daily_dict[the_day][item]['basics'][ind] != '--' and daily_dict[the_day][item]['basics'][6] != '-']
    if len(mv_seqs) != 0:
    	acc = round(sum(pre_list) / sum(mv_seqs) * float(real_seq), 1)
    return acc

def get_acc_list(daily_dict, summary, the_day):
    real_b = '--'
    if the_day not in summary.keys():
	return ['--', '--', '--']
    real_seq = summary[the_day][3]
    acc_A = get_acc(daily_dict, summary, the_day, 4, real_seq)
    acc_B = get_acc(daily_dict, summary, the_day, 7, real_seq)
    try:
	real_b = float(summary[the_day][2])
    except:
	pass
    return [acc_A, acc_B, real_b]

#当日预测票房与实际票房比较
def get_daily_pre(daily_dict, summary, the_day):
    daily_list = []
    if the_day in daily_dict.keys():
    	daily_list = [daily_dict[the_day][id] for id in daily_dict[the_day]]
    	try:
            daily_list.sort(key=lambda item: float(item['basics'][6]), reverse=True)
            acc_list = get_acc_list(daily_dict, summary, the_day)
            daily_list.insert(0, acc_list)
    	except:
	    print 'get_daily_pre err..'	
	if the_day in summary.keys():
            summary_list = summary[the_day]
	else:
	    summary_list = [the_day, '--', '--', '--']
        daily_list.insert(0, summary_list)
    return daily_list

def get_daily_list(raw_dict, the_day):
    daily_list = [raw_dict[the_day][id] for id in raw_dict[the_day]]
    daily_list.sort(key=lambda item: float(item['basics'][6]), reverse=True)
    return daily_list

#TOP5误差
def get_top5_err_by_weekday_by_ind(daily_dict, before_day_ids, ind):
    pre_list = [[], [], [], [], [], [], []]
    real_list = [[], [], [], [], [], [], []] 
    for d in daily_dict.keys():
	daily_list = [item for item in get_daily_list(daily_dict, d) if item['basics'][5] != '-']
	top5_list = basic_funcs.get_top5_by_ind(daily_list, 5)
	if d in before_day_ids.keys():
	    top5_list = [item for item in top5_list if item['basics'][1] not in before_day_ids[d]]
	weekday_ind = basic_funcs.get_weekday(d)
	pre_list[weekday_ind].extend([float(item['basics'][ind]) for item in top5_list if item['basics'][ind] != '--'])
	real_list[weekday_ind].extend([float(item['basics'][5]) for item in top5_list if item['basics'][ind] != '--'])
    err_list = [0.0] * 7
    size_list = [0] * 7
    for weekday_ind in xrange(7):
	size_list[weekday_ind] = len(pre_list[weekday_ind])
	for ind in xrange(size_list[weekday_ind]):
	    err_list[weekday_ind] += basic_funcs.get_err_by_real(pre_list[weekday_ind][ind], real_list[weekday_ind][ind])
	weekday_err = err_list[weekday_ind] / size_list[weekday_ind]
	err_list[weekday_ind] = weekday_err
    return err_list

def get_top5_err_by_weekday(daily_dict, before_day_ids):
    err_A = get_top5_err_by_weekday_by_ind(daily_dict, before_day_ids, 4)
    err_B = get_top5_err_by_weekday_by_ind(daily_dict, before_day_ids, 7)
    return err_A + err_B

#电影整体误差
def get_total_err_by_weekday_by_ind(daily_dict, before_day_ids, ind):
    pre_list = [[], [], [], [], [], [], []]
    real_list = [[], [], [], [], [], [], []]
    for d in daily_dict.keys():
        daily_list = [item for item in get_daily_list(daily_dict, d) if item['basics'][5] != '-']
	if d in before_day_ids.keys():
	    daily_list = [item for item in daily_list if item['basics'][1] not in before_day_ids[d]]
        weekday_ind = basic_funcs.get_weekday(d)
        pre_list[weekday_ind].extend([float(item['basics'][ind]) for item in daily_list if item['basics'][ind] != '--'])
        real_list[weekday_ind].extend([float(item['basics'][5]) for item in daily_list if item['basics'][ind] != '--'])
    err_list = [0.0] * 7
    size_list = [0] * 7
    for weekday_ind in xrange(7):
        size_list[weekday_ind] = len(pre_list[weekday_ind])
        for ind in xrange(size_list[weekday_ind]):
            err_list[weekday_ind] += basic_funcs.get_err_by_real(pre_list[weekday_ind][ind], real_list[weekday_ind][ind])
        weekday_err = err_list[weekday_ind] / size_list[weekday_ind]
        err_list[weekday_ind] = weekday_err
    return err_list

def get_total_err_by_weekday(daily_dict, before_day_ids):
    err_A = get_total_err_by_weekday_by_ind(daily_dict, before_day_ids, 4)
    err_B = get_total_err_by_weekday_by_ind(daily_dict, before_day_ids, 7)
    return err_A + err_B

#其余误差指标
def get_top5_err_total_by_ind(top5_list, ind): 
    err = 0.0
    pre_list = [float(item['basics'][ind]) for item in top5_list if item['basics'][ind] != '--']
    real_list = [float(item['basics'][5]) for item in top5_list if item['basics'][ind] != '--']
    for ind in xrange(len(pre_list)):
	err += basic_funcs.get_err_by_real(pre_list[ind], real_list[ind])
    return err, len(pre_list)

def get_top5_err_total(daily_dict, first_day_ids, before_day_ids): 
    err_A = 0.0
    err_B = 0.0
    err_size_A = 0
    err_size_B = 0
    first_err_A = 0.0
    first_err_B = 0.0
    first_err_size_A = 0
    first_err_size_B = 0
    next_err_A = 0.0
    next_err_B = 0.0
    next_err_size_A = 0
    next_err_size_B = 0
    for d in daily_dict.keys():
        daily_list = [item for item in get_daily_list(daily_dict, d) if item['basics'][5] != '-']
	top5_list = basic_funcs.get_top5_by_ind(daily_list, 5)
	if d in before_day_ids.keys():
	    top5_list = [item for item in top5_list if item['basics'][1] not in before_day_ids[d]]
	if d in first_day_ids.keys():
	    first_top5_list = [item for item in top5_list if item['basics'][1] in first_day_ids[d]]
	    next_top5_list = [item for item in top5_list if item['basics'][1] not in first_day_ids[d]]
	else:
	    first_top5_list = []
	    next_top5_list = top5_list
	daily_err, daily_len = get_top5_err_total_by_ind(top5_list, 4)
	err_A += daily_err
	err_size_A += daily_len
	daily_err, daily_len = get_top5_err_total_by_ind(top5_list, 7)
	err_B += daily_err
	err_size_B += daily_len
	daily_err, daily_len = get_top5_err_total_by_ind(first_top5_list, 4)
	first_err_A += daily_err
    	first_err_size_A += daily_len
	daily_err, daily_len = get_top5_err_total_by_ind(first_top5_list, 7)
	first_err_B += daily_err
    	first_err_size_B += daily_len
	daily_err, daily_len = get_top5_err_total_by_ind(next_top5_list, 4)
	next_err_A += daily_err
    	next_err_size_A += daily_len
	daily_err, daily_len = get_top5_err_total_by_ind(next_top5_list, 7)
	next_err_B += daily_err
    	next_err_size_B += daily_len
    err_A = basic_funcs.get_ave_err(err_A, err_size_A)
    err_B = basic_funcs.get_ave_err(err_B, err_size_B)
    first_err_A = basic_funcs.get_ave_err(first_err_A, first_err_size_A)
    first_err_B = basic_funcs.get_ave_err(first_err_B, first_err_size_B)
    next_err_A = basic_funcs.get_ave_err(next_err_A, next_err_size_A)
    next_err_B = basic_funcs.get_ave_err(next_err_B, next_err_size_B)
    return [err_A, err_B], [first_err_A, first_err_B], [next_err_A, next_err_B]

def get_total_err_total_by_ind(raw_dict, before_day_ids, ind):
    err = 0.0
    err_size = 0
    for d in raw_dict.keys():
        daily_list = [item for item in get_daily_list(raw_dict, d) if item['basics'][5] != '-']
	if d in before_day_ids.keys():
	    daily_list = [item for item in daily_list if item['basics'][1] not in before_day_ids[d]]
	pre_list = [float(item['basics'][ind]) for item in daily_list if item['basics'][ind] != '--']
	real_list = [float(item['basics'][5]) for item in daily_list if item['basics'][ind] != '--']
	for i in xrange(len(pre_list)):
	    err += basic_funcs.get_err_by_real(pre_list[i], real_list[i])
	err_size += len(pre_list)
    err = basic_funcs.get_ave_err(err, err_size)
    return err

def get_total_err_total(raw_dict, before_day_ids):
    err_A = get_total_err_total_by_ind(raw_dict, before_day_ids, 4)
    err_B = get_total_err_total_by_ind(raw_dict, before_day_ids, 7)
    return err_A, err_B

def get_summary_err_total(summary):
    err = 0.0
    size = 0
    pre = [summary[d][1] for d in summary.keys()]
    real = [summary[d][2] for d in summary.keys()]
    for ind in xrange(len(pre)):
	try:
	    err += basic_funcs.get_err_by_real(pre[ind], real[ind])
	    size += 1
	except:
	    continue
    if size != 0:
    	err /= size
    return err

def get_acc_err_total(daily_dict, summary):
    err_A = 0.0
    err_B = 0.0
    size_A = 0
    size_B = 0
    for d in daily_dict:
	acc_list = get_acc_list(daily_dict, summary, d)
	if acc_list[0] != '--' and acc_list[2] != '--':
	    err_A += basic_funcs.get_err_by_real(acc_list[0], acc_list[2])
	    size_A += 1
	if acc_list[1] != '--' and acc_list[2] != '--':
	    err_B += basic_funcs.get_err_by_real(acc_list[1], acc_list[2])
	    size_B += 1
    err_A = basic_funcs.get_ave_err(err_A, size_A)
    err_B = basic_funcs.get_ave_err(err_B, size_B)
    return err_A, err_B

def get_err_total(daily_dict, daily_first_dict, daily_next_dict, summary, first_day_ids, before_day_ids):
    mix_top5_err_total, first_top5_err_total, next_top5_err_total = get_top5_err_total(daily_dict, first_day_ids, before_day_ids)
    mix_total_err_total = get_total_err_total(daily_dict, before_day_ids)
    first_total_err_total = get_total_err_total(daily_first_dict, before_day_ids)
    next_total_err_total = get_total_err_total(daily_next_dict, before_day_ids)
    summary_err_total = get_summary_err_total(summary)
    acc_err_total = get_acc_err_total(daily_dict, summary)
    return summary_err_total, acc_err_total, mix_top5_err_total,\
	mix_total_err_total, first_top5_err_total, first_total_err_total,\
	next_top5_err_total, next_total_err_total

#单部电影票房趋势
def group_by_film(daily_dict, before_day_ids):
    dict_by_movie = {}
    for d in daily_dict.keys():
	for id in daily_dict[d].keys():
	    if d in before_day_ids.keys() and id in before_day_ids[d]:
		continue
	    if daily_dict[d][id]['basics'][3] not in dict_by_movie.keys():
		dict_by_movie[daily_dict[d][id]['basics'][3]] = []
	    dict_by_movie[daily_dict[d][id]['basics'][3]].append(daily_dict[d][id]['basics'])
    for name in dict_by_movie.keys():
	dict_by_movie[name].sort(key=lambda x:x[0])
    return dict_by_movie

def get_acc_dict(daily_dict, summary):
    acc_dict = {}
    for d in daily_dict:
    	acc_list = get_acc_list(daily_dict, summary, d)
	acc_dict[d] = acc_list
    return acc_dict

def get_multiple_list(film_name, dict_by_movie, summary, acc_dict):
    if film_name == '大盘':
	date_list = summary.keys()
	date_list.sort()
	pre_A_list = basic_funcs.get_trend_list([summary[d][1] for d in date_list])
	pre_B_list = pre_A_list
	real_list = basic_funcs.get_trend_list([summary[d][2] for d in date_list])
    elif film_name == '大盘(累积)':
	date_list = acc_dict.keys()
	date_list.sort()
	pre_A_list = basic_funcs.get_trend_list([acc_dict[d][0] for d in date_list])
	pre_B_list = basic_funcs.get_trend_list([acc_dict[d][1] for d in date_list])
	real_list = basic_funcs.get_trend_list([acc_dict[d][2] for d in date_list])
    else:
	mv_list = dict_by_movie[film_name]
	mv_list.sort(key=lambda x: x[0])
	date_list = [item[0] for item in mv_list]
	pre_A_list = basic_funcs.get_trend_list([item[4] for item in mv_list])
	pre_B_list = basic_funcs.get_trend_list([item[7] for item in mv_list])
	real_list = basic_funcs.get_trend_list([item[5] for item in mv_list])
    return date_list, pre_A_list, pre_B_list, real_list

#当日误差
def get_err_by_date(daily_dict, summary, the_day, before_day_ids):
    acc_list = get_acc_list(daily_dict, summary, the_day)
    range_list = [(0, 100), (100, 1000), (1000, 5000), (5000, -1)]
    range_size = len(range_list)
    err_A = [0.0] * range_size
    err_B = [0.0] * range_size
    size_A = [0] * range_size
    size_B = [0] * range_size
    if the_day in summary.keys() and summary[the_day][1] != '-' and summary[the_day][2] != '-':
        summary_err_by_date = basic_funcs.get_err_by_real(summary[the_day][1], summary[the_day][2])
    else:
        summary_err_by_date = -1.0
    if acc_list[0] != '--' and acc_list[2] != '--':
        acc_err_A_by_date = basic_funcs.get_err_by_real(acc_list[0], acc_list[2])
    else:
        acc_err_A_by_date = -1.0 
    if acc_list[1] != '--' and acc_list[2] != '--':
        acc_err_B_by_date = basic_funcs.get_err_by_real(acc_list[1], acc_list[2])
    else:
        acc_err_B_by_date = -1.0
    if the_day not in daily_dict.keys():
    	return err_A, err_B, summary_err_by_date, acc_err_A_by_date, acc_err_B_by_date, range_list
    for id in daily_dict[the_day]:
	if the_day in before_day_ids.keys() and id in before_day_ids[the_day]:
	    continue
	if daily_dict[the_day][id]['basics'][5] != '-' and daily_dict[the_day][id]['basics'][4] != '--':
	    for range_ind in xrange(range_size):
	    	if float(daily_dict[the_day][id]['basics'][5]) < range_list[range_ind][1] or range_ind == range_size - 1:
		    err_A[range_ind] += basic_funcs.get_err_by_real(daily_dict[the_day][id]['basics'][4], daily_dict[the_day][id]['basics'][5])
		    size_A[range_ind] += 1
		    break
	if daily_dict[the_day][id]['basics'][5] != '-' and daily_dict[the_day][id]['basics'][7] != '--':
	    for range_ind in xrange(range_size):
	    	if float(daily_dict[the_day][id]['basics'][5]) < range_list[range_ind][1] or range_ind == range_size - 1:
		    err_B[range_ind] += basic_funcs.get_err_by_real(daily_dict[the_day][id]['basics'][7], daily_dict[the_day][id]['basics'][5])
		    size_B[range_ind] += 1
		    break
    for range_ind in xrange(range_size):
	err_A[range_ind] = basic_funcs.get_ave_err(err_A[range_ind], size_A[range_ind])
	err_B[range_ind] = basic_funcs.get_ave_err(err_B[range_ind], size_B[range_ind])
    return err_A, err_B, summary_err_by_date, acc_err_A_by_date, acc_err_B_by_date, range_list
