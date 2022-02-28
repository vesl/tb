function showPlotFinance(plot){
    plotTitle('finance '+plot)
    initPlotSkeleton()
    switch(plot){
        case 'ohlc':
            var submitFunction = function(){plotFinanceOhlc()}
            break
        case 'volume':
            var submitFunction = function(){plotFinanceVolume()}
            break
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

function plotFinanceVolume(){
    $('#plot').html(loading())
    values = getFormValues()
    if (values == false) { return false}
    $.get('/api/plotter/finance/volume/'+values['timescale']+'/'+values['from']+'/'+values['to'],function(data){
        $('#plot').empty()
        const chart = LightweightCharts.createChart(document.getElementById('plot'));
        const volumeSeries = chart.addHistogramSeries();
        var data = JSON.parse(data)
        volumeSeries.setData(data)
    })
}

function plotFinanceRsi(){
    $('#plot').html(loading())
    values = getFormValues()
    if (values == false) { return false}
    $.get('/api/plotter/finance/rsi/'+values['timescale']+'/'+values['from']+'/'+values['to'],function(data){
        $('#plot').empty()
        const chart = LightweightCharts.createChart(document.getElementById('plot'));
        const rsiSeries = chart.addLineSeries();
        var data = JSON.parse(data)
        rsiSeries.setData(data)
    })
}