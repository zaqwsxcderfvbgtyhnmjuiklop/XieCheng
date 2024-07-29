        var myChart6 = echarts.init(document.getElementById('main7'));
        $.ajax({
        type: "post",
        async: "true",
        url: "/data1",
        dataType: "json",
        success: function (data) {
            var option = {
                title: {
                    text: '标签词云图',
                    left: 'center',
                    top: '0%',
                    textStyle: {
                        color: '#ffffff'
                    }
                },
                tooltip: {
                    show: true
                },
                series: [
                    {
                        type: 'wordCloud',
                        gridSize: 1,  //词间距
                        shape: 'circle',  //词云形状
                        sizeRange: [9, 20],  //词云大小范围
                        width: 400,  //词云显示宽度
                        height: 190,  //词云显示高度
                        textStyle: {
                            normal: {
                                color: function () {  //随机拿取颜色
                                    return 'rgb(' + [
                                        Math.round(Math.random() * 160),
                                        Math.round(Math.random() * 160),
                                        Math.round(Math.random() * 160)
                                    ].join(',') + ')';
                                }
                            },
                            emphasis: {  //鼠标悬停触发
                                shadowBlur: 10,  //阴影的模糊等级
                                shadowColor: '#333'  //阴影颜色
                            }
                        },
                        data: data
                    }
                ]
            };
            myChart6.setOption(option)
            }
        });