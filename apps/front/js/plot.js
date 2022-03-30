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

function showPlotsLabels(){
    initPlotForm(function(){
        initPlotDiv()
        $('#button-plot').click(function(){plotLabels()})
    })
    $('#content-title').html('Labels plots')
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
    const div = $('<div>')
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

function appendIndicatorChart(parent,name,values,next){
    $('#plot-title-'+parent).children('h3').append(' & '+name)
    $.get('/api/plotter/finance/'+name+'/'+values['timescale']+'/'+values['from']+'/'+values['to'],function(data){
        next(data)
    })
}

function plotFinanceCandles(){
    const values = getFormPlotValues()
    const checkedIndicators = getFormIndicators()
    if (values === false) return false
    $('#plot').empty()
    createIndicatorChart('candles',values,function(data){
        charts['candles'] = LightweightCharts.createChart(document.getElementById('plot-candles'),{height:400})
        const candlesSeries = charts['candles'].addCandlestickSeries()
        candlesSeries.setData(JSON.parse(data))
        checkedIndicators.forEach(function(indicator){
            indicators[indicator](values)
        })
    })
}

function plotFinanceVolume(values){
    appendIndicatorChart('candles','volume',values,function(data){
        data = JSON.parse(data)
        renameKey(data,'volume','value')
        const volumeSeries = charts['candles'].addHistogramSeries({
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
        charts['rsi'] = LightweightCharts.createChart(document.getElementById('plot-rsi'),{height:200})
        const rsiSeries = charts['rsi'].addLineSeries({lineWidth:2})
        rsiSeries.setData(data)
    })
}

function plotFinanceMACD(values){
    createIndicatorChart('macd',values,function(data) {
        data=JSON.parse(data)
        renameKey(data,'macd','value')
        charts['macd'] = LightweightCharts.createChart(document.getElementById('plot-macd'),{height:200})
        const macdSeries = charts['macd'].addLineSeries({lineWidth:2})
        macdSeries.setData(data)
        appendIndicatorChart('macd','macdsignal',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'macdsignal','value')
            const macdsignalSeries = charts['macd'].addLineSeries({color:'#6C00B2',lineWidth:2})
            macdsignalSeries.setData(data)
        })
        appendIndicatorChart('macd','macdhist',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'macdhist','value')
            const macdhistSeries = charts['macd'].addHistogramSeries({
                color: '#aeaeae',
                lineWidth: 2,
                priceFormat: {type: 'volume'},
                overlay: true,
                scaleMargins: {
                    top: 0.8,
                    bottom: 0,
                }
            })
            macdhistSeries.setData(data)
        })
    })
}

function plotFinanceADX(values){
    createIndicatorChart('adx',values,function(data){
        data = JSON.parse(data)
        renameKey(data,'adx','value')
        charts['adx'] = LightweightCharts.createChart(document.getElementById('plot-adx'),{height:200})
        const adxSeries = charts['adx'].addLineSeries({color:'#F3003A',lineWidth:2})
        adxSeries.setData(data)
        appendIndicatorChart('adx','adxr',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'adxr','value')
            const adxrSeries = charts['adx'].addLineSeries({color:'#00F33A',lineWidth:2})
            adxrSeries.setData(data)
        })
    })
}
function plotFinanceAPO(values){
    createIndicatorChart('apo',values,function(data){
        data = JSON.parse(data)
        renameKey(data,'apo','value')
        charts['apo'] = LightweightCharts.createChart(document.getElementById('plot-apo'),{
            height:200,
        })
        const apoSeries = charts['apo'].addLineSeries({color:'#A53AFF',lineWidth:2})
        apoSeries.setData(data)
    })
}
function plotFinanceAroon(values){
    createIndicatorChart('aroondown',values,function(data){
        data = JSON.parse(data)
        renameKey(data,'aroondown','value')
        charts['aroon'] = LightweightCharts.createChart(document.getElementById('plot-aroondown'),{height:200})
        const aroondownSeries = charts['aroon'].addLineSeries({color:'#3AFFB4',lineWidth:2})
        aroondownSeries.setData(data)
        appendIndicatorChart('aroondown','aroonup',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'aroonup','value')
            const aroonupSeries = charts['aroon'].addLineSeries({color:'#015535',lineWidth:2})
            aroonupSeries.setData(data)
        })
        appendIndicatorChart('aroondown','aroonosc',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'aroonosc','value')
            const aroonoscSeries = charts['aroon'].addLineSeries({color:'#46554F',lineWidth:2})
            aroonoscSeries.setData(data)
        })
    })
}

