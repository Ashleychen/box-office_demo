var error_date = $('#forcast').val();
function launch(t, e) {
    $('#movieWrapper').show();
    $('#dayWrapper').hide();
    $('#trend_seq_list').show();
    var filmName = $(t).parent().children(":eq(0)").html();
    var movieOption = {
        title: {
            text: "单部电影排片率趋势图"
        },
    	tooltip: {},
        legend: {
            data:['排片率']
        },
        xAxis: {
            name:'日期',
	    type:'category',
	    axisLabel:{
		interval:0,
		rotate:-20,
	    },
            data: []
            },
        yAxis: {},
        series: [
            {
                name: '排片率',
                type: 'line',
                data: []
            },
        ]
    };
    $.ajax({
        type:"GET",
        data:{'filmName':filmName},
        url:"/seqTrend",
        success:function(msg){
            movieOption.xAxis.data = msg['dateList'];
            movieOption.series[0].data = msg['seqRate'];
            movieChart.setOption(movieOption, true);
            movie_trend_list(msg['dateList'], msg['seqRate'], filmName);
        }
    });
}
function movie_trend_list(date_list, seq_list, filmName) {
    var html_str = "";
    var list_len = date_list.length;
    var max_len = Math.min(10, list_len);
    for (var i = list_len - max_len; i < list_len; i++) {
        var date_str = "<td>" + date_list[i] + "</td>";
        var seq_str = "<td>" + seq_list[i] + "</td>";
        html_str += "<tr>" + date_str + seq_str + "</tr>";
    }
    $('#seq_div').html(filmName);
    $('#trend_seq_table').html(html_str);
}
