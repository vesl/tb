function showPlotFinance(plot){
    plotTitle('finance '+plot)
    initPlotSkeleton()
    switch(plot){
        case 'ohlc':
            var submitFunction = function(){plotFinanceOhlc()}
    }
    $('#button-plot').click(submitFunction)
}

function plotFinanceOhlc(){
    $('#plot').html(loading())
    values = getFormValues()
    if (values == false) { return false}
    $.get('/api/plotter/finance/ohlc/'+values['timescale']+'/'+values['from']+'/'+values['to'],function(data){
        $('#plot').empty()
        const chart = LightweightCharts.createChart(document.getElementById('plot'));
        const candlestickSeries = chart.addCandlestickSeries();
        var data = JSON.parse(data)
        candlestickSeries.setData(data)
    })
}