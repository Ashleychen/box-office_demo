#coding=utf-8
import json
import basic_funcs
import reading

def get_on_days_errs_dict(total_dict, shuneng_dict):
    totol_err_by_on_days_dict = {}
    for d in total_dict.keys():
	for id in total_dict[d].keys():
	    l = total_dict[d][id]['basics']
	    on_days = l[5] 
	    if on_days not in totol_err_by_on_days_dict.keys():
		totol_err_by_on_days_dict[on_days] = []
	    if l[7] != '-' and basic_funcs.get_days_delta_from_today(l[4]) > 14:
	    	name = l[3].decode('utf-8')
	    	if l[4] in shuneng_dict.keys():
	    	    if name in shuneng_dict[l[4]].keys():
			totol_err_by_on_days_dict[on_days].append([l[8], shuneng_dict[l[4]][name], l[7]])
		    else:
		    	name_list = shuneng_dict[l[4]].keys()
		    	shuneng_pre_list = [shuneng_dict[l[4]][n] for n in name_list]
		    	flag, data, ind = basic_funcs.cmp_name_with_shuneng_list(name_list, shuneng_pre_list, name)
		    	if flag:
			    totol_err_by_on_days_dict[on_days].append([l[8], data, l[7]])
		    	else:
			    totol_err_by_on_days_dict[on_days].append([l[8], '--', l[7]])
	    	else:
		    totol_err_by_on_days_dict[on_days].append([l[8], '--', l[7]])
    return totol_err_by_on_days_dict

def get_on_days_errs_by_range(totol_err_by_on_days_dict, range_type):
    err_dict_by_range = {}
    for d in totol_err_by_on_days_dict.keys():
	if d not in err_dict_by_range.keys():
	    err_dict_by_range[d] = [0.0, 0.0, 0]
	for ind in xrange(len(totol_err_by_on_days_dict[d])):
	    baidu_pre = totol_err_by_on_days_dict[d][ind][0]
	    shuneng_pre = totol_err_by_on_days_dict[d][ind][1]
	    real = totol_err_by_on_days_dict[d][ind][2]
	    if baidu_pre != '-' and baidu_pre != '--' and shuneng_pre != '--' and (range_type == 'all' or (range_type == 'million' and float(real) < 10000 and float(real) >= 1000 or (range_type == 'billion' and float(real) >= 10000))):
		baidu_err = basic_funcs.get_err_by_real(baidu_pre, real)
		shuneng_err = basic_funcs.get_err_by_real(shuneng_pre, real)
	    	err_dict_by_range[d][0] += baidu_err
	    	err_dict_by_range[d][1] += shuneng_err
	    	err_dict_by_range[d][2] += 1
    return err_dict_by_range

def get_on_days_errs(total_dict, shuneng_dict):
    err_dict = {}
    totol_err_by_on_days_dict = get_on_days_errs_dict(total_dict, shuneng_dict)
    err_dict_total = get_on_days_errs_by_range(totol_err_by_on_days_dict, 'all')
    err_dict_by_million = get_on_days_errs_by_range(totol_err_by_on_days_dict, 'million')
    err_dict_by_billion = get_on_days_errs_by_range(totol_err_by_on_days_dict, 'billion')
    for d in totol_err_by_on_days_dict.keys():
	if err_dict_total[d][2] == 0:
	    baidu_err_total = '--'
	    shuneng_err_total = '--'
	else:
	    baidu_err_total = basic_funcs.get_ave_err(err_dict_total[d][0], err_dict_total[d][2])
	    shuneng_err_total = basic_funcs.get_ave_err(err_dict_total[d][1], err_dict_total[d][2])
	if err_dict_by_million[d][2] == 0:
	    baidu_err_million = '--'
	    shuneng_err_million = '--'
	else:
	    baidu_err_million = basic_funcs.get_ave_err(err_dict_by_million[d][0], err_dict_by_million[d][2])
	    shuneng_err_million = basic_funcs.get_ave_err(err_dict_by_million[d][1], err_dict_by_million[d][2])
	if err_dict_by_billion[d][2] == 0:
	    baidu_err_billion = '--'
	    shuneng_err_billion = '--'
	else:
	    baidu_err_billion = basic_funcs.get_ave_err(err_dict_by_billion[d][0], err_dict_by_billion[d][2])
	    shuneng_err_billion = basic_funcs.get_ave_err(err_dict_by_billion[d][1], err_dict_by_billion[d][2])
	err_dict[d] = [baidu_err_total, shuneng_err_total, baidu_err_million, shuneng_err_million, baidu_err_billion, shuneng_err_billion]
    return err_dict

