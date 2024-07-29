var myChart2 = echarts.init(document.getElementById('main2'));

$.ajax({
type: "post",
async: "true",
url: "/data3",
dataType: "json",
success: function (data) {
        var option = {
            title: {
                text: '服务星级占比情况',
                left: 'center',
                top: '0%',
                textStyle: {
                    color: '#ffffff'
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: '{b} : {c} ({d}%)'
            },
            legend: {
                left: 'right',
                top: 'middle',
                orient: 'vertical',
                textStyle: {
                    color: '#ffffff'
                }
            },
            series: [
                {
                    type: 'pie',
                    radius: ['40%', '70%'],
                    center: ['50%', '60%'],
                    label: {
                        show: false,
                        position: 'center',
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: '20',
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },

                    data: data
                }
            ]
        };

        // 自动轮播配置
        var currentIndex = -1;
        var timer;

        function startCarousel() {
            timer = setInterval(function () {
                var dataLength = data.length;
                // 取消上一个数据的高亮显示
                myChart2.dispatchAction({
                    type: 'downplay',
                    seriesIndex: 0,
                    dataIndex: currentIndex
                });
                currentIndex = (currentIndex + 1) % dataLength;
                // 高亮显示当前数据
                myChart2.dispatchAction({
                    type: 'highlight',
                    seriesIndex: 0,
                    dataIndex: currentIndex
                });
            }, 2000);
        }

        // 鼠标悬浮事件处理
        myChart2.on('mouseover', function (params) {
            clearInterval(timer);
            currentIndex = params.dataIndex;
        });

        myChart2.on('mouseout', function (params) {
            startCarousel();
        });

        // 加载图表
        myChart2.setOption(option);
        startCarousel();
    }
});