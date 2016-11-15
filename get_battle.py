#coding=utf-8

import json
import math
import sys
import basic_funcs

import basic_funcs
import daily_pre

reload(sys)
sys.setdefaultencoding('utf-8')

def read_shuneng():
    with open('/home/work/chenyaxue/movie/data/shuneng_pred') as s_f:
        line = s_f.readline()
        line_json = json.loads(line)
    return line_json

def single_score(daily_dict, shuneng_dict, cur_date):
    if cur_date not in daily_dict.keys():
	return []
    daily_list = [daily_dict[cur_date][id] for id in daily_dict[cur_date] if daily_dict[cur_date][id]['basics'][5] != '-']
    daily_top5 = basic_funcs.get_top5_by_ind(daily_list, 5)
    shuneng_dict = shuneng_dict[cur_date]
    name_list = shuneng_dict.keys()
    words_list = [set(name) for name in name_list]
    for item in daily_top5:
	name = item['basics'][3].decode('utf-8')
	name_set = set(name)
	len_list = [len(name_set.intersection(w)) for w in words_list]
	pair_list = zip(len_list, range(len(len_list)))
	pair_list.sort(key=lambda x: x[0], reverse=True)
	if pair_list[0][0] > 1:
	    item['shuneng'] = int(shuneng_dict[name_list[pair_list[0][1]]])
    return daily_top5

def daily_battle(daily_top5):
    bd_errs = []
    shuneng_errs = []
    win_list = []
    bd_scores = []
    shuneng_scores = []
    counter = 0
    for item in daily_top5:
	bd_err = '--'
	shuneng_err = '--'
        if 'shuneng' not in item.keys():
            item['shuneng'] = '--'
	try:
	    bd_err = basic_funcs.get_err_by_real(item['basics'][4], item['basics'][5])
	    shuneng_err = basic_funcs.get_err_by_real(item['shuneng'], item['basics'][5])
	except:
	    pass
        bd_errs.append(bd_err)
        shuneng_errs.append(shuneng_err)
        if bd_err == '--' or bd_err > shuneng_err:
	    basic_funcs.update_winner('shuneng', win_list, shuneng_scores, bd_scores, counter)
        elif shuneng_err == '--' or bd_err < shuneng_err:
	    basic_funcs.update_winner('baidu', win_list, bd_scores, shuneng_scores, counter)
        elif bd_err =='--' and shuneng_err == '--' or math.fabs(bd_err - shuneng_err) < 1e-9:
	    basic_funcs.update_winner('none', win_list, bd_scores, shuneng_scores, 5)
        counter += 1
    return bd_errs, shuneng_errs, win_list, bd_scores, shuneng_scores

def get_score(daily_dict, shuneng_dict):
    min_date = max(min(daily_dict.keys()),min(shuneng_dict.keys()))
    max_date = min(max(daily_dict.keys()), max(shuneng_dict.keys()))
    top5_dict = {}
    for d in shuneng_dict.keys():
        if d <= max_date and d >= min_date:
            daily_top5 = single_score(daily_dict, shuneng_dict, d)
            bd_errs, shuneng_errs, win_list, bd_scores, shuneng_scores = daily_battle(daily_top5)
            bd_score = sum(bd_scores)
            shuneng_score = sum(shuneng_scores)
            if bd_score > shuneng_score:
                winner = 'baidu'
            elif bd_score < shuneng_score:
                winner = 'shuneng'
            else:
                winner = 'none'
            top5_dict[d] = {}
            top5_dict[d]['list'] = daily_top5
            top5_dict[d]['bd_errs'] = bd_errs
            top5_dict[d]['shuneng_errs'] = shuneng = shuneng_errs
            top5_dict[d]['win'] = win_list
            top5_dict[d]['bd_scores'] = bd_scores
            top5_dict[d]['shuneng_scores'] = shuneng_scores
            top5_dict[d]['bd_score'] = bd_score
            top5_dict[d]['shuneng_score'] = shuneng_score
            top5_dict[d]['winner'] = winner
    return top5_dict, min_date, max_date

def battle_score(daily_dict):
    shuneng_dict = read_shuneng()
    top5_dict, first_date, last_date = get_score(daily_dict, shuneng_dict)
    return top5_dict, first_date, last_date

