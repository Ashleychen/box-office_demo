#coding=utf-8
import json
import sys
import reading
import basic_funcs

reload(sys)
sys.setdefaultencoding('utf-8')

def get_shuneng_week():
    with open('/home/work/chenyaxue/movie/data/shuneng_week') as f:
        line = f.readline()
        line_json = json.loads(line)
    return line_json

def get_boxoffice_summary_week():
    week_dict = {}
    with open('/home/work/chenyaxue/movie/data/boxoffice_summary_week.txt') as f:
	for line in f:
	    fields = line.strip().split('\x01')
	    start_date = fields[0]
	    end_date = fields[1]
	    pre_date = fields[2]
	    en_id = fields[3]
	    bd_id = fields[4]
	    name = fields[5]
	    on_date = fields[6]
	    on_days = fields[7]
	    pre = fields[8]
	    real = fields[9]
	    if pre_date not in week_dict.keys():
		week_dict[pre_date] = {}
	    if start_date + '~' + end_date not in week_dict[pre_date].keys():
		week_dict[pre_date][start_date + '~' + end_date] = []
	    week_dict[pre_date][start_date + '~' + end_date].append([on_date, on_days, name, pre, real])
    for d in week_dict.keys():
    	for r in week_dict[d].keys():
	    mv_list = week_dict[d][r]
	    real_sum = sum([float(item[4]) for item in mv_list])
	    if abs(real_sum - 0) < 1e-9:
	    	mv_list.sort(key=lambda x:float(x[3]), reverse=True)
	    else:
	    	mv_list.sort(key=lambda x:float(x[4]), reverse=True)
    return week_dict

def week_is_existed(name_list, pre_list, name):
    name_list = [n.decode('utf-8') for n in name_list]
    words_list = [set(n) for n in name_list]
    name_set = set(name.decode('utf-8'))
    len_list = [len(name_set.intersection(w)) for w in words_list]
    pair_list = zip(len_list, range(len(len_list)))
    pair_list.sort(key=lambda x: x[0], reverse=True)
    if len(pair_list) > 0 and ((pair_list[0][0] >= len(name_set) * 0.6 and pair_list[0][0] >= len(words_list[pair_list[0][1]]) * 0.6) or pair_list[0][0] >= 4):
        return True, pre_list[pair_list[0][1]], pair_list[0][1]
    else:
        return False, '--', -1

def append_shuneng_pre():
    shuneng_dict = get_shuneng_week()
    boxoffice_summary_week_dict = get_boxoffice_summary_week()
    for pre_date in boxoffice_summary_week_dict.keys():
    	for date_range in boxoffice_summary_week_dict[pre_date].keys():
	    for item_list in boxoffice_summary_week_dict[pre_date][date_range]:
	    	if date_range in shuneng_dict.keys():
		    name_list = shuneng_dict[date_range].keys()
		    pre_list = [shuneng_dict[date_range][name][2] for name in name_list]
		    flag, pre, ind = week_is_existed(name_list, pre_list, item_list[2])
		    item_list.append(pre)
	    	else:
		    item_list.append('--')
    return boxoffice_summary_week_dict

def get_err_by_weekday(weekly_list_with_real, weekly_err_dict, weekly_size_dict, weekday):
    for item_ind in xrange(len(weekly_list_with_real)):
	baidu_pre = weekly_list_with_real[item_ind][3]
	shuneng_pre = weekly_list_with_real[item_ind][5]
	real = weekly_list_with_real[item_ind][4]
	if baidu_pre != '-' and shuneng_pre != '--':
	    if basic_funcs.is_float_zero(baidu_pre, 0) and basic_funcs.is_float_zero(real, 0) and basic_funcs.is_float_zero(shuneng_pre, 0):
		weekly_size_dict[weekday][0] += 1
		continue
	    baidu_err = basic_funcs.get_err_by_real(baidu_pre, real)
	    shuneng_err = basic_funcs.get_err_by_real(shuneng_pre, real)
	    weekly_err_dict[weekday][0] += baidu_err
	    weekly_err_dict[weekday][1] += shuneng_err
	    weekly_size_dict[weekday][0] += 1
	    if item_ind < 5:
	    	weekly_err_dict[weekday][2] += baidu_err
	    	weekly_err_dict[weekday][3] += shuneng_err
	    	weekly_size_dict[weekday][1] += 1
	    if item_ind < 10:
	    	weekly_err_dict[weekday][4] += baidu_err
	    	weekly_err_dict[weekday][5] += shuneng_err
	    	weekly_size_dict[weekday][2] += 1
    return weekly_err_dict, weekly_size_dict

