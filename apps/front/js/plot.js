var charts = {}

function showPlotsFinance(){
    initPlotForm(function(){
        initPlotIndicatorsForm()
        initPlotDiv()
        $('#button-plot').click(function(){requestFinancePlotData()})
    })
    $('#content-title').html('Finance plots')
}

function getFormPlotValues(){
    var values = {}
    values['from'] = $('#datepicker-from').val()
    values['to'] = $('#datepicker-to').val()
    values['timescale'] = $('#timescale').val()
    if(values['from'] == undefined || values['to'] == undefined || values['timescale'] == 'Timescale'){
        alert('Fill the form')
        return false
    }
    else return values
}

function getFormIndicators(){
    let checkedIndicators = []
    for(const indicator in indicators){
        if ($('#checkbox-indicator-'+indicator).is(':checked') === true) { checkedIndicators.push(indicator)}
    }
    return checkedIndicators
}

function requestFinancePlotData(){
    const values = getFormPlotValues()
    const checkedIndicators = getFormIndicators()
    if (values === false) return false
    initPlotLoading()
    $.get('/api/plotter/finance/candles/'+values['timescale']+'/'+values['from']+'/'+values['to'],function(data){
        $('#plot').empty()
        charts['price'] = LightweightCharts.createChart(document.getElementById('plot'));
        const candlesSeries = charts['price'].addCandlestickSeries()
        candlesSeries.setData(JSON.parse(data))
        checkedIndicators.forEach(function(indicator){
            indicators[indicator](values)
        })
    })
}

function plotFinanceVolume(values){
    $.get('/api/plotter/finance/volume/'+values['timescale']+'/'+values['from']+'/'+values['to'],function(data){
        const volumeSeries = charts['price'].addHistogramSeries({
            color: '#aeaeae',
            lineWidth: 2,
            priceFormat: {type: 'volume'},
            overlay: true,
            scaleMargins: {
                top: 0.8,
                bottom: 0,
            }
        })
        volumeSeries.setData(JSON.parse(data))
    })
}