#百度数能误差对比
def update_err(name_list, real_list, pre_val, mv_name, err, err_len):
    name_list = [n.decode('utf-8') for n in name_list]
    is_existed, real_val, ccc = basic_funcs.is_name_existed(name_list, real_list, mv_name)
    if is_existed:
	err += basic_funcs.get_err_by_real(pre_val, real_val)
    	err_len += 1
    return err, err_len

def get_dapan_err(summary, shuneng_dict, start_date, end_date):
    dapan_shuneng_err = 0.0
    dapan_baidu_err = 0.0
    dapan_shuneng_size = 0
    dapan_baidu_size = 0
    for d in summary.keys():
	if d >= start_date and d <= end_date:
	    pre = summary[d][1]
	    real = summary[d][2]
	    if pre != '-' and real != '-':
		dapan_baidu_err += basic_funcs.get_err_by_real(pre, real)
		dapan_baidu_size += 1
    for d in shuneng_dict.keys():
	if d >= start_date and d <= end_date and d in summary.keys():
	    pre = shuneng_dict[d]['大盘'.decode('utf-8')]
	    real = summary[d][2]
	    if pre != '——' and real != '-':
		dapan_shuneng_err += basic_funcs.get_err_by_real(pre, real)
		dapan_shuneng_size += 1
    if dapan_baidu_size != 0:
	dapan_baidu_err /= dapan_baidu_size
    else:
	dapan_baidu_err = -1.0
    if dapan_shuneng_size != 0:
	dapan_shuneng_err /= dapan_shuneng_size
    else:
	dapan_shuneng_err = -1.0
    return dapan_baidu_err, dapan_shuneng_err
def get_top5_err_shuneng(daily_dict, first_day_ids, before_day_ids, shuneng_dict, start_date, end_date):
    top5_shuneng_err = 0.0
    first_top5_shuneng_err = 0.0
    next_top5_shuneng_err = 0.0
    top5_shuneng_size = 0
    first_top5_shuneng_size = 0
    next_top5_shuneng_size = 0
    for d in shuneng_dict.keys():
	if d >= start_date and d <= end_date:
	    if d in daily_dict.keys():
    		daily_list = [item for item in daily_pre.get_daily_list(daily_dict, d) if item['basics'][5] != '-']
	    else:
		daily_list = []
    	    top5_list = basic_funcs.get_top5_by_ind(daily_list, 5)
	    if d in before_day_ids.keys():
    	    	top5_list = [item for item in top5_list if item['basics'][1] not in before_day_ids[d]]
	    top5_names = [item['basics'][3].decode('utf-8') for item in top5_list]
	    top5_reals = [item['basics'][5].decode('utf-8') for item in top5_list]
	    if d not in first_day_ids.keys():
		first_top5_list = []
	    	next_top5_list = top5_list
	    else:
	    	first_top5_list = [item for item in top5_list if item['basics'][1] in first_day_ids[d]]
	    	next_top5_list = [item for item in top5_list if item['basics'][1] not in first_day_ids[d]]
	    first_top5_names = [item['basics'][3].decode('utf-8') for item in first_top5_list]
	    first_top5_reals = [item['basics'][5].decode('utf-8') for item in first_top5_list]
	    next_top5_names = [item['basics'][3].decode('utf-8') for item in next_top5_list]
	    next_top5_reals = [item['basics'][5].decode('utf-8') for item in next_top5_list]
	    for mv_name in shuneng_dict[d].keys():
		if mv_name == '大盘':
		    continue
		top5_shuneng_err, top5_shuneng_size = update_err(top5_names, top5_reals, shuneng_dict[d][mv_name], mv_name, top5_shuneng_err, top5_shuneng_size)
		first_top5_shuneng_err, first_top5_shuneng_size = update_err(first_top5_names, first_top5_reals, shuneng_dict[d][mv_name], mv_name, first_top5_shuneng_err, first_top5_shuneng_size)
		next_top5_shuneng_err, next_top5_shuneng_size = update_err(next_top5_names, next_top5_reals, shuneng_dict[d][mv_name], mv_name, next_top5_shuneng_err, next_top5_shuneng_size)
    if top5_shuneng_size != 0:
	top5_shuneng_err /= top5_shuneng_size
    else:
	top5_shuneng_err = -1.0
    if first_top5_shuneng_size != 0:
	first_top5_shuneng_err /= first_top5_shuneng_size
    else:
	first_top5_shuneng_err = -1.0
    if next_top5_shuneng_size != 0:
	next_top5_shuneng_err /= next_top5_shuneng_size
    else:
	next_top5_shuneng_err = -1.0
    return top5_shuneng_err, first_top5_shuneng_err, next_top5_shuneng_err

