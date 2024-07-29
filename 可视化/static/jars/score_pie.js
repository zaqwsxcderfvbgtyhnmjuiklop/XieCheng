var myChart3 = echarts.init(document.getElementById('main5'));

$.ajax({
type: "post",
async: "true",
url: "/data5",
dataType: "json",
success: function (data) {
        var option = {
            title: {
                text: '评分占比情况',
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
                left: 'left',
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
                myChart3.dispatchAction({
                    type: 'downplay',
                    seriesIndex: 0,
                    dataIndex: currentIndex
                });
                currentIndex = (currentIndex + 1) % dataLength;
                // 高亮显示当前数据
                myChart3.dispatchAction({
                    type: 'highlight',
                    seriesIndex: 0,
                    dataIndex: currentIndex
                });
            }, 2000);
        }

        // 鼠标悬浮事件处理
        myChart3.on('mouseover', function (params) {
            clearInterval(timer);
            currentIndex = params.dataIndex;
        });

        myChart3.on('mouseout', function (params) {
            startCarousel();
        });

        // 加载图表
        myChart3.setOption(option);
        startCarousel();
    }
});