var plotterDatasetTechFeaturesMap = "";
var plotterModelTechMap = [];

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
        container.append('<h6><b>Cusum events</b> count <b>'+data.count_cusum+'</b> <b>threshold</b> '+data.threshold+'</h6>')
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
    contentCollapse('Features',JSON.stringify(results.features,null,2))
    plotterPlotConfusionMatrix(labels,results.score.confusion_matrix)
    contentBarChart('f1-score',labels,results.score.f1_score)
    contentLineChart('cross-val-score',[1,2,3,4,5],results.score.cross_val_score)
    PlotterPlotFeatureImportances(JSON.parse(results.score.feature_importances))
    console.log(results)
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