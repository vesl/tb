var plotterDatasetTechFeaturesMap = "";

function plotterDatasetTech(){
    contentTitle('Dataset - Tech')
    plotterGetDatasetTechFeaturesMap((featuresMap)=>{
        contentCollapse('Features list',JSON.stringify(featuresMap,null,2))
        contentDatePicker()
        contentButton('Plot features',()=>{plotterPlotDatasetTechFeatures()})
    })
}

function plotterLabels(){
    contentTitle('Labels')
    contentDatePicker()
    contentButton('Plot cusum',()=>{plotterPlotLabelsCusum()},'m-2')
    contentButton('Plot TBM',()=>{plotterPlotLabelsTbm()},'m-2')
    contentButton('Plot balance',()=>{plotterPlotLabelsBalance()},'m-2')
}

function plotterGetDatasetTechFeaturesMap(then){
    $.get('/api/plotter/dataset/tech/features/map',(featuresMapJson)=>{
        plotterDatasetTechFeaturesMap = JSON.parse(featuresMapJson)
        then(plotterDatasetTechFeaturesMap)
    })
}

function plotterLineLcChart(node,data){
    var plot = LightweightCharts.createChart(document.getElementById(node[0].id),{height:200})
    let series = plot.addLineSeries({color:'#'+((1 << 24) * Math.random() | 0).toString(16).padStart(6, "0")})
    console.log(data)
    series.setData(data)
}

function plotterGetDatasetTechFeatureData(dataset,feature){
    let featureData = []
    for (const i in dataset) {
        featureData.push({'time':dataset[i]['time'],'value':dataset[i][feature]})
    }
    return featureData
}

function plotterPlotDatasetTechFeatures(){
    contentHTML('<p id="plot-features">')
    var container = $('#plot-features')
    var dpValues = getDpValues()
    if (!container.is(':empty') || !dpValues){container.empty();return;}
    var featuresList = Object.getOwnPropertyNames(plotterDatasetTechFeaturesMap)
    contentShowLoading(container)
    $.get('/api/plotter/dataset/tech/feature/'+featuresList.toString()+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(dataset)=>{
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

function plotterPlotLabelsCusum(){
    contentHTML('<p id="plot-labels-cusum">')
    var container = $('#plot-labels-cusum')
    var dpValues = getDpValues()
    if (!container.is(':empty') || !dpValues){container.empty();return;}
    contentShowLoading(container)
    $.get('/api/plotter/labels/cusum/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(data)=>{
        contentRemoveLoading(container)
        container.append('<h6><b>Cusum events</b> couunt <b>'+data.count_cusum+'</b></h6>')
        container.append('<img src="data:image/png;base64, '+data.image_base64+'">')
    })
}

function plotterPlotLabelsTbm(){
    contentHTML('<p id="plot-labels-tbm">')
    var container = $('#plot-labels-tbm')
    var dpValues = getDpValues()
    if (!container.is(':empty') || !dpValues){container.empty();return;}
    contentShowLoading(container)
    $.get('/api/plotter/labels/tbm/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(data)=>{
        contentRemoveLoading(container)
        container.append('<h6><b>Tbm samples</b> count <b>'+data.count_tbm+'</b></h6>')
        container.append('<img src="data:image/png;base64, '+data.image_base64+'">')
    })
}

function plotterPlotLabelsBalance(){
    contentHTML('<p id="plot-labels-balance">')
    var container = $('#plot-labels-balance')
    var dpValues = getDpValues()
    if (!container.is(':empty') || !dpValues){container.empty();return;}
    contentShowLoading(container)
    $.get('/api/plotter/labels/balance/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(data)=>{
        contentRemoveLoading(container)
        container.append('<h6><b>Balance</b></h6>')
        container.append('<img src="data:image/png;base64, '+data.image_base64+'">')
    })
}