def get_total_err_shuneng(daily_dict, first_day_ids, before_day_ids, shuneng_dict, start_date, end_date):
    shuneng_err = 0.0
    first_shuneng_err = 0.0
    next_shuneng_err = 0.0
    shuneng_size = 0
    first_shuneng_size = 0
    next_shuneng_size = 0
    for d in shuneng_dict.keys():
	if d > start_date and d < end_date:
	    if d in daily_dict.keys():
    		daily_list = [item for item in daily_pre.get_daily_list(daily_dict, d) if item['basics'][5] != '-']
	    else:
		daily_list = []
	    if d in before_day_ids.keys():
    	    	daily_list = [item for item in daily_list if item['basics'][1] not in before_day_ids[d]]
	    daily_names = [item['basics'][3].decode('utf-8') for item in daily_list]
	    daily_reals = [item['basics'][5].decode('utf-8') for item in daily_list]
	    if d not in first_day_ids.keys():
		first_daily_list = []
	    	next_daily_list = daily_list
	    else:
	    	first_daily_list = [item for item in daily_list if item['basics'][1] in first_day_ids[d]]
	    	next_daily_list = [item for item in daily_list if item['basics'][1] not in first_day_ids[d]]
	    first_daily_names = [item['basics'][3].decode('utf-8') for item in first_daily_list]
	    first_daily_reals = [item['basics'][5].decode('utf-8') for item in first_daily_list]
	    next_daily_names = [item['basics'][3].decode('utf-8') for item in next_daily_list]
	    next_daily_reals = [item['basics'][5].decode('utf-8') for item in next_daily_list]
	    for mv_name in shuneng_dict[d].keys():
		if mv_name == '大盘':
		    continue
		shuneng_err, shuneng_size = update_err(daily_names, daily_reals, shuneng_dict[d][mv_name], mv_name, shuneng_err, shuneng_size)
		first_shuneng_err, first_shuneng_size = update_err(first_daily_names, first_daily_reals, shuneng_dict[d][mv_name], mv_name, first_shuneng_err, first_shuneng_size)
		next_shuneng_err, next_shuneng_size = update_err(next_daily_names, next_daily_reals, shuneng_dict[d][mv_name], mv_name, next_shuneng_err, next_shuneng_size)
#		if len(mv_name) < 5 and len(mv_name) > 3:
#			a,aa, ai = basic_funcs.is_name_existed(daily_names, daily_reals, mv_name)
#			b,bb, bi = basic_funcs.is_name_existed(first_daily_names, first_daily_reals, mv_name)
#			c,cc, ci = basic_funcs.is_name_existed(next_daily_names, next_daily_reals, mv_name)
#			print mv_name, '..'.join(daily_names), a, ai
#			print mv_name, '..'.join(first_daily_names), b, bi
#			print mv_name, '..'.join(next_daily_names), c, ci
#			print '#################'
    if shuneng_size != 0:
	shuneng_err /= shuneng_size
    else:
	shuneng_err = -1.0
    if first_shuneng_size != 0:
	first_shuneng_err /= first_shuneng_size
    else:
	first_shuneng_err = -1.0
    if next_shuneng_size != 0:
	next_shuneng_err /= next_shuneng_size
    else:
	next_shuneng_err = -1.0
    return shuneng_err, first_shuneng_err, next_shuneng_err

