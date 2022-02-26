function showPlotFinance(plot){
    plotTitle('finance '+plot)
    initPlotSkeleton()
    switch(plot){
        case 'price':
            var submitFunction = function(){plotFinancePrice()}
    }
    $('#button-plot').click(submitFunction)
}

function plotFinancePrice(){
    $('#plot').html(loading())
    values = getFormValues()
    if (values == false) { return false}
    $.get('/api/plotter/finance/price/'+values['timescale']+'/'+values['from']+'/'+values['to'],function(data){
        $('#plot').empty()
        const chart = LightweightCharts.createChart(document.getElementById('plot'));
        const volumeSeries = chart.addHistogramSeries({
            color: '#AEAEAE',
            lineWidth: 2,
            priceFormat: {type: 'volume'},
            overlay: true,
            scaleMargins: {
                top: 0.8,
                bottom: 0,
            }
        });
        const candlestickSeries = chart.addCandlestickSeries();
        var data = JSON.parse(data)
        candlestickSeries.setData(data)
        volumeData = []
        data.forEach(function(candle){
            volumeData.push({'time':candle['time'],'value':candle['volume']})
        })
        volumeSeries.setData(volumeData)
    })
}