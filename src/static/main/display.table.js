function displayCompare(msg) {
    var tableHtml = '';
    var firstDayList = msg['firstDayList'];
    var beforeDayList = msg['beforeDayList'];
    var dailyList = msg['dailyList'];
    if (dailyList.length == 0) {
        $('#dailyBox').html(tableHtml);
	return;
    }
    var summaryList = dailyList[0];
    if (summaryList[2] == '-') {
	summaryList[2] = '--';
    }
    var summaryHtml = "<tr><td><a href='javascript:void(0);' onclick='summaryLaunch(this, event)'>大盘</a></td><td>" + summaryList[1] + "</td><td>--</td><td>" + summaryList[2] + "</td><td>--</td></tr>";
    var accList = dailyList[1];
    var accHtml = "<tr><td><a href='javascript:void(0);' onclick='summaryLaunch(this, event)'>大盘(累积)</a></td><td>" + accList[0] + "</td><td>" + accList[1] + "</td><td>" + accList[2] + "</td><td>--</td></td>";
    var tableHtml = summaryHtml + accHtml;
    for(var i = 2; i < dailyList.length; i++) {
	var enID = dailyList[i]['basics'][1];
	if ($.inArray(enID, firstDayList) != -1) {
            var trStr = "<tr class='first_day pop' style='background-color:#FFB5C5'>";
	} else if ($.inArray(enID, beforeDayList) != -1) {
	    var trStr = "<tr class='before_day pop' style='background-color:#b5e0ff'>";
	} else {
            var trStr = "<tr class='pop'>";
        }
	if ($.inArray(enID, beforeDayList) != -1) {
            var nameStr = "<td id='nametd'><a id='namel' href='javascript:void(0);'>" +
	    	dailyList[i]['basics'][3] + "</a>	<a class='btn btn-default btn-xs' id='lbtn' href='http://www.cbooo.cn/m/" +
	    	enID + "'>详情</a></td>";
	} else {
            var nameStr = "<td id='nametd'><a id='namel' href='javascript:void(0);' onclick='launch(this, event)'>" +
	    	dailyList[i]['basics'][3] + "</a>	<a class='btn btn-default btn-xs' id='lbtn' href='http://www.cbooo.cn/m/" +
	    	enID + "'>详情</a></td>";
	}
	var preAStr = numToTdHtmlByPrecision(dailyList[i]['basics'][4], 1);
	var preBStr = numToTdHtmlByPrecision(dailyList[i]['basics'][7], 1);
	var realStr = numToTdHtmlByPrecision(dailyList[i]['basics'][5], 1);
	var seqStr = numToTdHtmlByPrecision(dailyList[i]['basics'][6], 1);
        trStr += nameStr + preAStr + preBStr + realStr + seqStr + "</tr>";
	tableHtml += trStr;
    }
    $('#dailyBox').html(tableHtml);
}
function rangeListToStr(rangeList, errList, summaryErrDate, accErrDate) {
    var newErrDict = new Array();
    var rangeStrList = new Array();
    for (var i = 0; i < rangeList.length; i++) {
        if (Math.abs(parseFloat(errList[i]) + 1.0) > 1e-6 && Math.abs(parseFloat(errList[i]) - 0.0) > 1e-6) {
            if (i == 0) {
                var rangeStr = "<=" + rangeList[i][1];
            } else if ( i == rangeList.length - 1) {
                var rangeStr = ">=" + rangeList[i][0];
            } else {
                var rangeStr = "(" + rangeList[i][0] + "," + rangeList[i][1] + "]";
            }
            rangeStrList.push(rangeStr);
            newErrDict[rangeStr] = parseFloat(errList[i]).toFixed(4);
        }
    }
    if (Math.abs(parseFloat(summaryErrDate) + 1.0) > 1e-6) {
        newErrDict['大盘'] = parseFloat(summaryErrDate).toFixed(4);
        rangeStrList.push('大盘');
    }
    if (Math.abs(parseFloat(accErrDate) + 1.0) > 1e-6) {
        newErrDict['大盘(累积)'] = parseFloat(accErrDate).toFixed(4);
        rangeStrList.push('大盘(累积)');
    }
    return [rangeStrList, newErrDict];
}

//main每日误差控制图和表格的显示
function showOrHide(rangeStrList, rangeErrDict, dailyOption) {
    if (rangeStrList.length == 0) {
        $('#ewrapper').hide();
        $('#twrapper').hide();
        $('#trend_list').hide();
        $('#error_list').hide();
    } else {
        $('#ewrapper').show();
        $('#twrapper').hide();
        $('#error_list').show();
        $('#error_div').html('误差列表');
        $('#trend_list').hide();
        displayDailyErrTable(rangeErrDict);
        dailyOption.xAxis.data = rangeStrList;
        var trimTooltipErrs = trimDailyErrs(rangeErrDict);
        dailyOption.series[0].data = trimTooltipErrs;
        eChart.setOption(dailyOption, true);
    }
}

