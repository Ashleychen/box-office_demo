function numToHtml(num) {
   if (num != '-' && num != '--') {
	var htmlStr = "<td>" + parseFloat(num).toFixed(1) + "</td>";
   } else {
	var htmlStr = "<td>--</td>";
   }
   return htmlStr;
}
function rewriteDateStr(dateObj) {
    var yearStr = dateObj.getFullYear();
    var monthStr = dateObj.getMonth() + 1;
    if (parseInt(monthStr) < 10) {
        monthStr = "0" + monthStr;
    }
    var dayStr = dateObj.getDate();
    if (parseInt(dayStr) < 10) {
        dayStr = "0" + dayStr;
    }
    var dateRewStr =  yearStr + '-' + monthStr + '-' + dayStr;
    return dateRewStr;
}

function comp_date(min_date, current_date, max_date) {
    if (current_date <= min_date) {
        $("#pre_d").attr("class","pre_gray_d" );
    }
    if (current_date >= max_date) {
        $("#aft_d").attr("class","aft_gray_d" );
    }
    if (current_date > min_date && current_date < max_date) {
        $("#pre_d").attr("class","pre_d" );
        $("#aft_d").attr("class","aft_d" );
    }
}

function get_datetime(curDate, delta){
    if(curDate == ''){
        var curDate = new Date();
    } else {
	var curDate = new Date(Date.parse(curDate));
    }
    var preDate = new Date();
    preDate.setTime(curDate.getTime() + delta*24*60*60*1000);
    var preStr = rewriteDateStr(preDate);
    $("#forcast").val(preStr);
    return preStr;
}

function rangeListToStr(rangeList, errList, summaryErrDate, accErrDate) {
    var newErrList = new Array();
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
	    newErrList[rangeStr] = parseFloat(errList[i]).toFixed(4);
	}
    }
    if (Math.abs(parseFloat(summaryErrDate) + 1.0) > 1e-6) {
        newErrList['大盘'] = parseFloat(summaryErrDate).toFixed(4);
	rangeStrList.push('大盘');
    }
    if (Math.abs(parseFloat(accErrDate) + 1.0) > 1e-6) {
        newErrList['大盘(累积)'] = parseFloat(accErrDate).toFixed(4);
    	rangeStrList.push('大盘(累积)');
    }
    return [rangeStrList, newErrList];
}

function trimDailyErrs(errList) {
    var newErrList = new Array();
    for (var i in errList) {
        if (parseFloat(errList[i]) > 0.5) {
            newErrList.push('0.5');
        } else {
            newErrList.push(errList[i]);
        }
    }
    return newErrList;
}

function showOrHide(rangeStrList, errList, dailyOption) {
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
	displayDailyErrTable(errList);
	dailyOption.xAxis.data = rangeStrList;
	var trimTooltipErrs = trimDailyErrs(errList);
	dailyOption.series[0].data = trimTooltipErrs;
	eChart.setOption(dailyOption, true);
    }
}

function displayDailyErrTable(errList) {
    errorHtml = "";
    for (var i in errList) {
        var rangeCol = "<td>" + i + "</td>";
        var errCol = "<td>" + parseFloat(errList[i]).toFixed(4) + "</td>";
        errorHtml += "<tr>" + rangeCol + errCol + "</tr>";
    }
    $('#error_table').html(errorHtml);
}

function popFeatures(msg) {
    var dailyList = msg['dailyList'];
    var feaMap = getFeatureDict(dailyList);
    $(".pop").click(function(e) {
        var filmName = $(e.target).parent().children(":eq(0)").children(":eq(0)").html();
        var feaList = feaMap[filmName];
        var feaStr = feaStrToTable(feaList);
    	layer.open({
            type: 1,
	        title: '特征说明',
	        closeBtn: 0,
            area: ['600px', '360px'],
            shadeClose: true, //点击遮罩关闭
            content: '\<\div style="padding:20px;">'+ feaStr+'\<\/div>'
    	});
	    var top = e.clientY;
	    document.querySelector(".layui-layer").style.top = top + "px";
    });
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

function feaStrToTable(feaList) {
    var tableHtml = '<table class="table">';
    var thStr = '<tr><th>特征名</th><th>特征值</th><th>权重</th></tr>';
    tableHtml += thStr;
    for (var i = 0; i < feaList.length; i++) {
        var trStr = '<tr>';
        for (var j = 0; j < feaList[i].length; j++) {
            trStr += '<td>' + feaList[i][j] + '</td>';
        }
        trStr += '</tr>';
        tableHtml += trStr;
    }
    tableHtml += '</table>'
    return tableHtml;
}
