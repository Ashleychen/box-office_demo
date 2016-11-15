var limitBoxofficeMVDict;
var weekChart;
var boxofficeSummaryWeekDict;
$(document).ready(function(){
    $.ajax({
        type: "POST",
        url: "/week",
	data: {},
	dataType: "json",
	success:function(msg) {
	    var maxPreDate = msg['maxPreDate'];
	    var minPreDate = msg['minPreDate'];
	    boxofficeSummaryWeekDict = msg['boxofficeSummaryWeekDict'];
	    limitBoxofficeMVDict = msg['limitBoxofficeMVDict'];
	    weekChart = echarts.init(document.getElementById('weekMain'));
	    initiateDatepicker(maxPreDate, minPreDate);
	    changeContent(maxPreDate, maxPreDate, minPreDate);
	    var weeklyErrList = msg['weeklyErrList'];
	    getErrs(weeklyErrList);
	},
    });
});

function initiateDatepicker(maxPreDate, minPreDate) {
    initDatePicker($("#weekDate"), minPreDate, maxPreDate, maxPreDate, pickerChangeTrigger);
    $(".choose_forcast_d").on("click",".pre_d",function(){
        var selected = $('#weekDate').val();
	var preDate = getDateByDeltaAndDate(selected, -1);
	$('#weekDate').val(preDate);
	changeContent(preDate, maxPreDate, minPreDate);
    });
    $(".choose_forcast_d").on("click",".aft_d",function(){
   	var selected = $('#weekDate').val();
	var aftDate = getDateByDeltaAndDate(selected, 1);
	$('#weekDate').val(aftDate);
	changeContent(aftDate, maxPreDate, minPreDate);
    });
}

function pickerChangeTrigger(minPreDate, maxPreDate, selected) {
    changeContent(selected, maxPreDate, minPreDate);
}

function changeContent(selectedDate, maxPreDate, minPreDate) {
    weeklyDisplay(boxofficeSummaryWeekDict, selectedDate);
    var multiList = getMultiList(boxofficeSummaryWeekDict, selectedDate);
    displayWeekChart(multiList, weekChart, selectedDate, maxPreDate);
    popChart(selectedDate);
    compDate(minPreDate, selectedDate, maxPreDate);
}

function weeklyDisplay(boxofficeSummaryWeekDict, preDate) {
    var tableHtml = '';
    var preWeekRange = getCurrentWeekRange(preDate);
    $('#weekRange').html(preWeekRange);
    if (boxofficeSummaryWeekDict.hasOwnProperty(preDate) && boxofficeSummaryWeekDict[preDate].hasOwnProperty(preWeekRange)) {
    	var boxSumWeekList = boxofficeSummaryWeekDict[preDate][preWeekRange];
    	for (var i = 0; i < boxSumWeekList.length; i++) {
	    if (parseInt(boxSumWeekList[i][1]) <= 7) {
	    	var trHtml = '<tr class="pop" style="background-color:#FFB5C5">';
	    } else {
	    	var trHtml = '<tr class="pop">';
	    }
	    trHtml += '<td>' + boxSumWeekList[i][2] + '</td>';
	    trHtml += '<td>' + boxSumWeekList[i][0] + '</td>';
	    trHtml += '<td>' + boxSumWeekList[i][1] + '</td>';
	    trHtml += '<td>' + boxSumWeekList[i][3] + '</td>';
	    trHtml += '<td>' + boxSumWeekList[i][5] + '</td>';
	    trHtml += '<td>' + boxSumWeekList[i][4] + '</td>';
	    trHtml += '</tr>';
	    tableHtml += trHtml;
    	}
    }
    $('#week_table').html(tableHtml);
}

function getMultiList(boxofficeSummaryWeekDict, selectedDate) {
    var nameList = new Array();
    var preList = new Array();
    var realList = new Array();
    var shunengList = new Array();
    var selectedWeekRange = getCurrentWeekRange(selectedDate);
    if (boxofficeSummaryWeekDict.hasOwnProperty(selectedDate) && boxofficeSummaryWeekDict[selectedDate].hasOwnProperty(selectedWeekRange)) {
	var boxSumWeekList = boxofficeSummaryWeekDict[selectedDate][selectedWeekRange];
    	for (var i = 0; i < boxSumWeekList.length; i++) {
	    nameList.push(boxSumWeekList[i][2]);
	    preList.push(boxSumWeekList[i][3]);
	    realList.push(boxSumWeekList[i][4]);
	    shunengList.push(boxSumWeekList[i][5]);
    	}
    }
    return [nameList, preList, realList, shunengList];
}