def getWeekLlyErrList(boxoffice_summary_week_dict):
    weekly_err_dict = {}
    weekly_size_dict = {}
    for ind in xrange(7):
	weekly_err_dict[ind] = [0.0] * 6
    	weekly_size_dict[ind] = [0] * 6
    pre_date_list = boxoffice_summary_week_dict.keys()
    pre_date_list.sort()
    max_pre_date = pre_date_list[-1]
    for pre_date in boxoffice_summary_week_dict.keys():
	week_end_date = boxoffice_summary_week_dict[pre_date].keys()[0].split('~')[1]
	if basic_funcs.get_days_delta(week_end_date, max_pre_date) <= 2:
	    continue
	pre_weekday = basic_funcs.get_weekday(pre_date)
	if pre_weekday not in weekly_err_dict.keys():
	    weekly_err_dict[pre_weekday] = []
    	for dr in boxoffice_summary_week_dict[pre_date].keys():
	    weekly_list = boxoffice_summary_week_dict[pre_date][dr]
	    weekly_list_with_real = [item for item in weekly_list if item[4] != '-']
	    weekly_list_with_real.sort(key=lambda x: float(x[4]), reverse = True)
	    weekly_err_dict, weekly_size_dict = get_err_by_weekday(weekly_list_with_real, weekly_err_dict, weekly_size_dict, pre_weekday)
    for weekday in xrange(7):
	for ind in xrange(3):
	    if weekly_size_dict[weekday][ind] != 0:
		weekly_err_dict[weekday][ind * 2] /= weekly_size_dict[weekday][ind]
		weekly_err_dict[weekday][ind * 2 + 1] /= weekly_size_dict[weekday][ind]
	    else:
		weekly_err_dict[weekday][ind * 2] = '--'
		weekly_err_dict[weekday][ind * 2 + 1] = '--'
    weekly_err_list = []
    for weekday in weekly_err_dict.keys():
	weekly_err_list += weekly_err_dict[weekday]
    return weekly_err_list

def get_boxoffice_week():
    weekly_dict = {}
    with open('/home/work/chenyaxue/movie/data/boxoffice_week.txt') as f:
	for line in f:
	    fields = line.strip().split('\x01')
	    week_start_date = fields[0]
	    week_end_date = fields[1]
	    pre_date = fields[2]
	    date = fields[3]
	    en_id = fields[4]
	    bd_id = fields[5]
	    name = fields[6]
	    pre = fields[7]
	    rate = fields[8]
	    if pre_date not in weekly_dict.keys():
		weekly_dict[pre_date] = {}
	    if name not in weekly_dict[pre_date].keys():
		weekly_dict[pre_date][name] = []
	    weekly_dict[pre_date][name].append([date, pre, rate])
    for pre_date in weekly_dict.keys():
	for name in weekly_dict[pre_date].keys():
	    weekly_dict[pre_date][name].sort(key=lambda x:x[0])
    return weekly_dict

def get_max_date_range(boxoffice_summary_week_dict):
    range_list = boxoffice_summary_week_dict.keys()
    range_list.sort(reverse=True)
    return range_list[0], range_list[-1] 

if __name__ == '__main__':
    #get_shuneng_week()
    boxoffice_summary_week_dict = append_shuneng_pre()
    max_date = get_max_date_range(boxoffice_summary_week_dict)
    print max_date
