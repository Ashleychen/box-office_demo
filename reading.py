#coding=utf-8

def read_with_features(f_name):
    f_dict = {}
    with open(f_name) as f:
	while True:
	    line = f.readline()
	    if not line:
		break
	    fields = line.strip('\n').split('\x01')
	    #mv_date = fields[0], en_id = fields[1], bd_id = fields[2], mv_name = fields[3]
	    #pre_b = fields[4], real_b = fields[5], scr_rate = fields[6]
	    mv_date = fields[0]
	    if mv_date not in f_dict.keys():
		f_dict[mv_date] = {}
	    en_id = fields[1]
	    if en_id not in f_dict[mv_date].keys():
		f_dict[mv_date][en_id] = {}
	    f_dict[mv_date][en_id]['basics'] = fields
	    count_line = f.readline()
	    count = int(count_line.strip('\n'))
	    fea_list = []
	    for i in xrange(count):
		feature_line = f.readline()
		fields = feature_line.strip('\n').split('\x01')
		fea_name = fields[0]
		fea_val = fields[1]
		fea_weight = fields[2]
		fea_list.append((fea_name, fea_val, fea_weight))
	    fea_list.sort(key=lambda x: x[0])
	    f_dict[mv_date][en_id]['feas'] = fea_list
    return f_dict

def read_without_features(f_name):
    f_dict = {}
    with open(f_name) as f:
	for line in f:
	    fields = line.strip('\n').split('\x01')
	    mv_date = fields[0]
	    f_dict[mv_date] = fields
    return f_dict

def read_screening(f_name):
    f_dict = {}
    with open(f_name) as f:
	for line in f:
	    fields = line.strip('\n').split('\x01')
	    mv_date = fields[0]
	    if mv_date not in f_dict.keys():
		f_dict[mv_date] = {}
	    en_id = fields[1]
	    if en_id not in f_dict[mv_date].keys():
		f_dict[mv_date][en_id] = {}
	    f_dict[mv_date][en_id] = fields
    return f_dict

def read_files():
    first_day_a = read_with_features('/home/work/chenyaxue/movie/data/boxoffice_first_day1.txt')
    first_day_b = read_with_features('/home/work/chenyaxue/movie/data/boxoffice_first_day2.txt')
    next_day_a = read_with_features('/home/work/chenyaxue/movie/data/boxoffice_next_day1.txt')
    next_day_b = read_with_features('/home/work/chenyaxue/movie/data/boxoffice_next_day2.txt')
    before_day_dict = read_with_features('/home/work/chenyaxue/movie/data/boxoffice_before_first_day.txt')
    summary = read_without_features('/home/work/chenyaxue/movie/data/boxoffice_summary_day.txt')
    total_basic = read_with_features('/home/work/chenyaxue/movie/data/total_boxoffice_basic_info.txt')
    total_first_dict = read_with_features('/home/work/chenyaxue/movie/data/total_boxoffice_playdate.txt')
    min_date = max(min(next_day_a.keys()), min(next_day_b.keys()))
    max_date = min(max(next_day_a.keys()), max(next_day_b.keys()))
    first_day_keys = set(first_day_a.keys() + first_day_b.keys())
    next_day_keys = set(next_day_a.keys() + next_day_b.keys())
    first_ids_keys = {}
    next_ids_keys = {}
    for d in first_day_keys:
	first_ids = []
	if d in first_day_a.keys():
	    first_ids.extend(first_day_a[d].keys())
	if d in first_day_b.keys():
	    first_ids.extend(first_day_b[d].keys())
	first_ids_keys[d] = list(set(first_ids))
    for d in next_day_keys:
	next_ids = []
	if d in next_day_a.keys():
	    next_ids.extend(next_day_a[d].keys())
	if d in next_day_b.keys():
	    next_ids.extend(next_day_b[d].keys())
	next_ids_keys[d] = set(next_ids)
    before_day_ids = {}
    for d in before_day_dict.keys():
	before_day_ids[d] = before_day_dict[d].keys()
    for d in first_day_keys:
	for id in first_ids_keys[d]:
	    if d in first_day_a.keys() and id in first_day_a[d].keys():
		if d in first_day_b.keys() and id in first_day_b[d].keys():
	            first_day_a[d][id]['basics'].append(first_day_b[d][id]['basics'][4])
		else:
                    first_day_a[d][id]['basics'].append('--')
	    else:
		if d not in first_day_a.keys():
		    first_day_a[d] = {}
		first_day_a[d][id] = first_day_b[d][id]
		pre_B = first_day_b[d][id]['basics'][4]
		first_day_a[d][id]['basics'][4] = '--'
		first_day_a[d][id]['basics'].append(pre_B)
    for d in next_day_keys:
	for id in next_ids_keys[d]:
	    if d in next_day_a.keys() and id in next_day_a[d].keys():
		if d in next_day_b.keys() and id in next_day_b[d].keys():
		    next_day_a[d][id]['basics'].append(next_day_b[d][id]['basics'][4])
		else:
		    next_day_a[d][id]['basics'].append('--')
	    else:
		if d not in next_day_a.keys():
		    next_day_a[d] = {}
		next_day_a[d][id] = next_day_b[d][id]
		pre_B = next_day_b[d][id]['basics'][4]
		next_day_a[d][id]['basics'][4] = '--'
		next_day_a[d][id]['basics'].append(pre_B)
    for d in before_day_dict.keys():
	for id in before_day_dict[d].keys():
	    before_day_dict[d][id]['basics'].append(before_day_dict[d][id]['basics'][4])
    daily_dict = {}
    for d in next_day_keys:
	#temp_dict = {'大盘': summary[d]}
	temp_dict = {}
	if d in first_day_a.keys():
	    temp_dict = dict(temp_dict.items() + first_day_a[d].items())
	if d in next_day_a.keys():
	    temp_dict = dict(temp_dict.items() + next_day_a[d].items())
	if d in before_day_dict.keys():
	    temp_dict = dict(temp_dict.items() + before_day_dict[d].items())
	daily_dict[d] = temp_dict
    return daily_dict, first_day_a, next_day_a, summary, total_basic, total_first_dict, min_date, max_date, first_ids_keys, before_day_ids

if __name__ == '__main__':
    read_files()