def get_total_boxoffice_dict(playdate_dict):
    smooth_dict = reading.read_with_features('/home/work/chenyaxue/movie/data/total_boxoffice_playdate_smooth.txt')
    for pre_date in playdate_dict.keys():
	for en_id in playdate_dict[pre_date].keys():
	    if pre_date in smooth_dict.keys() and en_id in smooth_dict[pre_date].keys():
		playdate_dict[pre_date][en_id]['basics'].append(smooth_dict[pre_date][en_id]['basics'][6])
	    else:
		playdate_dict[pre_date][en_id]['basics'].append('--')
    for pre_date in smooth_dict.keys():
	for en_id in smooth_dict[pre_date].keys():
	    if pre_date not in playdate_dict.keys() or en_id not in playdate_dict[pre_date].keys():
		if pre_date not in playdate_dict.keys():
		     playdate_dict[pre_date] = {}
		if en_id not in playdate_dict[pre_date].keys():
		     playdate_dict[pre_date][en_id] = {}
		pre_smooth = smooth_dict[pre_date][en_id]['basics'][6]
		playdate_dict[pre_date][en_id]['basics'] = smooth_dict[pre_date][en_id]['basics']
		playdate_dict[pre_date][en_id]['basics'][6] = '--'
		playdate_dict[pre_date][en_id]['basics'].append(pre_smooth)
		playdate_dict[pre_date][en_id]['feas'] = []
		for feas in playdate_dict[pre_date][en_id]['feas']:
		    playdate_dict[pre_date][en_id]['feas'].append(feas)
    return playdate_dict
    
def get_first_list(total_dict, shuneng_dict, pre_date):
    total_list = []
    if pre_date in total_dict.keys():
	for id in total_dict[pre_date]:
	    l = total_dict[pre_date][id]['basics']
	    name = l[3].decode('utf-8')
	    if l[4] in shuneng_dict.keys():
	    	if name in shuneng_dict[l[4]].keys():
	    	    total_list.append([l[4], l[3], l[6], l[8], shuneng_dict[l[4]][name], l[7]])
		else:
		    name_list = shuneng_dict[l[4]].keys()
		    shuneng_pre_list = [shuneng_dict[l[4]][n] for n in name_list]
		    flag, data, ind = basic_funcs.cmp_name_with_shuneng_list(name_list, shuneng_pre_list, name)
		    if flag:
	    	    	total_list.append([l[4], l[3], l[6], l[8], data, l[7]])
		    else:
	    		total_list.append([l[4], l[3], l[6], l[8], '--', l[7]])
	    else:
	    	total_list.append([l[4], l[3], l[6], l[8], '--', l[7]])
    return total_list

def get_whole_err(total_first_dict, shuneng_dict):
    total_first_list_dict = {}
    for d in total_first_dict.keys():
        daily_first_list = get_first_list(total_first_dict, shuneng_dict, d)
        total_first_list_dict[d] = daily_first_list
    err_dict = {}

def get_movie_multi_pre_dict(total_first_dict, shuneng_dict):
    total_first_list_dict = {}
    for d in total_first_dict.keys():
	daily_first_list = get_first_list(total_first_dict, shuneng_dict, d)
	total_first_list_dict[d] = daily_first_list
    temp_first_movie_dict = {}
    first_movie_dict = {}
    for d in total_first_list_dict.keys():
	for l in total_first_list_dict[d]:
	    name = l[1]
	    if name not in temp_first_movie_dict.keys():
		first_movie_dict[name] = {'dateList': [], 'preList': [], 'smoothList': [], 'shunengList': [], 'realList': []}
	    if name not in temp_first_movie_dict.keys():
		temp_first_movie_dict[name] = []
	    temp_first_movie_dict[name].append({'dateList': d, 'preList': l[2], 'smoothList': l[3], 'shunengList': l[4], 'realList': l[5]})
    for name in temp_first_movie_dict:
	temp_first_movie_dict[name].sort(key=lambda x: x['dateList'])
    for name in temp_first_movie_dict.keys():
	for item in temp_first_movie_dict[name]:
	    first_movie_dict[name]['dateList'].append(item['dateList'])
	    first_movie_dict[name]['preList'].append(item['preList'])
	    first_movie_dict[name]['smoothList'].append(item['smoothList'])
	    first_movie_dict[name]['shunengList'].append(item['shunengList'])
	    first_movie_dict[name]['realList'].append(item['realList'])
    return first_movie_dict

def get_basic_list(total_basic_dict, basic_start_date, basic_end_date):
    total_basic_list = []
    for d in total_basic_dict.keys():
	if d < basic_start_date or d > basic_end_date:
	    continue
	for id in total_basic_dict[d]:
	    l = total_basic_dict[d][id]['basics']
	    name_link = "<a style='color:#2fa4e7' href='javascript:void(0);' onclick='analLaunch(this, event)'>" + l[3] + "</a>"
	    total_basic_list.append([l[0], name_link, l[5], l[4], l[6]])
    return total_basic_list

