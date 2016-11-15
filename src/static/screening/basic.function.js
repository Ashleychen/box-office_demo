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
	$("#aft_d").attr("class","aft_d" );
    }
    if (current_date >= max_date) {
	$("#pre_d").attr("class","pre_d" );
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
    $("#screening").val(preStr);
    return preStr;
}