function plotFinanceBOP(values){
    createIndicatorChart('bop',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'bop','value')
        charts['bop'] = LightweightCharts.createChart(document.getElementById('plot-bop'),{height:200})
        const bopSeries = charts['bop'].addLineSeries({color:'#F8FF13',lineWidth:2})
        bopSeries.setData(data)
    })
}
function plotFinanceCCI(values){
    createIndicatorChart('cci',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'cci','value')
        charts['cci'] = LightweightCharts.createChart(document.getElementById('plot-cci'),{height:200})
        const cciSeries = charts['cci'].addLineSeries({color:'#2B00B2',lineWidth:2})
        cciSeries.setData(data)
    })
}
function plotFinanceCMO(values){
    createIndicatorChart('cmo',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'cmo','value')
        charts['cmo'] = LightweightCharts.createChart(document.getElementById('plot-cmo'),{height:200})
        const cciSeries = charts['cmo'].addLineSeries({color:'#00B21B',lineWidth:2})
        cciSeries.setData(data)
    })
}
function plotFinanceDX(values){
    createIndicatorChart('dx',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'dx','value')
        charts['dx'] = LightweightCharts.createChart(document.getElementById('plot-dx'),{height:200})
        const cciSeries = charts['dx'].addLineSeries({color:'#B20031',lineWidth:2})
        cciSeries.setData(data)
    })
}
function plotFinanceMFI(values){
    createIndicatorChart('mfi',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'mfi','value')
        charts['mfi'] = LightweightCharts.createChart(document.getElementById('plot-mfi'),{height:200})
        const mfiSeries = charts['mfi'].addLineSeries({color:'#000DB2',lineWidth:2})
        mfiSeries.setData(data)
    })
}
function plotFinanceMinus(values){
    createIndicatorChart('minusdi',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'minusdi','value')
        charts['minus'] = LightweightCharts.createChart(document.getElementById('plot-minusdi'),{height:200})
        const minusdiSeries = charts['minus'].addLineSeries({color:'#FFBD00',lineWidth:2})
        minusdiSeries.setData(data)
        appendIndicatorChart('minusdi','minusdm',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'minusdm','value')
            const minusdmSeries = charts['minus'].addLineSeries({color:'#BF7701',lineWidth:2})
            minusdmSeries.setData(data)          
        })
    })
}
function plotFinanceMOM(values){
    createIndicatorChart('mom',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'mom','value')
        charts['mom'] = LightweightCharts.createChart(document.getElementById('plot-mom'),{height:200})
        const momSeries = charts['mom'].addLineSeries({color:'#9A01BF',lineWidth:2})
        momSeries.setData(data)
    })
}
function plotFinancePlus(values){
    createIndicatorChart('plusdi',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'plusdi','value')
        charts['plus'] = LightweightCharts.createChart(document.getElementById('plot-plusdi'),{height:200})
        const plusdiSeries = charts['plus'].addLineSeries({color:'#01BF2C',lineWidth:2})
        plusdiSeries.setData(data)
        appendIndicatorChart('plusdi','plusdm',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'plusdm','value')
            const plusdmSeries = charts['plus'].addLineSeries({color:'#ADFFBF',lineWidth:2})
            plusdmSeries.setData(data)
        })
    })
}
function plotFinancePPO(values){
    createIndicatorChart('ppo',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'ppo','value')
        charts['ppo'] = LightweightCharts.createChart(document.getElementById('plot-ppo'),{height:200})
        const ppoSeries = charts['ppo'].addLineSeries({color:'#ADC8FF',lineWidth:2})
        ppoSeries.setData(data)
    })
}
function plotFinanceROC(values){
    createIndicatorChart('roc',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'roc','value')
        charts['roc'] = LightweightCharts.createChart(document.getElementById('plot-roc'),{height:200})
        const rocSeries = charts['roc'].addLineSeries({color:'#6C5C64',lineWidth:2})
        rocSeries.setData(data)
        appendIndicatorChart('roc','rocp',values,function(data) {
           data = JSON.parse(data)
           renameKey(data,'rocp','value')
           const rocpSeries = charts['roc'].addLineSeries({color:'#34212B',lineWidth:2})
           rocpSeries.setData(data)
        })
        appendIndicatorChart('roc','rocr',values,function(data) {
           data = JSON.parse(data)
           renameKey(data,'rocr','value')
           const rocrSeries = charts['roc'].addLineSeries({color:'#76214D',lineWidth:2})
           rocrSeries.setData(data)
        })
    })
}
function plotFinanceStoch(values){
    createIndicatorChart('slowk',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'slowk','value')
        charts['stoch'] = LightweightCharts.createChart(document.getElementById('plot-slowk'),{height:200})
        const slowkSeries = charts['stoch'].addLineSeries({color:'#AB5966',lineWidth:2})
        slowkSeries.setData(data)
        appendIndicatorChart('slowk','slowd',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'slowd','value')
            const slowdSeries = charts['stoch'].addLineSeries({color:'#A659AB',lineWidth:2})
            slowdSeries.setData(data)
        })
        appendIndicatorChart('slowk','fastk',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'fastk','value')
            const slowdSeries = charts['stoch'].addLineSeries({color:'#5966AB',lineWidth:2})
            slowdSeries.setData(data)
        })
        appendIndicatorChart('slowk','fastd',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'fastd','value')
            const slowdSeries = charts['stoch'].addLineSeries({color:'#59AB6E',lineWidth:2})
            slowdSeries.setData(data)
        })
        appendIndicatorChart('slowk','fastkrsi',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'fastkrsi','value')
            const slowdSeries = charts['stoch'].addLineSeries({color:'#ABAB59',lineWidth:2})
            slowdSeries.setData(data)
        })
        appendIndicatorChart('slowk','fastdrsi',values,function(data) {
            data = JSON.parse(data)
            renameKey(data,'fastdrsi','value')
            const slowdSeries = charts['stoch'].addLineSeries({color:'#AB6E59',lineWidth:2})
            slowdSeries.setData(data)
        })
    })
}
function plotFinanceUltosc(values){
    createIndicatorChart('ultosc',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'ultosc','value')
        charts['ultosc'] = LightweightCharts.createChart(document.getElementById('plot-ultosc'),{height:200})
        const ultoscSeries = charts['ultosc'].addLineSeries({color:'#07F9DB',lineWidth:2})
        ultoscSeries.setData(data)
    })
}
function plotFinanceWillr(values){
    createIndicatorChart('willr',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'willr','value')
        charts['willr'] = LightweightCharts.createChart(document.getElementById('plot-willr'),{height:200})
        const willrSeries = charts['willr'].addLineSeries({color:'#3AF907',lineWidth:2})
        willrSeries.setData(data)
    })
}

