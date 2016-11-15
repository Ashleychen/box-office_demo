//特征弹窗表格
function feaStrToTable(headList, feaList) {
    var tableHtml = '<br/><div style="text-align: center"><table class="table" style="width:80%;margin:0px 0px 0px 10%;">';
    var thStr = '<tr>';
    for (var i = 0; i < headList.length; i++) {
        thStr += '<th>' + headList[i] + '</th>';
    }
    thStr += '</tr>';
    tableHtml += thStr;
    for (var i = 0; i < feaList.length; i++) {
        var trStr = '<tr>';
    	for (var j = 0; j < feaList[0].length; j++) {
            trStr += '<td>' + feaList[i][j] + '</td>';
	}
        trStr += '</tr>';
        tableHtml += trStr;
    }
    tableHtml += '</table></div>'
    return tableHtml;
}

function detailStrToTable(headList, multiList) {
    var tableHtml = '<br/><div style="text-align: center"><table class="table" style="width:80%;margin:0px 0px 0px 10%;">';
    var thStr = '<tr>';
    for (var i = 0; i < headList.length; i++) {
        thStr += '<th>' + headList[i] + '</th>';
    }
    thStr += '</tr>';
    tableHtml += thStr;
    for (var i = 0; i < multiList[0].length; i++) {
        var trStr = '<tr>';
        for (var j = 0; j < multiList.length; j++) {
            trStr += '<td>' + multiList[j][i] + '</td>';
        }
        trStr += '</tr>';
        tableHtml += trStr;
    }
    tableHtml += '</table></div>'
    return tableHtml;
}

//弹窗画图
function writePopChart(wrapperID, mainID) {
    var htmlStr = "<div id=" + wrapperID + "style='width:100%;height:100%;display:inline-block;vertical-align:middle;background-color:white;'><div id=" + mainID + "style='margin:auto;width:100%;height:100%;display:inline-block;'></div></div>";
    return htmlStr;
}

//特征弹窗事件
function popEvent(titleStr, contentStr, e) {
    layer.open({
        type: 1,
        title: titleStr,
        closeBtn: 0,
        area: ['600px', '360px'],
        shadeClose: true, //点击遮罩关闭
        content: '\<\div style="padding:20px;">'+ contentStr+'\<\/div>'
    });
    var top = e.clientY;
    document.querySelector(".layui-layer").style.top = top + "px";
}
