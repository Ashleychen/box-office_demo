$(document).ready(function(){
    movieChart = echarts.init(document.getElementById('movieMain'));
    dayChart = echarts.init(document.getElementById('dayMain'));
    var pd={"today":'default'};
    $.ajax({
	type: 'POST',
	url: "/screening",
	//async: false,
	data: pd,
	success:function(msg){
	    maxDate = msg['maxDate'];
	    minDate = msg['minDate'];
	    $("#screening" ).datepicker({
                "option":$.datepicker.regional[ "zh-cn" ],
                dateFormat:"yy-mm-dd",
                maxDate: maxDate,
                minDate: minDate,
                changeMonth:true,
            });
            var d = new Date(Date.parse($('#screening').val()));
            var curRew = rewriteDateStr(d);
            get_seq(curRew);
            comp_date(minDate, curRew, maxDate);
            $("#screening").change(function(){
                var changeDate = $("#screening").val();
                var d = new Date(Date.parse(changeDate));
                var changeStr = rewriteDateStr(d);
                get_seq(changeStr);
                comp_date(minDate, changeDate, maxDate);
            });

            $(".choose_forcast_d").on("click",".pre_d",function(){
                var curDate=$("#screening").val();
                if(curDate===''){
                    var preDate = get_datetime('','-1');
                }else{
                    var preDate = get_datetime(curDate,'-1');
                }
                get_seq(preDate);
                comp_date(minDate, preDate, maxDate);
            });

            $(".choose_forcast_d").on("click",".aft_d",function(){
                var curDate=$("#screening").val();
                if(curDate===''){
                    var nextDate = get_datetime('','1');
                }else{
                    var nextDate = get_datetime(curDate,'1');
                }
                get_seq(nextDate);
                comp_date(minDate, nextDate, maxDate);
            });
	}
    });
});
function get_seq(date){	
    var url="/screening";
    var pd={"today":date};
    $.ajax({
        type: "POST",
        url: url,
        data: pd,
        success:function(msg){
	    displayScreening(msg);
	    displayDayChart(msg);
        }
    }); 
}
