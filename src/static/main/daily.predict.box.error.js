var tchart;
var eChart;
$(document).ready(function(){
    $.ajax({
        type: "POST",
        url: '/',
	data: {'choice': 1},
	success:function(msg){
	    tchart = echarts.init(document.getElementById('tmain'));
	    eChart = echarts.init(document.getElementById('emain'));
	    var maxDate = msg['maxDate'];
	    var minDate = msg['minDate'];
	    var defaultDate = getDateByDelta(0);
	    var forcastPicker = $("#forcast");
	    initDatePicker(forcastPicker, minDate, maxDate, defaultDate, controlDisplay);
	    controlDisplay(minDate, maxDate, defaultDate);
	    getErrCompare()
	    $(".choose_forcast_d").on("click",".pre_d",function(){
		controlDisplayBydelta(minDate, maxDate, -1);
	    });

	    $(".choose_forcast_d").on("click",".aft_d",function(){
		controlDisplayBydelta(minDate, maxDate, 1);
	    });
	}
    });
});

function controlDisplayBydelta(minDate, maxDate, delta) {
    var curDate=$("#forcast").val();
    var newDate = getDateByDeltaAndDate(curDate, delta);
    $("#forcast").datepicker('setDate', getDateFromStr(newDate));
    controlDisplay(minDate, maxDate, newDate);
}

function controlDisplay(startDate, endDate, selectedDate) {
    var changeDate = getFormattedDate(getDateFromStr(selectedDate));
    getForcastCompare(changeDate);
    compDate(startDate, changeDate, endDate);
}

function getForcastCompare(date){	
    var url="/";
    var pd={"choice": 2, "theDay":date};
    $.ajax({
        type: "POST",
        url: url,
        data: pd,
        success:function(msg){
	    //当日预测票房与实际票房比较
	    displayCompare(msg);
	    //当日误差
	    displayBarChart(msg);
    	    popFeatures(msg);
        }
    }); 
}

function getErrCompare(){	
    var url="/";
    var pd={"choice": 3};
    $.ajax({
        type: "POST",
        url: url,
        data: pd,
        success:function(msg){
	    var top5ErrWeekday = msg['top5ErrWeekday'];
	    var totalErrWeekday = msg['totalErrWeekday'];
	    var totalErrTotal = new Array();
	    var summaryErrTotal = msg['summaryErrTotal'];
	    var accErrTotal = msg['accErrTotal'];
	    var mixTop5ErrTotal = msg['mixTop5ErrTotal'];
	    var mixTotalErrTotal = msg['mixTotalErrTotal'];
	    var firstTop5ErrTotal = msg['firstTop5ErrTotal'];
	    var firstTotalErrTotal = msg['firstTotalErrTotal'];
	    var nextTop5ErrTotal = msg['nextTop5ErrTotal'];
	    var nextTotalErrTotal = msg['nextTotalErrTotal'];
	    totalErrTotal.push(summaryErrTotal);
	    totalErrTotal.push(accErrTotal[0]);
	    totalErrTotal.push(mixTop5ErrTotal[0]);
	    totalErrTotal.push(mixTotalErrTotal[0]);
	    totalErrTotal.push(firstTop5ErrTotal[0]);
	    totalErrTotal.push(firstTotalErrTotal[0]);
	    totalErrTotal.push(nextTop5ErrTotal[0]);
	    totalErrTotal.push(nextTotalErrTotal[0]);
	    totalErrTotal.push(summaryErrTotal);
            totalErrTotal.push(accErrTotal[1]);
            totalErrTotal.push(mixTop5ErrTotal[1]);
            totalErrTotal.push(mixTotalErrTotal[1]);
            totalErrTotal.push(firstTop5ErrTotal[1]);
            totalErrTotal.push(firstTotalErrTotal[1]);
            totalErrTotal.push(nextTop5ErrTotal[1]);
            totalErrTotal.push(nextTotalErrTotal[1]);
	    var lineCate = ['预测票房A','预测票房B'];
	    //TOP5误差
	    var top5WeekdayErrsStr = ErrorListToHtml(lineCate, trimFloatList(top5ErrWeekday, 4), 2, 7);
    	    $("#top5_weekday_err").html(top5WeekdayErrsStr);
	    //电影整体误差
	    var elseWeekdayErrsStr = ErrorListToHtml(lineCate, trimFloatList(totalErrWeekday, 4), 2, 7);
    	    $("#else_weekday_err").html(elseWeekdayErrsStr);
	    //其余误差指标
	    var globErrsStr = ErrorListToHtml(lineCate, trimFloatList(totalErrTotal, 4), 2, 8);
    	    $("#glob_error").html(globErrsStr);
        }
    });
}
