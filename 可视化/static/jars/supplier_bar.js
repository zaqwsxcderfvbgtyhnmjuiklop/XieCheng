var myChart4 = echarts.init(document.getElementById('main4'));

$.ajax({
type: "post",
async: "true",
url: "/data6",
dataType: "json",
success: function (data) {
        var option = {
            grid: {
                left: '20%',
            },
            title: {
                text: '旅游项目最多的10个供应商',
                left: 'center',
                top: '0%',
                textStyle: {
                    color: '#ffffff'
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                }
            },
            xAxis: {
                data: data[0],
                axisLabel: {
                    interval: 0,
                    rotate: 45
                }
            },
            yAxis: {},
            textStyle: {
                color: '#ffffff'
            },
            series: [{
                name: '统计项目',
                type: 'bar',
                data: data[1]
            }]
        };
        myChart4.setOption(option);
    }
});