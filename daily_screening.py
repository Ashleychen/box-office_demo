#coding=utf-8
#单部电影排片率趋势
def group_by_film(daily_scr):
    scr_by_movie = {}
    for d in daily_scr.keys():
	for id in daily_scr[d].keys():
            if daily_scr[d][id][3] not in scr_by_movie.keys():
            	scr_by_movie[daily_scr[d][id][3]] = []
            scr_by_movie[daily_scr[d][id][3]].append(daily_scr[d][id])
    for name in scr_by_movie.keys():
        scr_by_movie[name].sort(key=lambda x:x[0])
    return scr_by_movie
