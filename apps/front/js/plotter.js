var plotterDatasetTechFeaturesMap = "";
var plotterDatasetIchimokuFeaturesMap = "";
var plotterModelTechMap = [];
var plotterBacktestMap = [];

function plotterGetDatasetTechFeaturesMap(then){
    $.get('/api/plotter/dataset/tech/features/map',(featuresMapJson)=>{
        plotterDatasetTechFeaturesMap = JSON.parse(featuresMapJson)
        then(plotterDatasetTechFeaturesMap)
    })
}

function plotterGetDatasetIchimokuFeaturesMap(then){
    $.get('/api/plotter/dataset/ichimoku/features/map',(featuresMapJson)=>{
        plotterDatasetIchimokuFeaturesMap = JSON.parse(featuresMapJson)
        then(plotterDatasetIchimokuFeaturesMap)
    })
}

function plotterLineLcChart(node,data){
    var plot = LightweightCharts.createChart(document.getElementById(node[0].id),{height:200})
    let series = plot.addLineSeries({color:'#'+((1 << 24) * Math.random() | 0).toString(16).padStart(6, "0")})
    series.setData(data)
}

function plotterOhlcLcChart(node,data,close_trades){
    var plot = LightweightCharts.createChart(document.getElementById(node[0].id),{height:300})
    let series = plot.addCandlestickSeries()
    let markers = []
    for (const [time,trade] of Object.entries(close_trades)){
		markers.push({
			time: Date.parse(trade.buy_time)/1000,
			position: 'belowBar',
			color: '#2196F3',
			shape: 'arrowUp',
			text: 'Buy @ ' + trade.buy_time,
		});
        markers.push({
			time: Date.parse(trade.sell_time)/1000,
			position: 'aboveBar',
			color: '#e91e63',
			shape: 'arrowDown',
			text: 'Sell @ ' + trade.buy_time,
		});
    }
    series.setData(data)
    series.setMarkers(markers);
}

function plotterGetDatasetTechFeatureData(dataset,feature){
    let featureData = []
    regex_feature_name = new RegExp('^'+feature+'\-')
    feature_fmt_name = Object.keys(dataset[0]).find(value => regex_feature_name.test(value))
    for (const i in dataset) {
        featureData.push({'time':dataset[i]['time'],'value':dataset[i][feature_fmt_name]})
    }
    return featureData
}

function plotterGetDatasetIchimokuFeatureData(dataset,feature){
    let featureData = []
    regex_feature_name = new RegExp('^'+feature+'\-')
    feature_fmt_name = Object.keys(dataset[0]).find(value => regex_feature_name.test(value))
    for (const i in dataset) {
        featureData.push({'time':dataset[i]['time'],'value':dataset[i][feature_fmt_name]})
    }
    return featureData
}

function plotterPlotToggle(name,next){
    var dpValues = getDpValues()
    var container = $('<div id="plot-'+name+'">')
    if($('#'+container[0].id).length == 0 && dpValues) {
        contentHTML(container)
        contentShowLoading(container)
        next(dpValues,container)
    } 
    else $('#'+container[0].id).remove()
}

function plotterDatasetTech(){
    contentTitle('Dataset - Tech')
    plotterGetDatasetTechFeaturesMap((featuresMap)=>{
        contentCollapse('Features list',JSON.stringify(featuresMap,null,2))
        contentDatePicker()
        contentButton('Plot features',()=>{plotterPlotToggle('features',plotterPlotDatasetTechFeatures)})
    })
}

function plotterDatasetIchimoku(){
    contentTitle('Dataset - Ichimoku')
    plotterGetDatasetIchimokuFeaturesMap((featuresMap)=>{
        contentCollapse('Features list',JSON.stringify(featuresMap,null,2))
        contentDatePicker()
        contentButton('Plot features',()=>{plotterPlotToggle('features',plotterPlotDatasetIchimokuFeatures)})
    })
}

function plotterLabels(){
    contentTitle('Labels')
    contentDatePicker()
    contentButton('Plot cusum',()=>{plotterPlotToggle('cusum',plotterPlotLabelsCusum)})
    contentButton('Plot TBM',()=>{plotterPlotToggle('tbm',plotterPlotLabelsTbm)})
    contentButton('Plot balance',()=>{plotterPlotToggle('balance',plotterPlotLabelsBalance)})
}

