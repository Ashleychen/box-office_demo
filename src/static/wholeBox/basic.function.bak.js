var firstMovieDict;
var firstErrDict;
$(document).ready(function(){
    initFirstDatePicker(firstLoading);
});

function initFirstDatePicker(changeFunc) {
    var pd={"choice": 1};
    $.ajax({
        type:"POST",
        url:"/wholeBox",
        data: pd,
        success:function(msg){
            var firstMinDate=msg['firstMinDate'];
            var firstMaxDate= msg['firstMaxDate'];
	    var defaultDate = firstMaxDate;
    	    var firstPickerObj = $('#first_range');
    	    initDatePicker(firstPickerObj, firstMinDate, firstMaxDate, defaultDate, changeFunc);
    	    changeFunc(firstMinDate, firstMaxDate, defaultDate);
	    firstMovieDict = msg['firstMovieDict'];
	    firstErrDict = msg['firstErrDict'];
	    getErrTable(firstErrDict);
        }
    });
}

function firstLoading(minDate, maxDate, preDate) {
    var pd={"preDate":preDate, "choice": 2};
    $.ajax({
        type:"POST",
        url:"/wholeBox",
	data: pd,
        success:function(msg){
            tableFirstData=msg['totalFirstList'];
	    var totalFirstFeas = msg['firstFeasDict'];
	    firstFeaTrigger(tableFirstData, totalFirstFeas, preDate);
        }
    });
}

function firstFeaTrigger(tableFirstData, totalFirstFeas, preDate) {
    $('#tb_temp').dataTable({
	destroy:true,
    	"aaSorting": [[ 0, "desc" ], [4, "desc"], [2, "desc"]],
    	data:tableFirstData
    });
    $("#tb_temp").unbind();
    $('#tb_temp').on( 'click', "tr", function (e) {
	var filmName = $(e.target).parent().children(":eq(1)").html();
	var feaList = totalFirstFeas[preDate][filmName];
	var feaHeadList = ['特证名', '特征值', '权重'];
	var feaStr = feaStrToTable(feaHeadList, feaList);
	var chartStr = writePopChart("'firstWrapper'", "'firstMain'");
	var detailDict = firstMovieDict[filmName];
	var detailLists = [detailDict['dateList'], detailDict['preList'], detailDict['smoothList'], detailDict['shunengList'], detailDict['realList']];
	var detailHeadList = ['日期', '百度预测A', '百度预测B', '数能预测', '实时票房'];
	var detailStr = detailStrToTable(detailHeadList, detailLists);
	popEvent('特征说明', chartStr + detailStr + feaStr, e);
	var detailChart = echarts.init(document.getElementById('firstMain'));
        displayDetailChart(detailDict, detailChart)
    });
}

function displayDetailChart(detailDict, detailChart) {
    firstDetailOption.xAxis.data = detailDict['dateList'];
    firstDetailOption.series[0].data = detailDict['preList'];
    firstDetailOption.series[1].data = detailDict['smoothList'];
    firstDetailOption.series[2].data = detailDict['shunengList'];
    firstDetailOption.series[3].data = detailDict['realList'];
    detailChart.setOption(firstDetailOption, true);
}

function isDataValid(preA, preB, preShuneng, real) {
    var invalidList = ['-', '--', '——'];
    if (invalidList.indexOf(preA) != -1 || invalidList.indexOf(preB) != -1 || invalidList.indexOf(preShuneng) != -1 || invalidList.indexOf(real) != -1) {
	return false;
    } else {
	return true;
    }
}

function getErrTable(firstErrDict) {
    var dayList = new Array();
    var errList = new Array();
    for (var d in firstErrDict) {
	dayList.push(d);
    }
    dayList.sort(function sortNumber(a, b) {return parseInt(a) - parseInt(b)});
    for (var j = 0; j < dayList.length; j++) {
	for (var i = 0; i < firstErrDict[dayList[j]].length; i++) {
	    errList.push(firstErrDict[dayList[j]][i]);
	}
    }
    var tableHtml = ErrorListToHtml(dayList, trimFloatList(errList, 4), dayList.length, 6);
    $('#wholeErrorTable').html(tableHtml);
}
