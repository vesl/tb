var plotterDatasetTechFeaturesMap = "";

function plotterGetDatasetTechFeaturesMap(then){
    $.get('/api/plotter/dataset/tech/features/map',(featuresMapJson)=>{
        plotterDatasetTechFeaturesMap = JSON.parse(featuresMapJson)
        then(plotterDatasetTechFeaturesMap)
    })
}

function plotterLineLcChart(node,data){
    var plot = LightweightCharts.createChart(document.getElementById(node[0].id),{height:200})
    let series = plot.addLineSeries({color:'#'+((1 << 24) * Math.random() | 0).toString(16).padStart(6, "0")})
    series.setData(data)
}

function plotterGetDatasetTechFeatureData(dataset,feature){
    let featureData = []
    for (const i in dataset) {
        featureData.push({'time':dataset[i]['time'],'value':dataset[i][feature]})
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
        contentButton('Plot correlation',()=>{plotterPlotToggle('correlation',plotterPlotDatasetTechCorrelation)})
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

function plotterPlotDatasetTechCorrelation(dpValues,container){
    var featuresList = Object.getOwnPropertyNames(plotterDatasetTechFeaturesMap)
    $.get('/api/plotter/dataset/tech/correlation/'+featuresList.toString()+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(data)=>{
        contentRemoveLoading(container)
        container.append('<h6><b>Features correlation</b></h6>')
        container.append('<img src="data:image/png;base64, '+data.image_base64+'">')
    })
}

function plotterPlotLabelsCusum(dpValues,container){
    $.get('/api/plotter/labels/cusum/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(data)=>{
        contentRemoveLoading(container)
        container.append('<h6><b>Cusum events</b> count <b>'+data.count_cusum+'</b></h6>')
        container.append('<img src="data:image/png;base64, '+data.image_base64+'">')
    })
}

function plotterPlotLabelsTbm(dpValues,container){
    $.get('/api/plotter/labels/tbm/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(data)=>{
        contentRemoveLoading(container)
        container.append('<h6><b>Tbm samples</b> count <b>'+data.count_tbm+'</b></h6>')
        container.append('<img src="data:image/png;base64, '+data.image_base64+'">')
    })
}

function plotterPlotLabelsBalance(dpValues,container){
    $.get('/api/plotter/labels/balance/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(data)=>{
        contentRemoveLoading(container)
        container.append('<h6><b>Balance</b></h6>')
        container.append('<img src="data:image/png;base64, '+data.image_base64+'">')
    })
}