function displayWeekChart(multiList, weekChart, selected, maxPreDate) {
    var baiduErrList = getErrList(multiList[1], multiList[2]);
    var shunengErrList = getErrList(multiList[3], multiList[2]);
    var limitNameList = new Array();
    var limitBaiduErrs = new Array();
    var limitShunengErrs = new Array();
    for (var i = 0; i < multiList[0].length; i++) {
	if (i < 10 && shunengErrList[i] != '--') {
	    limitNameList.push(multiList[0][i]);
	    limitBaiduErrs.push(baiduErrList[i]);
	    limitShunengErrs.push(shunengErrList[i]);
	}
    }
    var maxDate = getDateFromStr(maxPreDate);
    var maxWeekDay = maxDate.getDay();
    if (maxWeekDay <= 2 && maxWeekDay != 0) {
	var deltaDays = getTimeDeltaDaysByDate(selected, maxPreDate);
	if (deltaDays < maxWeekDay || limitNameList.length == 0) {
	    $('#weekBlock').hide();
	} else {
	    $('#weekBlock').show();
	}
    } else if (limitNameList.length == 0) {
	$('#weekBlock').hide();
    } else {
	$('#weekBlock').show();
    }
    weekOption.xAxis.data = limitNameList;
    weekOption.series[0].data = limitBaiduErrs;
    weekOption.series[1].data = limitShunengErrs;
    weekChart.setOption(weekOption, true);
}
function getErrs(weeklyErrList) {
    var lineCate = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天'];
    var tableHtml = ErrorListToHtml(lineCate, trimFloatList(weeklyErrList, 4), 7, 6);
    $('#errorTable').html(tableHtml);
}

function getMVLists(mvList, preDate) {
    var dateList = new Array();
    var preList = new Array();
    var rateList = new Array();
    for (var i = 0; i < mvList.length; i++) {
	dateList.push(mvList[i][0]);
	preList.push(mvList[i][1]);
	rateList.push(mvList[i][2]);
    }
    var theDate = getDateByDeltaAndDate(preDate, 0);
    var weekday = getDateFromStr(theDate).getDay();
    var startDate = getDateByDeltaAndDate(preDate, -( weekday - 1));
    var completeDateList = new Array();
    var completePreList = new Array();
    var completeRateList = new Array();
    for (var i = 0;  i < 7; i++) {
	var curDate = getDateByDeltaAndDate(startDate, i);
	var ind = dateList.indexOf(curDate);
	if (ind != -1) {
	    completeDateList.push(dateList[ind]);
	    completePreList.push(preList[ind]);
	    completeRateList.push(rateList[ind]);
	} else {
	    completeDateList.push(curDate);
	    completePreList.push('--');
	    completeRateList.push('--');
	}
    }
    return [completeDateList, completePreList, completeRateList];
}
function displayMVChart(multiList, mvChart) {
    weekMvOption.xAxis.data = multiList[0];
    weekMvOption.series[0].data = multiList[1];
    weekMvOption.series[1].data = multiList[2];
    mvChart.setOption(weekMvOption, true);
}

function popChart(preDate) {
    $(".pop").click(function(e) {
        var filmName = $(e.target).parent().children(":eq(0)").html();
        var htmlStr = writePopChart("'movieWrapper'", "'movieMain'");
	var multiList = getMVLists(limitBoxofficeMVDict[preDate][filmName], preDate);
	var headList = ['日期', '百度预测', '排片率'];
	htmlStr += detailStrToTable(headList, multiList);
	popEvent('每日票房和排片预测趋势', htmlStr, e);
	var mvChart = echarts.init(document.getElementById('movieMain'));
	displayMVChart(multiList, mvChart)
    });
}
