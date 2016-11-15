var basicAnalDict;
$(document).ready(function(){
    var lastMonth = getDateByDelta(-30);
    var nextWeek = getDateByDelta(7);
    var basicPickerObj = $('#basic_range');
    initBasicDateRangePicker(basicPickerObj, lastMonth, nextWeek, basicLoading);
});

function initBasicDateRangePicker(pickerObj, lastMonth, nextWeek, changeFunc) {
    initDateRangePicker(pickerObj, lastMonth, nextWeek, changeFunc);
    changeFunc(lastMonth, nextWeek);
}

function basicLoading(startDate, endDate) {
    var pd={"startDate":startDate, "endDate":endDate, "choice":1};
    $.ajax({
        type:"POST",
        url:"/deep",
	data: pd,
        success:function(msg){
            tableBasicData=msg['totalBasicList'];
    	    var totalBasicFeas = msg['basicFeasDict'];
	    basicFeaTrigger(tableBasicData, totalBasicFeas);
	    basicAnalDict = msg['basicAnalDict'];
        }
    });
}

function basicFeaTrigger(tableBasicData, totalBasicFeas) {
    $('#basic_temp').dataTable({
	destroy:true,
    	"aaSorting": [[ 0, "desc" ], [4, "desc"], [2, "desc"]],
    	data:tableBasicData
    });
    $("#basic_temp").unbind();
    $('#basic_temp').on('click', "tr", function (e) {
	var filmName = $(e.target).parent().children(":eq(1)").children(":eq(0)").html();
	var onDate = $(e.target).parent().children(":eq(0)").html();
	var feaList = totalBasicFeas[onDate][filmName];
	var feaHeadList = ['特证名', '特征值', '权重'];
	var feaStr = feaStrToTable(feaHeadList, feaList);
	popEvent('特征说明', feaStr, e);
    });
}

function getRatingStarsPos(ratingVal, maxRating) {
    var posY = (-11 * parseFloat((1 - parseFloat(ratingVal) / maxRating) * 10).toFixed(0)).toFixed(0);
    var spanHtml = "<span class='ratingStars' style='background-position: 0 " + posY + "px;'></span>"
    return spanHtml;
}

function getCateHtml(cateName, scoreStr) {
    var cateHtml = "<li class='feaCate'>" + cateName + getRatingStarsPos(scoreStr, 10) + getFloatStrByPrecision(scoreStr, 1) + "</li>";
    return cateHtml;
}

function getCateAndJoinNamesHtml(cateName, singleAnalDict) {
    var cateScore = "<li class='feaCate'>" + cateName + "	" + getRatingStarsPos(parseFloat(singleAnalDict[cateName]['score']), 10) + getFloatStrByPrecision(singleAnalDict[cateName]['score'], 1);
    var cateNames = "<ul><li class='feaName'>" + singleAnalDict[cateName]['names'].join() + "</li></ul></li>";
    return cateScore + cateNames;
}

function getNamesScoreHtml(dictList) {
    var nameScoreHtml = '<ul>';
    for (var i = 0; i < dictList.length; i++) {
	var nameDict = dictList[i];
	var nameHtml = "<li class='feaName'>" + nameDict['person'] + "	" + getRatingStarsPos(parseFloat(nameDict['score']), 10) + "	" + getFloatStrByPrecision(nameDict['score'], 1) + "(" + getFloatStrByPrecision(nameDict['val'], 3) + ")";
	nameScoreHtml += nameHtml;
    }
    nameScoreHtml += "</ul>";
    return nameScoreHtml;
}

function analLaunch(t, e) {
    var filmName = $(t).parent().children(":eq(0)").html();
    var onDate = $(t).parent().parent().children(":eq(0)").html();
    var singleAnalDict = basicAnalDict[onDate][filmName];
    var listHtml = "<ul>";
    var movieHtml = getCateHtml(filmName, singleAnalDict['score']);
    listHtml += movieHtml;
    var systemHtml = getCateAndJoinNamesHtml('制式', singleAnalDict);
    listHtml += systemHtml;
    var publisherHtml = getCateAndJoinNamesHtml('发行公司', singleAnalDict);
    listHtml += publisherHtml;
    var producerHtml = getCateAndJoinNamesHtml('制作公司', singleAnalDict);
    listHtml += producerHtml;
    var typeHtml = getCateAndJoinNamesHtml('类型', singleAnalDict);
    listHtml += typeHtml;
    var countryHtml = getCateAndJoinNamesHtml('国家', singleAnalDict);
    listHtml += countryHtml;
    var countryTypeHtml = getCateAndJoinNamesHtml('国家和类型组合', singleAnalDict);
    listHtml += countryTypeHtml;
    var ipHtml = getCateAndJoinNamesHtml('ip信息', singleAnalDict);
    listHtml += ipHtml;
    var directorHtml = getCateAndJoinNamesHtml('导演', singleAnalDict);
    listHtml += directorHtml;
    var writerHtml = getCateAndJoinNamesHtml('编剧', singleAnalDict);
    listHtml += writerHtml;
    var actorScoreHtml = "<li class='feaCate'>" + '演员' + getRatingStarsPos(singleAnalDict['演员']['score'], 10) + getFloatStrByPrecision(singleAnalDict['演员']['score'], 1);
    listHtml += actorScoreHtml;
    var actorNamesHtml = getNamesScoreHtml(singleAnalDict['演员']['names']);
    listHtml += actorNamesHtml;
    listHtml += "</li>";
    listHtml += "</ul>";
    popEvent('分析报告', listHtml, e);
}
