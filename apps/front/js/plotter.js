var plotterDatasetTechFeaturesList = "";

function plotterDatasetTech(){
    contentTitle('Dataset - Tech')
    plotterGetDatasetTechFeaturesList((features)=>{
        contentCollapse('Features list',JSON.stringify(features,null,2))
        contentDatePicker()
        contentButton('Plot features',()=>{plotterDatasetTechFeatures()})
        contentHTML('<p id="plot-features">')
    })
}

function plotterGetDatasetTechFeaturesList(then){
    $.get('/api/plotter/dataset/tech/features/list',(featuresJson)=>{
        let features = JSON.parse(featuresJson)
        plotterDatasetTechFeaturesList = features
        then(features)
    })
}

function plotterDatasetTechFeatures(){
    var container = $('#plot-features')
    var dpValues = getDpValues()
    if (!container.is(':empty') || !dpValues){container.empty();return;}
    Object.entries(plotterDatasetTechFeaturesList).forEach(([feature,props])=>{
        var featureContainer = $('<div id="plot-'+feature+'">')
        container.append('<b>'+feature.toUpperCase()+'</b> source: <b>'+props['source']+'</b> scaled: <b>'+props['scaled']+'</b>')
        container.append(featureContainer)
        contentShowLoading(featureContainer)
        $.get('/api/plotter/dataset/tech/feature/'+feature+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end,(feature_data)=>{
            contentRemoveLoading(featureContainer)
        })
    })
}