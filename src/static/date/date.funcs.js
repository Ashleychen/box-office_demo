function appendZero(s) {
    return ("00"+ s).substr((s+"").length);
}

function getFormattedDate(curDate) {
    return curDate.getFullYear() + "-" + appendZero(curDate.getMonth() + 1) + "-" + appendZero(curDate.getDate());
}

function getDateByDelta(delta) {
    var newDate = new Date();
    newDate.setDate(newDate.getDate() + delta);
    newDate = getFormattedDate(newDate);
    return newDate;
}

function getDateByDeltaAndDate(theDate, delta) {
    var newDate = getDateFromStr(theDate);
    newDate.setDate(newDate.getDate() + delta);
    newDate = getFormattedDate(newDate);
    return newDate;
}

function getTimeDeltaDays(fromDate) {
    var fromDateTime = Date.parse(new Date(fromDate.replace(/-/g, "/")));
    var today = new Date();
    var delta = today.getTime() - fromDateTime;
    var days = Math.floor(delta/(24*3600*1000));
    return days;
}

function getTimeDeltaDaysByDate(fromDate, toDate) {
    var fromDateTime = Date.parse(new Date(fromDate.replace(/-/g, "/")));
    var toDateTime = Date.parse(new Date(toDate.replace(/-/g, "/")));
    var delta = toDateTime - fromDateTime;
    var days = Math.floor(delta/(24*3600*1000));
    return days;
}

function getDateFromStr(dateStr) {
    var newDate = Date.parse(new Date(dateStr.replace(/-/g, "/")));
    newDate = new Date(newDate);
    return newDate;
}

function getWeekRange(startDate) {
    var endDate = new Date(Date.parse(startDate));
    endDate.setDate(endDate.getDate() + 6);
    var endDateStr = getFormattedDate(endDate);
    $('#endDate').html('~' + endDateStr);
    return startDate + '~' + endDateStr;
}

function compDate(minDate, curDate, maxDate) {
    if (curDate <= minDate) {
        $("#pre_d").attr("class","pre_gray_d" );
        $("#aft_d").attr("class","aft_d" );
    }
    if (curDate >= maxDate) {
        $("#pre_d").attr("class","pre_d" );
        $("#aft_d").attr("class","aft_gray_d" );
    }
    if (curDate > minDate && curDate < maxDate) {
        $("#pre_d").attr("class","pre_d" );
        $("#aft_d").attr("class","aft_d" );
    }
}

function getCurrentWeekRange(curDateStr) {
    var curDate = getDateFromStr(curDateStr);
    var curWeekDay = curDate.getDay();
    if (curWeekDay != 0) {
        var endDate = getDateByDeltaAndDate(curDateStr, (7 - curWeekDay));
    } else {
	var endDate = getDateByDeltaAndDate(curDateStr, 0);
    }
    var startDate = getDateByDeltaAndDate(endDate, -6);
    return startDate + '~' + endDate;
}
