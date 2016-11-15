$(document).ready(function(){
    var sd = getBasicDate()[0];
    var ed = getBasicDate()[1];
    $('#basic_range').daterangepicker(
    {
        locale: {
        format: 'YYYY-MM-DD'
        },
        startDate: sd,
        endDate: ed,
        "autoApply": true,
    },
    function(start, end, label) {
        var firstDate = start.format('YYYY-MM-DD');
        var lastDate = end.format('YYYY-MM-DD');
	loading(firstDate, lastDate, 2);
    });
    loading(sd, ed, 1);
});

function appendZero(s) {
    return ("00"+ s).substr((s+"").length);
}

function getFormattedDate(curDate) {
    return curDate.getFullYear() + "-" + appendZero(curDate.getMonth() + 1) + "-" + appendZero(curDate.getDate());
}

function getBasicDate() {
    var startDate = new Date();
    var endDate = new Date();
    startDate.setDate(startDate.getDate() - 30);
    endDate.setDate(endDate.getDate() + 7);
    var startDate = getFormattedDate(startDate);
    var endDate = getFormattedDate(endDate);
    return [startDate, endDate];
}

function loading(startDate, endDate, choice) {
    var pd={"startDate":startDate, "endDate":endDate, "choice":choice};
    $.ajax({
        type:"POST",
        url:"/wholeBox",
	data: pd,
        success:function(msg){
            tableFirstData=msg['totalFirstList'];
            tableBasicData=msg['totalBasicList'];
	    var totalFirstFeas = msg['totalFirstFeas'];
    	    var totalBasicFeas = msg['totalBasicFeas'];
	    firstFeaTrigger(tableFirstData, totalFirstFeas);
	    basicFeaTrigger(tableBasicData, totalBasicFeas);
	    getErrTable(tableFirstData);
        }
    });
}

function firstFeaTrigger(tableFirstData, totalFirstFeas) {
    $('#tb_temp').dataTable({
	destroy:true,
    	"aaSorting": [[ 0, "desc" ], [4, "desc"], [2, "desc"]],
    	data:tableFirstData
    });
    $("#tb_temp").unbind();
    $('#tb_temp').on( 'click', "tr", function (e) {
	var filmName = $(e.target).parent().children(":eq(1)").html();
	var feaList = totalFirstFeas[filmName];
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

function basicFeaTrigger(tableBasicData, totalBasicFeas) {
    $('#basic_temp').dataTable({
	destroy:true,
    	"aaSorting": [[ 0, "desc" ], [3, "desc"], [2, "desc"]],
    	data:tableBasicData
    });
    $("#basic_temp").unbind();
    $('#basic_temp').on('click', "tr", function (e) {
	var filmName = $(e.target).parent().children(":eq(1)").html();
	var feaList = totalBasicFeas[filmName];
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

function isDataValid(preA, preB, preShuneng, real) {
    var invalidList = ['-', '--', '——'];
    if (invalidList.indexOf(preA) != -1 || invalidList.indexOf(preB) != -1 || invalidList.indexOf(preShuneng) != -1 || invalidList.indexOf(real) != -1) {
	return false;
    } else {
	return true;
    }
}

function getErrTable(tableFirstData) {
    var baiduErrA = 0.0;
    var baiduErrB = 0.0;
    var shunengErr = 0.0;
    var errSize = 0;
    for (var i = 0; i < tableFirstData.length; i++) {
	var onDate = Date.parse(new Date(tableFirstData[i][0].replace(/-/g, "/")));
	var today = new Date();
	var delta = today.getTime() - onDate;
	var days = Math.floor(delta/(24*3600*1000));
	if (days <= 14 && isDataValid(tableFirstData[i][2], tableFirstData[i][3], tableFirstData[i][4], tableFirstData[i][5])) {
	    baiduErrA += Math.abs(parseFloat(tableFirstData[i][2]) - parseFloat(tableFirstData[i][5])) / parseFloat(tableFirstData[i][5]);
	    baiduErrB += Math.abs(parseFloat(tableFirstData[i][3]) - parseFloat(tableFirstData[i][5])) / parseFloat(tableFirstData[i][5]);
	    shunengErr += Math.abs(parseFloat(tableFirstData[i][4]) - parseFloat(tableFirstData[i][5])) / parseFloat(tableFirstData[i][5]);
	    errSize += 1;
	}
    }
    if (errSize > 0) {
	baiduErrA = (baiduErrA / errSize).toFixed(4);
	baiduErrB = (baiduErrB / errSize).toFixed(4);
	shunengErr = (shunengErr / errSize).toFixed(4);
    } else {
	baiduErrA = '--';
	baiduErrB = '--';
	shunengErr = '--';
    }
    var tableHtml = '<tr><th>误差类别</th><th>百度预测A</th><th>百度预测B</th><th>数能预测</th></tr>';
    tableHtml += '<tr><td>总票房误差(近两周)</td><td>' + baiduErrA + '</td><td>' + baiduErrB + '</td><td>' + shunengErr + '</td></tr>';
    $('#errTable').html(tableHtml);
}