function displayDailyErrTable(dailyErrDict) {
    errorHtml = "";
    for (var i in dailyErrDict) {
        var rangeCol = "<td>" + i + "</td>";
        var errCol = numToTdHtmlByPrecision(dailyErrDict[i], 4);
        errorHtml += "<tr>" + rangeCol + errCol + "</tr>";
    }
    $('#error_table').html(errorHtml);
}

function displayBarChart(msg) {
    var errADate = msg['errADate'];
    var summaryErrDate = msg['summaryErrDate'];
    var accErrDate = msg['accErrDate'];
    var errRangeList = msg['errRangeList'];
    var returnList = rangeListToStr(errRangeList, errADate, summaryErrDate, accErrDate);
    var rangeStrList = returnList[0];
    var rangeErrDict = returnList[1];
    showOrHide(rangeStrList, rangeErrDict, dailyRangeOption);
}

function getFeatureDict(dailyList){
    var feaMap = new Array();
    for (var i = 2; i < dailyList.length; i++) {
        var item = dailyList[i];
        var features = item['feas'];
        var name = item['basics'][3];
        feaMap[name] = features;
    }
    return feaMap;
}

function popFeatures(msg) {
    var dailyList = msg['dailyList'];
    var feaMap = getFeatureDict(dailyList);
    var popObj = $(".pop");
    popObj.click(function(e) {
	var filmName = $(e.target).parent().children(":eq(0)").children(":eq(0)").html();
        var feaList = feaMap[filmName];
	var nameList = new Array();
	var valList = new Array();
	var weightList = new Array();
	var multiList = [nameList, valList, weightList];
	for (var i = 0; i < 3; i++) {
	    for (var j = 0; j < feaList.length; j++) {
		multiList[i].push(feaList[j][i]);
	    }
	}
	var headList = ['特征名', '特征值', '权重'];
        var feaStr = detailStrToTable(headList, multiList);
    	popEvent('特征说明', feaStr, e);
    });
}

function summaryLaunch(t, e) {
    $('#twrapper').show();
    $('#ewrapper').hide();
    $('#error_list').hide();
    $('#trend_list').show();
    var filmName = $(t).parent().children(":eq(0)").html();
    $('#error_div').html(filmName);
    $.ajax({
        type:"GET",
        data:{'filmName':filmName},
        url:"/lmain",
        success:function(msg){
            dapanTrendOption.xAxis.data = msg['dateList'];
            dapanTrendOption.series[0].data = msg['preAList'];
            dapanTrendOption.series[1].data = msg['preBList'];
            dapanTrendOption.series[2].data = msg['realList'];
            tchart.setOption(dapanTrendOption, true);
            displayTrendList(msg['dateList'], msg['preAList'], msg['realList'], msg['preBList'], filmName);
        }
    });
}
function launch(t, e) {
    $('#twrapper').show();
    $('#ewrapper').hide();
    $('#error_list').hide();
    $('#trend_list').show();
    var filmName = $(t).parent().children(":eq(0)").html();
    $.ajax({
        type:"GET",
        data:{'filmName':filmName},
        url:"/lmain",
        success:function(msg){
            singleTrendOption.xAxis.data = msg['dateList'];
            singleTrendOption.series[0].data = msg['preAList'];
            singleTrendOption.series[1].data = msg['preBList'];
            singleTrendOption.series[2].data = msg['realList'];
            tchart.setOption(singleTrendOption, true);
            displayTrendList(msg['dateList'], msg['preAList'], msg['realList'], msg['preBList'], filmName);
        }
    });
}
function displayTrendList(dateList, preAList, realList, preBList, filmName) {
    var htmlStr = "";
    var listLen = dateList.length;
    var maxLen = Math.min(10, listLen);
    for (var i = listLen - maxLen; i < listLen; i++) {
        var dateStr = "<td>" + dateList[i] + "</td>";
        var preStr = "<td>" + preAList[i] + "</td>";
        var preBStr = "<td>" + preBList[i] + "</td>";
        var realStr = "<td>" + realList[i] + "</td>";
        htmlStr += "<tr>" + dateStr + preStr + preBStr + realStr + "</tr>";
    }
    $('#trend_div').html(filmName);
    $('#trend_table').html(htmlStr);
}
