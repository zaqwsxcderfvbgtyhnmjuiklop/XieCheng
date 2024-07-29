var myChart = echarts.init(document.getElementById('main'));
$.ajax({
type: "post",
async: "true",
url: "/data2",
dataType: "json",
success: function (data) {
    var option = {
        title: {
            text: '旅游热度地图',
            left: 'center',
            textStyle: {
                color: '#ffffff'
            }
        },
        visualMap: {
            type: 'piecewise',
            pieces: [
                { min: 500000, max: 1000000, label: '热度大于等于500000', color: '#071D33' },
                { min: 300000, max: 499999, label: '热度300000~499999', color: '#0D3A66' },
                { min: 200000, max: 299999, label: '热度200000~299999', color: '#145699' },
                { min: 100000, max: 199999, label: '热度100000~199999', color: '#1A73CC' },
                { min: 0, max: 99999, label: '热度小于100000', color: '#2190FF' }
            ],
            color: ['#E0022B', '#E09107', '#A3E00B'],
            textStyle: {
                color: '#ffffff' // 修改图例的字体颜色为红色
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '热度<br>{b}:{c}'
        },
        series: [
            {
                type: 'map',
                mapType: 'china',
                geoIndex: 0,
                data: data,
                label: {
                    show: true,
                    color: 'rgb(249, 249, 249)'
                }
            }
        ],
        geo: {
          map: "china",
          roam: true,
          zoom:1, //默认显示级别
          scaleLimit:{min:0,max:3}, // 缩放级别
          regions: [
            {
              name: "南海诸岛",
              value: 0,
              itemStyle: {
                normal: {
                  opacity: 0,
                  label: {
                    show: false
                  }
                }
              }
            }
          ]
        }
    };
    myChart.setOption(option)
    }
});