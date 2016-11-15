function numToTdHtmlByPrecision(numStr, precision) {
   var numStr = getFloatStrByPrecision(numStr, precision);
   var htmlStr = "<td>" + numStr + "</td>";
   return htmlStr;
}

function getFloatStrByPrecision(floatStr, precision) {
    if (floatStr != '-' && floatStr != '--' && Math.abs(parseFloat(floatStr) + 1.0) > 1e-6) {
    	var newStr = parseFloat(floatStr).toFixed(precision)
    } else {
	var newStr = '--';
    }
    return newStr;
}

function trimFloatList(floatList, precision) {
    trimmedFloatList = new Array();
    for (var i = 0; i < floatList.length; i++) {
	var floatStr = getFloatStrByPrecision(floatList[i], precision);
        trimmedFloatList.push(floatStr);
    }
    return trimmedFloatList;
}

//main的误差表格
function ErrorListToHtml(lineCate, errorList, lineCount, lineSize) {
    var html_str = "";
    for (var i = 0; i < lineCount; i++) {
        var line_str = "<tr>";
        line_str += '<td style="color:#2fa4e7">' + lineCate[i] + '</td>'
        for (var j = 0; j < lineSize; j++) {
	    var td_str = numToTdHtmlByPrecision(errorList[i * lineSize + j], 4);
            line_str += td_str;
        }
        line_str += "</tr>";
        html_str += line_str;
    }
    return html_str;
}

function getErrByCheckingSize(err, errSize) {
    if (errSize != 0) {
        err = (err / errSize).toFixed(4);
    } else {
        err = '--';
    }
    return err;
}

function isDataValid(dateStr) {
    var invalidList = ['-', '--', '——'];
    if (invalidList.indexOf(dataStr) != -1) {
        return false;
    } else {
        return true;
    }
}

function getErrList(preList, realList) {
    var errList = new Array();
    for (var i = 0; i < preList.length; i++) {
        if (Math.abs(parseFloat(realList[i]) - 0.0) < 1e-6 || preList[i] == '--') {
            errList.push('--');
        } else {
            var err = (Math.abs(parseFloat(preList[i]) - parseFloat(realList[i])) / parseFloat(realList[i])).toFixed(4);
            errList.push(err);
        }
    }
    return errList;
}

function getErrByTop(topErrList, baiduErrList, shunengErrList, limitNum) {
    var bound = Math.min(baiduErrList.length, limitNum);
    for (var i = 0; i < bound; i++) {
        if (shunengErrList[i] == '--' || baiduErrList[i] == '--') {
            continue;
        }
        topErrList[0] += parseFloat(baiduErrList[i]);
        topErrList[2] += 1;
        topErrList[1] += parseFloat(shunengErrList[i]);
        topErrList[3] += 1;
    }
    return topErrList;
}
