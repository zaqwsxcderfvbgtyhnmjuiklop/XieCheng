var myChart7 = echarts.init(document.getElementById('main8'));

$.ajax({
type: "post",
async: "true",
url: "/data7",
dataType: "json",
success: function (data) {
        var option = {
            grid: {
                left: '20%',
                top: '10%'
            },
            title: {
                text: '销量最高的前10个旅游项目',
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
                    interval: 0, // 强制显示所有标签
                    rotate: 35,
                    textStyle: {
                        fontSize: 8
                    }
                }
            },
            yAxis: {
                axisLabel: {
                    textStyle: {
                        fontSize: 10
                    }
                }
            },
            textStyle: {
                color: '#ffffff'
            },
            series: [{
                name: '销量',
                type: 'bar',
                data: data[1]
            }]
        };
        myChart7.setOption(option);
    }
});