def get_top5_err_baidu(daily_dict, first_day_ids, before_day_ids, start_date, end_date):
    top5_baidu_err_A = 0.0
    top5_baidu_err_B = 0.0
    first_top5_baidu_err_A = 0.0
    first_top5_baidu_err_B = 0.0
    next_top5_baidu_err_A = 0.0
    next_top5_baidu_err_B = 0.0
    top5_baidu_size_A = 0
    top5_baidu_size_B = 0
    first_top5_baidu_size_A = 0
    first_top5_baidu_size_B = 0
    next_top5_baidu_size_A = 0
    next_top5_baidu_size_B = 0
    for d in daily_dict.keys():
	if d > start_date and d < end_date:
    	    daily_list = [item for item in daily_pre.get_daily_list(daily_dict, d) if item['basics'][5] != '-']
    	    top5_list = basic_funcs.get_top5_by_ind(daily_list, 5)
	    if d in before_day_ids.keys():
    	    	top5_list = [item for item in top5_list if item['basics'][1] not in before_day_ids[d]]
	    if d not in first_day_ids.keys():
		first_top5_list = []
	    	next_top5_list = top5_list
	    else:
	    	first_top5_list = [item for item in top5_list if item['basics'][1] in first_day_ids[d]]
	    	next_top5_list = [item for item in top5_list if item['basics'][1] not in first_day_ids[d]]
	    err_A, size_A, err_B, size_B = basic_funcs.get_err_by_list(top5_list)
	    top5_baidu_err_A += err_A
	    top5_baidu_size_A += size_A
	    top5_baidu_err_B += err_B
	    top5_baidu_size_B += size_B
	    err_A, size_A, err_B, size_B = basic_funcs.get_err_by_list(first_top5_list)
	    first_top5_baidu_err_A += err_A
	    first_top5_baidu_size_A += size_A
	    first_top5_baidu_err_B += err_B
	    first_top5_baidu_size_B += size_B
	    err_A, size_A, err_B, size_B = basic_funcs.get_err_by_list(next_top5_list)
	    next_top5_baidu_err_A += err_A
	    next_top5_baidu_size_A += size_A
	    next_top5_baidu_err_B += err_B
	    next_top5_baidu_size_B += size_B
    if top5_baidu_size_A != 0:
	top5_baidu_err_A /= top5_baidu_size_A
    else:
	top5_baidu_err_A = -1.0
    if top5_baidu_size_B != 0:
	top5_baidu_err_B /= top5_baidu_size_B
    else:
	top5_baidu_err_B = -1.0
    if first_top5_baidu_size_A != 0:
	first_top5_baidu_err_A /= first_top5_baidu_size_A
    else:
	first_top5_baidu_err_A = -1.0
    if first_top5_baidu_size_B != 0:
	first_top5_baidu_err_B /= first_top5_baidu_size_B
    else:
	first_top5_baidu_err_B = -1.0
    if next_top5_baidu_size_A != 0:
	next_top5_baidu_err_A /= next_top5_baidu_size_A
    else:
	next_top5_baidu_err_A = -1.0
    if next_top5_baidu_size_B != 0:
	next_top5_baidu_err_B /= next_top5_baidu_size_B
    else:
	next_top5_baidu_err_B = -1.0
    return top5_baidu_err_A, top5_baidu_err_B, first_top5_baidu_err_A, first_top5_baidu_err_B, next_top5_baidu_err_A, next_top5_baidu_err_B