def get_feas(total_dict):
    feas_dict = {}
    for d in total_dict.keys():
	if d not in feas_dict.keys():
	    feas_dict[d] = {}
	for en_id in total_dict[d]:
	    name = total_dict[d][en_id]['basics'][3]
	    fea_list = total_dict[d][en_id]['feas']
	    if name not in feas_dict[d].keys():
		feas_dict[d][name] = fea_list
    return feas_dict

#制式、发行公司、制作公司、类型、国家、ip信息、导演、演员
def get_analysis(total_basic_dict):
    anal_dict = {}
    for d in total_basic_dict.keys():
	if d not in anal_dict.keys():
	    anal_dict[d] = {}
	for en_id in total_basic_dict[d].keys():
	    name = total_basic_dict[d][en_id]['basics'][3]
	    if name not in anal_dict[d].keys():
		anal_dict[d][name] = {'制式':{}, '发行公司': {}, '制作公司': {}, '类型': {}, '国家': {}, 'ip信息': {}, '导演': {}, '编剧': {}, '演员': {}, '国家和类型组合': {}, 'score': total_basic_dict[d][en_id]['basics'][5]}
		for fea_type in anal_dict[d][name].keys():
		    if fea_type == 'score':
			continue
		    anal_dict[d][name][fea_type]['list'] = []
		    anal_dict[d][name][fea_type]['average'] = 0.0
		    anal_dict[d][name][fea_type]['weights'] = 0.0
		    anal_dict[d][name][fea_type]['score'] = 0.0
		    anal_dict[d][name][fea_type]['names'] = []
	    fea_list = total_basic_dict[d][en_id]['feas']
	    for feas in fea_list:
		fea_name = feas[0]
		if 'player_type' in fea_name or 'IMAX' in fea_name:
		    anal_dict[d][name]['制式']['list'].append(feas)
		if 'company_PUBLISHER' in fea_name:
		    anal_dict[d][name]['发行公司']['list'].append(feas)
		if 'company_PRODUCTCOM' in fea_name:
		    anal_dict[d][name]['制作公司']['list'].append(feas)
		if 'movie_detail_type' in fea_name or ('movie_type' in fea_name and 'movie_nation' not in fea_name):
		    anal_dict[d][name]['类型']['list'].append(feas)
		if 'movie_nation' in fea_name and 'movie_type' not in fea_name:
		    anal_dict[d][name]['国家']['list'].append(feas)
		if 'movie_ip' in fea_name:
		    anal_dict[d][name]['ip信息']['list'].append(feas)
		if 'person_导演' in fea_name:
		    anal_dict[d][name]['导演']['list'].append(feas)
		if 'person_编剧' in fea_name:
		    anal_dict[d][name]['编剧']['list'].append(feas)
		if 'person_演员' in fea_name:
		    anal_dict[d][name]['演员']['list'].append(feas)
		if 'movie_nation_movie_type' in fea_name:
		    anal_dict[d][name]['国家和类型组合']['list'].append(feas)
    total_anal_dict = {'制式':{}, '发行公司': {}, '制作公司': {}, '类型': {}, '国家': {}, 'ip信息': {}, '导演': {}, '编剧': {}, '演员': {}, '国家和类型组合': {}}
    for fea_type in total_anal_dict.keys():
	total_anal_dict[fea_type]['min'] = +999
	total_anal_dict[fea_type]['max'] = -999
	total_anal_dict[fea_type]['average'] = 0.0
	total_anal_dict[fea_type]['weights'] = 0.0
	total_anal_dict[fea_type]['size'] = 0.0
    actor_max = -999
    actor_min = 999
    for d in anal_dict.keys():
	for name in anal_dict[d].keys():
	    for fea_type in anal_dict[d][name].keys():
		if fea_type == 'score':
		    continue
		fea_list = anal_dict[d][name][fea_type]['list']
		invalid_fea_list = [item for item in fea_list if item[1] == '-' or item[2] == '-']
		valid_fea_list = [item for item in fea_list if item[1] != '-' and item[2] != '-']
		valid_fea_list.sort(key=lambda x: float(x[1]) * float(x[2]), reverse=True)
		fea_list = valid_fea_list + invalid_fea_list
		for feas in fea_list:
		    if 'IMAX' in feas[0] and float(feas[1]) * float(feas[2]) > 0:
			anal_dict[d][name]['制式']['names'].append(feas[0])
		    elif 'player_type' in feas[0]:
			anal_dict[d][name]['制式']['names'].append(feas[0].split('_')[2])
		    elif 'movie_detail_type' in feas[0]:
			anal_dict[d][name]['类型']['names'].append(feas[0].split('_')[3])
		    elif 'movie_type' in feas[0] and 'movie_nation' not in feas[0]:
			anal_dict[d][name]['类型']['names'].append(feas[0].split('_')[2])
		    elif 'company_PRODUCTCOM' in feas[0]:
			anal_dict[d][name]['制作公司']['names'].append(feas[0].split('_')[2])
		    elif 'company_PUBLISHER' in feas[0]:
			anal_dict[d][name]['发行公司']['names'].append(feas[0].split('_')[2])
		    elif 'movie_nation' in feas[0] and 'movie_type' not in feas[0]: 
			anal_dict[d][name]['国家']['names'].append(feas[0].split('_')[2])
		    elif 'movie_nation_movie_type' in feas[0]:
			anal_dict[d][name]['国家和类型组合']['names'].append(feas[0].split('movie_nation_movie_type_')[1])
		    elif 'movie_ip' in feas[0]:
			anal_dict[d][name]['ip信息']['names'].append(feas[0].split('_')[2])
		    elif 'person_导演' in feas[0]:
			anal_dict[d][name]['导演']['names'].append(feas[0].split('_')[2])
		    elif 'person_编剧' in feas[0]:
			anal_dict[d][name]['编剧']['names'].append(feas[0].split('_')[2])
		    elif 'person_演员' in feas[0]:
			if feas in valid_fea_list:
			    fea_val = float(feas[1]) * float(feas[2])
			    anal_dict[d][name]['演员']['names'].append({'person': feas[0].split('_')[2], 'val': fea_val, 'score': 5})
			    if fea_val < actor_min:
				actor_min = fea_val
			    elif fea_val > actor_max:
				actor_max = fea_val
			else:
			    anal_dict[d][name]['演员']['names'].append({'person': feas[0].split('_')[2], 'val': '-', 'score': 5})
		    if feas in valid_fea_list:
		    	fea_val = float(feas[1]) * float(feas[2])
		    	anal_dict[d][name][fea_type]['average'] += fea_val
		    	anal_dict[d][name][fea_type]['weights'] += float(feas[1])
		    	total_anal_dict[fea_type]['average'] += fea_val
		    	total_anal_dict[fea_type]['weights'] += float(feas[1])
		    	total_anal_dict[fea_type]['size'] += 1
		if len(valid_fea_list) > 0:
		    if basic_funcs.is_float_zero(anal_dict[d][name][fea_type]['weights'], 0):
		    	anal_dict[d][name][fea_type]['average']  = 0.0
		    else:
		    	anal_dict[d][name][fea_type]['average'] /= anal_dict[d][name][fea_type]['weights']
		if anal_dict[d][name][fea_type]['average'] > total_anal_dict[fea_type]['max']:
		    total_anal_dict[fea_type]['max'] = anal_dict[d][name][fea_type]['average']
		if anal_dict[d][name][fea_type]['average'] < total_anal_dict[fea_type]['min']:
		    total_anal_dict[fea_type]['min'] = anal_dict[d][name][fea_type]['average']
    for fea_type in total_anal_dict.keys():
	if total_anal_dict[fea_type]['size'] > 0:
	    if basic_funcs.is_float_zero(total_anal_dict[fea_type]['weights'], 0):
	    	total_anal_dict[fea_type]['average']  = 0.0
	    else:
	    	total_anal_dict[fea_type]['average'] /= total_anal_dict[fea_type]['weights']
    for d in anal_dict.keys():
	for name in anal_dict[d].keys():
	    for fea_type in anal_dict[d][name].keys():
		if fea_type == 'score':
		    continue
		min_val = total_anal_dict[fea_type]['min']
		max_val = total_anal_dict[fea_type]['max']
		ave_val = anal_dict[d][name][fea_type]['average']
		if fea_type == '演员':
		    for item in anal_dict[d][name][fea_type]['names']:
			if item['val'] != '-':
			    fea_val = float(item['val'])
			    if fea_val >= 0:
			    	item['score'] = 5 / actor_max * fea_val + 5
			    else:
			    	item['score'] = -5 / actor_min * fea_val + 5
		if ave_val >= 0:
		    if basic_funcs.is_float_zero(max_val, 0):
			anal_dict[d][name][fea_type]['score'] = 5
		    else:
		    	anal_dict[d][name][fea_type]['score'] = 5 / max_val * ave_val + 5
		else:
		    if basic_funcs.is_float_zero(min_val, 0):
		    	anal_dict[d][name][fea_type]['score'] = 5
		    else:
		    	anal_dict[d][name][fea_type]['score'] = -5  / min_val * ave_val + 5
    return anal_dict

def get_shuneng_dict():
    with open('/home/work/chenyaxue/movie/data/shuneng_air') as f:
	line = f.readline()
	line_json = json.loads(line)
    return line_json

if __name__ == '__main__':
    l = get_shuneng_dict()
    print l