function plotterPlotDatasetTechFeatures(dpValues,container){
    var featuresList = Object.getOwnPropertyNames(plotterDatasetTechFeaturesMap)
    $.get('/api/plotter/dataset/tech/features/'+dpValues.symbol+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(dataset)=>{
        contentRemoveLoading(container)
        featuresList.forEach((feature)=>{
            let props = plotterDatasetTechFeaturesMap[feature]
            let featureContainer = $('<div id="plot-'+feature+'">')
            let featureData = plotterGetDatasetTechFeatureData(JSON.parse(dataset),feature)
            container.append('<h6><b>'+feature.toUpperCase()+'</b> source: <b>'+props['source']+'</b> scaled: <b>'+props['scaled']+'</b></h6>')
            container.append(featureContainer)
            plotterLineLcChart(featureContainer,featureData)
        })
    })
}

function plotterPlotDatasetIchimokuFeatures(dpValues,container){
    var featuresList = Object.getOwnPropertyNames(plotterDatasetIchimokuFeaturesMap)
    $.get('/api/plotter/dataset/ichimoku/features/'+dpValues.symbol+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(dataset)=>{
        contentRemoveLoading(container)
        featuresList.forEach((feature)=>{
            let props = plotterDatasetIchimokuFeaturesMap[feature]
            let featureContainer = $('<div id="plot-'+feature+'">')
            let featureData = plotterGetDatasetIchimokuFeatureData(JSON.parse(dataset),feature)
            container.append('<h6><b>'+feature.toUpperCase()+'</b> source: <b>'+props['source']+'</b> scaled: <b>'+props['scaled']+'</b></h6>')
            container.append(featureContainer)
            plotterLineLcChart(featureContainer,featureData)
        })
    })
}

function plotterPlotTrades(dpValues,wallet_stable,open_trades,close_trades,container){
    var featureList = ['open','high','low','close']
    $.get('/api/plotter/dataset/tech/ohlc/'+dpValues.symbol+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(dataset)=>{
        contentRemoveLoading(container)
        // Plot trades
        let ohlcContainer = $('<div id="plot-trades-ohlc">')
        container.append('<h6>Trades plot</h6>')
        container.append(ohlcContainer)
        dataset = JSON.parse(dataset)
        plotterOhlcLcChart(ohlcContainer,dataset,close_trades)
        // Plot Wallet
        container.append('<h6>Wallet plot</h6>')
        let walletContainer = $('<div id="plot-wallet">')
        container.append(walletContainer)
        wallet_dataset = []
        for (const [time,trade] of Object.entries(close_trades)){
            wallet_stable+=(trade.offer-trade.bid)
            wallet_dataset.push({'time':Date.parse(time)/1000,'value':wallet_stable})
        }
        wallet_dataset.sort(function(a,b){
            var x = a['time']; var y = b['time'];
            return ((x < y) ? -1 : ((x > y) ? 1 : 0));
        })
        plotterLineLcChart(walletContainer,wallet_dataset)
        // Table open_trades
        contentHTML(`
        <h6>Open trades</h6>
        <table class="table table-bordered table-hover table-dark">
            <tbody id="table-open-trades">
                <thead>
                    <tr>
                        <th scope="col">Bid</th>
                        <th scope="col">Buy price</th>
                        <th scope="col">Buy time</th>
                        <th scope="col">Stop loss</th>
                        <th scope="col">Quantity</th>
                        <th scope="col">Jumps</th>
                    </tr>
                </thead>
            </tbody>
        </table>`)
        tableOpenTrades = $('#table-open-trades')
        for (const [time,trade] of Object.entries(open_trades)) {
            pnl = trade.offer-trade.bid
            tableOpenTrades.append(`
            <tr class="table-primary">
                <td>`+trade.bid+`</td>
                <td>`+trade.buy_price+`</td>
                <td>`+trade.buy_time+`</td>
                <td>`+trade.stop_loss+`</td>
                <td>`+trade.qty+`</td>
                <td>`+trade.jumps+`</td>
            </tr>
            `)
        }
        // Table closed trades
        contentHTML(`
        <h6>Closed trades</h6>
        <table class="table table-bordered table-hover table-dark">
            <tbody id="table-close-trades">
                <thead>
                    <tr>
                        <th scope="col">Bid</th>
                        <th scope="col">Buy price</th>
                        <th scope="col">Buy time</th>
                        <th scope="col">Offer</th>
                        <th scope="col">Sell price</th>
                        <th scope="col">Sell time</th>
                        <th scope="col">Stop loss</th>
                        <th scope="col">Quantity</th>
                        <th scope="col">Jumps</th>
                        <th scope="col">PNL</th>
                    </tr>
                </thead>
            </tbody>
        </table>`)
        tableCloseTrades = $('#table-close-trades')
        for (const [time,trade] of Object.entries(close_trades)) {
            pnl = trade.offer-trade.bid
            tableCloseTrades.append(`
            <tr class="table-`+contentColorPosNeg(pnl)+`">
                <td>`+trade.bid+`</td>
                <td>`+trade.buy_price+`</td>
                <td>`+trade.buy_time+`</td>
                <td>`+trade.offer+`</td>
                <td>`+trade.sell_price+`</td>
                <td>`+trade.sell_time+`</td>
                <td>`+trade.stop_loss+`</td>
                <td>`+trade.qty+`</td>
                <td>`+trade.jumps+`</td>
                <td>`+pnl+`</td>
            </tr>
            `)
        }
    })
}

