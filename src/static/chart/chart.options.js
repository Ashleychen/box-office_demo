//当日误差柱状图
var dailyRangeOption = {
    title: {
    	left:'left',
        top:'5%',
        text: "当日误差"
    },
    tooltip: {
    	formatter:function(params) {
    	    var res = '当日误差:<br/>'+
            	params.name + ':' + rangeErrDict[params.name];
            return res;
        },
    },
    legend: {
        data:['当日误差'],
        left:'right',
        top:'5%',
    },
    xAxis: {
        name:'票房范围',
        data: []
    },
    yAxis: {
        max:0.5,
    },
    series: [
        {
            name: '当日误差',
            type: 'bar',
            barWidth:40,
            data: []
        },
    ]
};

//当日票房趋势折线图
var dapanTrendOption = {
    tooltip: {
        trigger: 'axis',
        position: function (pt) {
            return [pt[0], '10%'];
        }
    },
    title: {
        text: '大盘票房',
    },
    legend: {
        data:['预测票房A', '预测票房B', '真实票房']
    },
    toolbox: {
        show: true,
        feature: {
            dataView: {show: true, readOnly: false},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data:[]
    },
    yAxis: {
        type: 'value',
        boundaryGap: [0, '100%']
    },
    dataZoom: [{
        type: 'inside',
        start: 0,
        end: 30
    }, {
        start: 0,
        end: 30
    }],
    series: [
        {
            name:'预测票房A',
            type:'line',
            smooth:true,
            symbol: 'none',
            sampling: 'average',
            itemStyle: {
            	normal: {
                color: 'rgb(255, 70, 131)'
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgb(255, 158, 68)'
                    }, {
                    offset: 1,
                    color: 'rgb(255, 70, 131)'
                    }])
                }
            },
            data:[]
        },
        {
            name:'预测票房B',
            type:'line',
            smooth:true,
            symbol: 'none',
            sampling: 'average',
            itemStyle: {
                normal: {
                color: 'rgb(64, 102, 255)'
            	}
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgb(64, 230, 255)'
                    }, {
                    offset: 1,
                    color: 'rgb(64, 102, 255)'
                    }])
            	}
            },
            data:[]
        },
	{
            name:'真实票房',
            type:'line',
            smooth:true,
            symbol: 'none',
            sampling: 'average',
            itemStyle: {
                normal: {
                    color: 'rgb(0, 255, 127)'
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgb(189, 252, 201)'
                     }, {
                        offset: 1,
                        color: 'rgb(0, 255, 127)'
                     }])
                }
            },
            data:[]
        }
    ]
};

var singleTrendOption = {
    title: {
        text: "单部电影票房趋势图"
    },
    tooltip: {},
    legend: {
        data:['预测票房A', '预测票房B', '真实票房']
    },
    xAxis: {
        name:'日期',
        data: []
    },
    yAxis: {},
    series: [
        {
            name: '预测票房A',
            type: 'line',
            areaStyle: {normal: {}},
            data: [5, 20, 36, 10, 10, 20]
        },
        {
            name: '预测票房B',
            type: 'line',
            areaStyle: {normal: {}},
            data: [5, 20, 36, 10, 10, 20]
        },
        {
            name: '真实票房',
            type: 'line',
            areaStyle: {normal: {}},
            data: [5, 20, 36, 10, 10, 20]
        }
    ]
};

var aveOption = {
    tooltip: {
        trigger: 'axis',
        position: function (pt) {
            return [pt[0], '10%'];
        }
    },
    title: {
        text: "Moving Average"
    },
    legend: {
        data:['Win Times'],
    },
    toolbox: {
        show: true,
        feature: {
            dataView: {show: true, readOnly: false},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    xAxis: {
        name:'日期',
        boundaryGap: false,
        type:'category',
        data: []
    },
    yAxis: {
        type: 'value',
        boundaryGap: [0, '100%'],
        min: 0,
        max: 1
    },
    dataZoom: [{
        type: 'inside',
        start: 0,
        end: 30
        }, {
        start: 0,
        end: 30
    }],
    series: [
        {
            name: 'Win Times',
            type: 'line',
            smooth:true,
            symbol: 'none',
            sampling: 'average',
            itemStyle: {
                normal: {
                    color: 'rgb(255, 70, 131)'
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgb(255, 158, 68)'
                    }, {
                        offset: 1,
                        color: 'rgb(255, 70, 131)'
                    }])
                }
            },
            data: []
        },
    ]
};

var weekOption = {
    title: {
        left:'center',
        top:'5%',
        text: "周票房误差"
    },
    tooltip: {
        trigger:'axis'
    },
    legend: {
        data:['周票房'],
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
    yAxis: {
        type: 'value',
        name: '误差',
        axisLabel: {
            formatter: '{value} '
        }
    },
    series: [
        {
            name: '百度误差',
            type: 'bar',
            data: []
         },
        {
            name: '数能误差',
            type: 'bar',
            data: []
         },
    ]
};

var weekMvOption = {
    title: {
    },
    tooltip: {
        trigger:'axis'
    },
    legend: {
        data:['每日票房', '排片率'],
        left:'right',
        top:'5%',
    },
    xAxis: {
        type:'category',
        axisLabel:{
            interval:0,
            rotate:-15,
        },
        data: []
    },
    yAxis: [
        {
            type: 'value',
            name: '票房',
            axisLabel: {
                formatter: '{value} 万'
            }
        },
        {
            type: 'value',
            name: '排片率',
            axisLabel: {
                formatter: '{value} %'
            }
        },
    ],
    series: [
        {
            name: '每日票房',
            type: 'bar',
            barWidth:40,
            data: []
         },
        {
            name: '排片率',
            type: 'line',
            yAxisIndex: 1,
            data: []
         },
    ]
};

var firstDetailOption = {
    title: {
    },
    tooltip: {
        trigger:'axis'
    },
    legend: {
        data:['百度预测A', '百度预测B', '数能预测', '实时票房'],
        left:'right',
        top:'5%',
    },
    xAxis: {
        type:'category',
        axisLabel:{
            interval:0,
            rotate:-15,
        },
        data: []
    },
    yAxis: [
        {
            type: 'value',
            name: '票房',
            axisLabel: {
                formatter: '{value} 万'
            }
        },
    ],
    series: [
        {
            name: '百度预测A',
            type: 'line',
            data: []
         },
        {
            name: '百度预测B',
            type: 'line',
            data: []
         },
        {
            name: '数能预测',
            type: 'line',
            data: []
         },
        {
            name: '实时票房',
            type: 'line',
            data: []
         },
    ]
};
