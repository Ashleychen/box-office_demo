var movieChart;
var dayChart;
function displayScreening(msg) {
    var firstDaySet = new Set(msg['firstDaySet']);
    var table_html = "";
    for(var i = 0; i < msg['curList'].length; i++) {
        if (firstDaySet.has(msg['curList'][i][1])) {
            var tr_str = "<tr class='first_day' style='background-color:#FFB5C5'>";
        } else {
            var tr_str = "<tr>";
        }
	var name_str = "<td id='nametd'><a id='namel' href='javascript:void(0);' onclick='launch(this, event)'>" +
	    msg['curList'][i][3] + "</a>" + "   " + "<a class='btn btn-default btn-xs' id='lbtn' href='http://www.cbooo.cn/m/" +
	    msg['curList'][i][1] + "'>详情</a></td>";
        var seq_str = "<td>" +  msg['curList'][i][4] + "</td>";
        table_html += tr_str + name_str + seq_str + "</tr>";
        }
    $('#seq_table').html(table_html);
}
function displayDayChart(msg) {
    var day_option = {
        title: {
            left:'center',
            top:'5%',
            text: "排片率趋势"
        },
	tooltip: {
	    trigger:'axis'
	},
        legend: {
            data:['当日排片率'],
            left:'right',
            top:'5%',
        },
        xAxis: {
            name:'电影名',
	    type:'category',
	    axisLabel:{
		interval:0,
	        rotate:-15,
	    },
            data: []
        },
        yAxis: {},
        series: [
            {
                name: '当日排片率',
                type: 'line',
                data: []
             },
        ]
    };
    var day_movies = new Array();
    var day_seqs = new Array();
    for (var i = 1; i < msg['curList'].length; i++) {
	day_movies.push(msg['curList'][i][3]);
	day_seqs.push(msg['curList'][i][4]);
    }
    $('#movieWrapper').hide();
    $('#trend_seq_list').hide();
    if (day_movies.length == 0) {
        $('#dayWrapper').hide();
    } else {
        $('#dayWrapper').show();
        day_option.xAxis.data = day_movies;
        day_option.series[0].data = day_seqs;
        dayChart.setOption(day_option, true);
    }
}
