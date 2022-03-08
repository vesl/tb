var charts = {}

function renameKey(data,o,n){
    for (const i in data) {
        data[i][n] = data[i][o];
        delete data[i][o];
    }
}

function showPlotsFinance(){
    initPlotForm(function(){
        initPlotIndicatorsForm()
        initPlotDiv()
        $('#button-plot').click(function(){plotFinanceCandles()})
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

function createIndicatorChart(name,values,next){
    const title = $('<span>')
    const div=$('<div>')
    title.html('<h3>'+name+'</h3>')
    title.attr('id','plot-title-'+name)
    div.attr('id','plot-'+name)
    $('#plot').append(title)
    $('#plot').append(div)
    initPlotLoading(div)
    $.get('/api/plotter/finance/'+name+'/'+values['timescale']+'/'+values['from']+'/'+values['to'],function(data){
        next(data)
        $('#plot-'+name).children('#loading').remove()
    })
}

function plotFinanceCandles(){
    const values = getFormPlotValues()
    const checkedIndicators = getFormIndicators()
    if (values === false) return false
    $('#plot').empty()
    createIndicatorChart('candles',values,function(data){
        charts['price'] = LightweightCharts.createChart(document.getElementById('plot-candles'),{
            height:400,
        });
        const candlesSeries = charts['price'].addCandlestickSeries()
        candlesSeries.setData(JSON.parse(data))
        checkedIndicators.forEach(function(indicator){
            indicators[indicator](values)
        })
    })
}

function plotFinanceVolume(values){
    createIndicatorChart('volume',values,function(data){
        $('#plot-volume').remove()
        $('#plot-title-volume').remove()
        data = JSON.parse(data)
        renameKey(data,'volume','value')
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
        volumeSeries.setData(data)
    })
}

function plotFinanceRSI(values){
    createIndicatorChart('rsi',values,function(data){
        data = JSON.parse(data)
        renameKey(data,'rsi','value')
        charts['rsi'] = LightweightCharts.createChart(document.getElementById('plot-rsi'),{
            height:200,
        });
        const rsiSeries = charts['rsi'].addLineSeries({lineWidth:2})
        rsiSeries.setData(data)
    })
}

function plotFinanceADX(values){
    createIndicatorChart('adx',values,function(data){
        data = JSON.parse(data)
        renameKey(data,'adx','value')
        charts['adx'] = LightweightCharts.createChart(document.getElementById('plot-adx'),{
            height:200,
        });
        const rsiSeries = charts['rsi'].addLineSeries({color:'#FF903A',lineWidth:2})
        rsiSeries.setData(data)
    })
}
function plotFinanceADXR(values){

}
function plotFinanceAPO(values){

}
function plotFinanceAroon(values){

}
function plotFinanceAroonosc(values){

}
function plotFinanceBOP(values){

}
function plotFinanceCCI(values){

}
function plotFinanceCMO(values){

}
function plotFinanceDX(values){

}
function plotFinanceMFI(values){

}
function plotFinanceMinusDI(values){

}
function plotFinanceMinusDM(values){

}
function plotFinanceMOM(values){

}
function plotFinancePlusDI(values){

}
function plotFinancePlusDM(values){

}
function plotFinancePPO(values){

}
function plotFinanceROC(values){

}
function plotFinanceROCP(values){

}
function plotFinanceROCR(values){

}
function plotFinanceROCR100(values){

}
function plotFinanceStoch(values){

}
function plotFinanceStochF(values){

}
function plotFinanceStochRSI(values){

}
function plotFinanceTrix(values){

}
function plotFinanceUltosc(values){

}
function plotFinanceWillr(values){

}