function plotterPlotLabelsCusum(dpValues,container){
    $.get('/api/plotter/labels/cusum/'+dpValues.symbol+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(data)=>{
        contentRemoveLoading(container)
        container.append('<h6><b>Cusum events</b> count <b>'+data.count_cusum+'</b> <b>threshold</b> '+data.threshold+'</h6>')
        container.append('<img src="data:image/png;base64, '+data.image_base64+'">')
    })
}

function plotterPlotLabelsTbm(dpValues,container){
    $.get('/api/plotter/labels/tbm/'+dpValues.symbol+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(data)=>{
        contentRemoveLoading(container)
        container.append('<h6><b>Tbm samples</b> count <b>'+data.count_tbm+'</b></h6>')
        container.append('<img src="data:image/png;base64, '+data.image_base64+'">')
    })
}

function plotterPlotLabelsBalance(dpValues,container){
    $.get('/api/plotter/labels/balance/'+dpValues.symbol+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(data)=>{
        contentRemoveLoading(container)
        container.append('<h6><b>Balance</b></h6>')
        container.append('<img src="data:image/png;base64, '+data.image_base64+'">')
    })
}

function plotterGetModelTechMap(next){
    $.get('/api/plotter/models/tech/results/list',(list)=>{
        plotterModelTechMap = list
        next()
    })
}

function plotterPlotConfusionMatrix(labels,confusion_matrix){
    contentHTML('<th scope="col">#</th>')
    labels.forEach((label)=>{contentHTML('<th scope="col" class="bg-success p-2">'+label+'</th>')})
    contentHTML('</tr>')
    confusion_matrix.forEach((row,i)=>{
        contentHTML('<tr>')
        contentHTML('<th class="bg-success p-2" scope="row">'+labels[i]+'</th>')
        row.forEach((col,j)=>{
            contentHTML('<td class="'+(i == j ? 'bg-primary': 'bg-dark')+' p-2">'+(col/row.reduce((sum, a) => sum + a, 0)).toFixed(2)+'</td>')
        })
        contentHTML('</tr>')
    })
}

function PlotterPlotFeatureImportances(feature_importances){
    contentHTML('<table class="table table-bordered table-hover table-dark"><tbody id="table-feature-importances"><thead><tr><th scope="col">Feature</th><th scope="col">Importance</th></tr></thead>')
    table = $('#table-feature-importances')
    feature_importances = Object.entries(feature_importances).sort((a,b) => b[1]-a[1])
    feature_importances.forEach((i)=>{table.append('<tr><td>'+i[0]+'</td><td>'+i[1]+'</td></tr>')})
}

