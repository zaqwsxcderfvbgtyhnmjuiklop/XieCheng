var myChart5 = echarts.init(document.getElementById('main6'));
$.ajax({
type: "post",
async: "true",
url: "/data4",
dataType: "json",
success: function (data) {
    var option = {
        grid: {
            left: '20%',
            top: '35%',
        },
        textStyle: {
            color: '#ffffff'
        },
        title: {
            text: '价格与销售之间的关系',
            left: 'center',
            top: '0%',
            textStyle: {
                color: '#ffffff'
            }
        },
        xAxis: {
            max: 25000,
            name: '价格',
            nameLocation: 'center',  //居中显示
            nameGap: 35  //与轴的距离
        },
        yAxis: {
            max: 25000,
            name: '销售',
            nameLocation: 'center',  //居中显示
            nameGap: 50  //与轴的距离
        },
        series: {
            data: data,
            symbolSize: function (data) {  //使用function函数将data数据作为参数
                return data[2];  //获取data数据中的第三个数据,气泡大小
            },
            type: 'scatter'
        }
    };
    myChart5.setOption(option)
    }
});