function plotFinanceIchimoku(values){
    appendIndicatorChart('candles','ichtenkan',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'ichtenkan','value')
        const ichtenkanSeries = charts['candles'].addLineSeries({color:'#FF7070',lineWidth:1})
        ichtenkanSeries.setData(data)
    })
    appendIndicatorChart('candles','ichkijun',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'ichkijun','value')
        const ichkijunSeries = charts['candles'].addLineSeries({color:'#7081FF',lineWidth:1})
        ichkijunSeries.setData(data)
    })
    appendIndicatorChart('candles','ichssa',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'ichssa','value')
        const ichssaSeries = charts['candles'].addLineSeries({color:'#DA70FF',lineWidth:1})
        ichssaSeries.setData(data)
    })
    appendIndicatorChart('candles','ichssb',values,function(data) {
        data = JSON.parse(data)
        renameKey(data,'ichssb','value')
        const ichssbSeries = charts['candles'].addLineSeries({color:'#C2FF70',lineWidth:1})
        ichssbSeries.setData(data)
    })
}

function createPlotImg(name,uri,values){
    const title = $('<span>')
    const div = $('<div>')
    const img = $('<img>')
    title.html('<h3>'+name+'</h3>')
    title.attr('id','plot-title-'+name)
    div.attr('id','plot-'+name)
    $('#plot').append(title)
    $('#plot').append(div)
    img.attr('src','/api/plotter/'+uri+'/'+values['timescale']+'/'+values['from']+'/'+values['to']+'/'+name+'.png')
    div.html(img)
}

function plotLabels(){
    const values = getFormPlotValues()
    $('#plot').empty()
    createPlotImg('cusum','labels/filters/cusum',values)
}