function plotterPlotModelTechResults(results){
    contentTitle('Model - Tech - Results - '+results.name)
    let labels = [-1,0,1]
    contentClearContent()
    contentHTML('<h3>F1 score mean: '+results.score.f1_score_mean+'</h3>')
    contentCollapse('Classifier configuration',JSON.stringify(results.clf_config,null,2))
    contentCollapse('Features',JSON.stringify(Object.keys(JSON.parse(results.score.feature_importances))))
    plotterPlotConfusionMatrix(labels,results.score.confusion_matrix)
    contentBarChart('f1-score',labels,results.score.f1_score)
    contentLineChart('cross-val-score',[1,2,3,4,5],results.score.cross_val_score)
    PlotterPlotFeatureImportances(JSON.parse(results.score.feature_importances))
}

function plotterModelTechResults(){
    contentTitle('Model - Tech - Results')
    plotterGetModelTechMap(()=>{
        Object.entries(plotterModelTechMap).forEach((results)=>{
            results = results[1]
            results.score.f1_score_mean = (results.score.f1_score.reduce((a, b) => a + b, 0) / results.score.f1_score.length).toFixed(3)
            contentButton('<b>'+results.name+'</b> f1 score mean: <b>'+results.score.f1_score_mean+'</b>',()=>{plotterPlotModelTechResults(results)})
        })
    })
}

function plotterGetBacktestMap(next){
    $.get('/api/plotter/market/backtest/results/list',(list)=>{
        plotterBacktestMap = list
        next()
    })
}

function plotterPlotMarketResults(prefix,results){
    contentTitle(prefix+' - Results - '+results.name)
    contentClearContent()
    if (Object.keys(results.close_trades) == 0 && Object.keys(results.open_trades) == 0) {
        contentHTML("Waiting for trades ...")
        return
    }
    let pnl = Math.round(results.wallet[results.stable] - results.stable_start)
    let pnl_pct = Math.round(results.wallet[results.stable] * 100 / results.stable_start)
    let dpValues = {
        'symbol':'BTCUSDT',
        'period':'1h',
        'start': new Date(Object.keys(results.close_trades)[0]).toLocaleDateString("en-US",{year:"numeric",month:"2-digit",day:"2-digit"}).replace(/\//g,'-'),
        'end': new Date().toLocaleDateString("en-US",{year:"numeric",month:"2-digit",day:"2-digit"}).replace(/\//g,'-')
    }
    contentHTML('<h3>Perf: '+pnl_pct+'%</h3>')
    contentHTML('<h3>PNL: <span class="text-'+contentColorPosNeg(pnl)+'">'+pnl+'$<span>')
    contentHTML('<h4>Wallet</h4>')
    contentHTML('<li>Coin: <b>'+results.coin+'</b> Stable: <b>'+results.stable+'</b></li>')
    contentHTML('<li>Start Coin: <b>'+results.coin_start+'</b> End Stable: <b>'+results.stable_start+'</b></li>')
    contentHTML('<li>End Coin: <b>'+results.wallet[results.coin]+'</b> End Stable: <b>'+results.wallet[results.stable]+'</b></li>')
    contentHTML('<h4>Time</h4>')
    contentHTML('<li>Period: <b>'+dpValues.period+'</b> Start: <b>'+dpValues.start+'</b> End: <b>'+dpValues.end+'</b>')
    contentDiv('trades-ohlc')
    let container = $('#trades-ohlc')
    contentShowLoading(container)
    plotterPlotTrades(dpValues,results.stable_start,results.open_trades,results.close_trades,container)
}

function plotterBacktestResults(){
    contentTitle('Backtest - Results')
    plotterGetBacktestMap(()=>{
        Object.entries(plotterBacktestMap).forEach((results)=>{
            results = results[1]
            let pnl_pct = Math.round(results.wallet[results.stable] * 100 / results.stable_start)
            contentButton('<b>'+results.name+'</b> Perf: <b>'+pnl_pct+'%</b>',()=>{plotterPlotMarketResults('Backtest',results)})
        })
    })
}

function plotterPaperResults(){
    $.get('/api/plotter/market/paper/results',results=>{
        plotterPlotMarketResults('Paper',results)
    })
}