def get_total_err_baidu(daily_dict, first_day_ids, before_day_ids, start_date, end_date):
    baidu_err_A = 0.0
    baidu_err_B = 0.0
    first_baidu_err_A = 0.0
    first_baidu_err_B = 0.0
    next_baidu_err_A = 0.0
    next_baidu_err_B = 0.0
    baidu_size_A = 0
    baidu_size_B = 0
    first_baidu_size_A = 0
    first_baidu_size_B = 0
    next_baidu_size_A = 0
    next_baidu_size_B = 0
    for d in daily_dict.keys():
	if d > start_date and d < end_date:
    	    daily_list = [item for item in daily_pre.get_daily_list(daily_dict, d) if item['basics'][5] != '-']
	    if d in before_day_ids.keys():
    	    	daily_list = [item for item in daily_list if item['basics'][1] not in before_day_ids[d]]
	    if d not in first_day_ids.keys():
		first_daily_list = []
	    	next_daily_list = daily_list
	    else:
	    	first_daily_list = [item for item in daily_list if item['basics'][1] in first_day_ids[d]]
	    	next_daily_list = [item for item in daily_list if item['basics'][1] not in first_day_ids[d]]
	    err_A, size_A, err_B, size_B = basic_funcs.get_err_by_list(daily_list)
	    baidu_err_A += err_A
	    baidu_size_A += size_A
	    baidu_err_B += err_B
	    baidu_size_B += size_B
	    err_A, size_A, err_B, size_B = basic_funcs.get_err_by_list(first_daily_list)
	    first_baidu_err_A += err_A
	    first_baidu_size_A += size_A
	    first_baidu_err_B += err_B
	    first_baidu_size_B += size_B
	    err_A, size_A, err_B, size_B = basic_funcs.get_err_by_list(next_daily_list)
	    next_baidu_err_A += err_A
	    next_baidu_size_A += size_A
	    next_baidu_err_B += err_B
	    next_baidu_size_B += size_B
    if baidu_size_A != 0:
	baidu_err_A /= baidu_size_A
    else:
	baidu_err_A = -1.0
    if baidu_size_B != 0:
	baidu_err_B /= baidu_size_B
    else:
	baidu_err_B = -1.0
    if first_baidu_size_A != 0:
	first_baidu_err_A /= first_baidu_size_A
    else:
	first_baidu_err_A = -1.0
    if first_baidu_size_B != 0:
	first_baidu_err_B /= first_baidu_size_B
    else:
	first_baidu_err_B = -1.0
    if next_baidu_size_A != 0:
	next_baidu_err_A /= next_baidu_size_A
    else:
	next_baidu_err_A = -1.0
    if next_baidu_size_B != 0:
	next_baidu_err_B /= next_baidu_size_B
    else:
	next_baidu_err_B = -1.0
    return baidu_err_A, baidu_err_B, first_baidu_err_A, first_baidu_err_B, next_baidu_err_A, next_baidu_err_B

def battle_errs(summary, daily_dict, first_day_ids, before_day_ids, start_date, end_date):
    shuneng_dict = read_shuneng()
    dapan_baidu_err, dapan_shuneng_err = get_dapan_err(summary, shuneng_dict, start_date, end_date)
    top5_shuneng_err, first_top5_shuneng_err, next_top5_shuneng_err = get_top5_err_shuneng(daily_dict, first_day_ids, before_day_ids, shuneng_dict, start_date, end_date)
    shuneng_err, first_shuneng_err, next_shuneng_err = get_total_err_shuneng(daily_dict, first_day_ids, before_day_ids, shuneng_dict, start_date, end_date)
    top5_baidu_err_A, top5_baidu_err_B, first_top5_baidu_err_A, first_top5_baidu_err_B, next_top5_baidu_err_A, next_top5_baidu_err_B = get_top5_err_baidu(daily_dict, first_day_ids, before_day_ids, start_date, end_date)
    baidu_err_A, baidu_err_B, first_baidu_err_A, first_baidu_err_B, next_baidu_err_A, next_baidu_err_B = get_total_err_baidu(daily_dict, first_day_ids, before_day_ids, start_date, end_date)
    return [dapan_shuneng_err, top5_shuneng_err, first_top5_shuneng_err, next_top5_shuneng_err, shuneng_err, first_shuneng_err, next_shuneng_err,\
	dapan_baidu_err, top5_baidu_err_A, first_top5_baidu_err_A, next_top5_baidu_err_A, baidu_err_A, first_baidu_err_A, next_baidu_err_A,\
	-1.0, top5_baidu_err_B, first_top5_baidu_err_B, next_top5_baidu_err_B, baidu_err_B, first_baidu_err_B, next_baidu_err_B]

def movingAve(top5_dict):
    date_list = [per_date for per_date in top5_dict.keys()]
    date_list.sort()
    winner_list = [top5_dict[item]['winner'] for item in date_list]
    ave_list = []
    temp_ave = 0.0
    for i in xrange(len(date_list)):
        if winner_list[i] == 'baidu':
            temp_ave += 0.2
        if i >= 5 and winner_list[i - 5] == 'baidu':
            temp_ave -= 0.2
        ave_list.append(round(temp_ave,2))
    return date_list, ave_list

if __name__ == '__main__':
    battle_score()
