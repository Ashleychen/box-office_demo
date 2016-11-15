function initDateRangePicker(pickerObj, pickerStartDate, pickerEndDate, changeFunc) {
    pickerObj.daterangepicker(
    {
        locale: {
        format: 'YYYY-MM-DD'
        },
        startDate: pickerStartDate,
        endDate: pickerEndDate,
        "autoApply": true,
    },
    function(start, end, label) {
        var firstDate = start.format('YYYY-MM-DD');
        var lastDate = end.format('YYYY-MM-DD');
        changeFunc(firstDate, lastDate);
    });
}

function initDatePicker(pickerObj, pickerStartDate, pickerEndDate, defaultDate, changeFunc) {
    pickerObj.datepicker({
	"option":$.datepicker.regional[ "zh-cn" ],
        dateFormat:"yy-mm-dd",
        maxDate: pickerEndDate,
        minDate: pickerStartDate,
        changeMonth:true,
    });
    pickerObj.datepicker('setDate', getDateFromStr(defaultDate));
    pickerObj.change(function(){
        var changeDate = pickerObj.val();
	changeFunc(pickerStartDate, pickerEndDate, changeDate);
    });
}
