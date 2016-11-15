var battleDict;
$(document).ready(function(){
    aveChart = echarts.init(document.getElementById('aveLine'));
    $.ajax({
        type: 'POST',
        url: "/battle",
        success:function(msg){
            maxDate = msg['lastDate'];
            minDate = msg['firstDate'];
	    battleDict = msg['dict'];
            var defaultDate = maxDate;
            var battlePicker = $("#battle");
            initDatePicker(battlePicker, minDate, maxDate, defaultDate, controlDisplay);
            controlDisplay(minDate, maxDate, defaultDate);
            $(".choose_forcast_d").on("click",".pre_d",function(){
                controlDisplayBydelta(minDate, maxDate, -1);
            })
            $(".choose_forcast_d").on("click",".aft_d",function(){
                controlDisplayBydelta(minDate, maxDate, 1);
            });
            displayPicker(msg);
            displayErr(msg);
            displayAveChart(msg);
        }
    });
});

function controlDisplay(startDate, endDate, selectedDate) {
    var changeDate = getFormattedDate(getDateFromStr(selectedDate));
    displayBattle(battleDict, selectedDate);
    compDate(startDate, changeDate, endDate);
}

function controlDisplayBydelta(minDate, maxDate, delta) {
    var curDate=$("#battle").val();
    var newDate = getDateByDeltaAndDate(curDate, delta);
    $("#battle").datepicker('setDate', getDateFromStr(newDate));
    controlDisplay(minDate, maxDate, newDate);
}

var aveChart;
function displayBattle(battleDict, myDate) {
    var table_html = "";
    $("#winner").html('winner is:       ' + battleDict[myDate]['winner']);
    var dateDict = battleDict[myDate];
    for(var i = 0; i < dateDict['list'].length; i++) {
        var tr_str = "<tr>";
	var name_str = "<td id='nametd'>" + dateDict['list'][i]['basics'][3] + "</td>";
	var pre_str = numToTdHtmlByPrecision(dateDict['list'][i]['basics'][4], 1);
	var err_str = numToTdHtmlByPrecision(dateDict['bd_errs'][i], 2);
	var shuneng_str = numToTdHtmlByPrecision(dateDict['list'][i]['shuneng'], 1);
	var shuneng_err = numToTdHtmlByPrecision(dateDict['shuneng_errs'][i], 2);
	var real_str = numToTdHtmlByPrecision(dateDict['list'][i]['basics'][5], 1);
        var seq_str = numToTdHtmlByPrecision(dateDict['list'][i]['basics'][6], 1);
	if (parseInt(dateDict['bd_scores'][i]) > parseInt(dateDict['shuneng_scores'][i])) {
            var score_str = "<td>" +  dateDict['win'][i] + "\t" + dateDict['bd_scores'][i] + "</td>";
	} else if (parseInt(dateDict['bd_scores'][i]) < parseInt(dateDict['shuneng_scores'][i])) {
            var score_str = "<td>" +  dateDict['win'][i] + "\t" + dateDict['shuneng_scores'][i] + "</td>";
	} else {
            var score_str = "<td>0</td>";
	}
        table_html += tr_str + name_str + pre_str + err_str + shuneng_str + shuneng_err + real_str + score_str + seq_str + "</tr>";
        }
    $('#battle_table').html(table_html);
}

function displayPicker(msg) {
    var sd = msg['firstDate'];
    var ed = msg['lastDate'];
    initDateRangePicker($('#date_range'), sd, ed, scoreRangePickerTrigger);
    scoreByRangePicker(sd, ed, battleDict);
}

function scoreRangePickerTrigger(startDate, endDate) {
    scoreByRangePicker(startDate, endDate, battleDict);
}

function scoreByRangePicker(startDate, endDate, battleDict) {
    var score = calScore(startDate, endDate, battleDict);
    var bdScore = score[0];
    var shunengScore = score[1];
    var bdTimes = score[2];
    var shunengTimes = score[3];
    $("#bdScore").html("baidu\t" + bdTimes + "(" + bdScore + ")");
    $("#shunengScore").html("shuneng\t" + shunengTimes + "(" + shunengScore + ")");
}

function calScore(firstDate, lastDate, battleDict) {
    var bdScore = 0;
    var shunengScore = 0;
    var bdTimes = 0;
    var shunengTimes = 0;
    for (var iterDate in battleDict) {
	if (iterDate >= firstDate && iterDate <= lastDate) {
	    bdScore += parseInt(battleDict[iterDate]['bd_score']);
	    shunengScore += parseInt(battleDict[iterDate]['shuneng_score']);
	    if (parseInt(battleDict[iterDate]['bd_score']) > parseInt(battleDict[iterDate]['shuneng_score'])) {
		bdTimes += 1;
	    } else if (parseInt(battleDict[iterDate]['bd_score']) < parseInt(battleDict[iterDate]['shuneng_score'])) {
		shunengTimes += 1;
	    }
	}
    }
    var scores = new Array(bdScore, shunengScore, bdTimes, shunengTimes);
    return scores
}

function displayErr(msg) {
    var sd = msg['firstDate'];
    var ed = msg['lastDate'];
    initDateRangePicker($('#err_range'), sd, ed, getBattleErr);
    getBattleErr(sd, ed);
}

function getBattleErr(startDate, endDate){
    var url="/battleErr";
    var pd={"startDate":startDate, "endDate":endDate};
    $.ajax({
        type: "GET",
        url: url,
        data: pd,
        success:function(msg){
	    var lineCate = ['数能预测', '百度预测A', '百度预测B'];
	    var battleErrs = msg['battleErrs'];
	    var tableHtml = ErrorListToHtml(lineCate, battleErrs, 3, 7);
	    $('#battleErr').html(tableHtml);
        }
    });
}

function displayAveChart(msg) {
    aveOption.xAxis.data = msg['dates'];
    aveOption.series[0].data = msg['bdRates'];
    aveChart.setOption(aveOption, true);
    displayAveTable(msg);
}

function displayAveTable(msg) {
    var tableHtml = '';
    var maxLen = Math.min(msg['dates'].length, 10);
    for (var i = msg['dates'].length - 1; i >= msg['dates'].length - maxLen; i--) {
	var dateStr = "<td>" + msg['dates'][i] + "</td>";
	var rateStr = "<td>" + msg['bdRates'][i] + "</td>";
	tableHtml += "<tr>" + dateStr + rateStr + "</tr>";
    }
    $("#aveTable").html(tableHtml);
}
