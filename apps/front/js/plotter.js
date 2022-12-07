var plotterDatasetTechFeaturesMap = "";

function plotterDatasetTech(){
    contentTitle('Dataset - Tech')
    plotterGetDatasetTechFeaturesMap((featuresMap)=>{
        contentCollapse('Features list',JSON.stringify(featuresMap,null,2))
        contentDatePicker()
        contentButton('Plot features',()=>{plotterDatasetTechFeatures()})
        contentHTML('<p id="plot-features">')
    })
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

function plotterDatasetTechFeatures(){
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
            container.append('<b>'+feature.toUpperCase()+'</b> source: <b>'+props['source']+'</b> scaled: <b>'+props['scaled']+'</b>')
            container.append(featureContainer)
            plotterLineLcChart(featureContainer,featureData)
        })
    })
}