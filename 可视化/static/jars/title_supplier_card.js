var myChart8 = echarts.init(document.getElementById('main3'));

$.ajax({
    type: "post",
    async: "true",
    url: "/data8",
    dataType: "json",
    success: function (data) {
        var option = {
            title:[
                {
                    text: data[0],
                    x: '16%',
                    y: '10%',
                    textStyle: {
                        fontSize: 20,
                        color: 'rgb(101,171,190)'
                    }
                },
                {
                    text: '旅游项目总数',
                    x: '12%',
                    y: '24%',
                    textStyle: {
                        color: 'rgb(101,171,190)'
                    }
                },
                {
                    text: data[1],
                    x: '73%',
                    y: '10%',
                    textStyle: {
                        fontSize: 20,
                        color: 'rgb(101,171,190)'
                    }
                },
                {
                    text: '供应商总数',
                    x: '70%',
                    y: '24%',
                    textStyle: {
                        color: 'rgb(101,171,190)'
                    }
                }
            ]
        };
        myChart8.setOption(option)
    }
});
