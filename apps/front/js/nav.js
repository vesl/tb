// Nav map
const navMap = {
    'Plotter': {
        'Dataset - Tech': ()=>{plotterDatasetTech()},
        'Dataset - Ichimoku': ()=>{plotterDatasetIchimoku()},
        'Dataset - Chartist': ()=>{plotterDatasetChartist()},
        'Labels': ()=>{plotterLabels()},
        'Model - Tech - Results': ()=>{plotterModelTechResults()},
        'Model - Ichimoku - Results': ()=>{plotterModelIchimokuResults()},
        'Backtest - Results': ()=>{plotterBacktestResults()},
        'Paper - Results': ()=>{plotterPaperResults()}
    },
    'Trainer': {
        'Model - Tech': ()=>{trainerModelTech()},
        'Model - Ichimoku': ()=>{trainerModelIchimoku()}, 
    },
    'Trader': {
        'Backtest': ()=>{traderBacktest()},
    }
}

// Create Nav
window.onload = function () {
    for (const app in navMap) {
        $('#nav').append('<li><strong>'+app+'</strong></li>')
        for (const appPage in navMap[app]) {
            let a = $('<a href=#>').append(appPage).click(function(){contentClear();navMap[app][appPage]();})
            let li = $('<li>').append(a)
            $('#nav').append(li)
        }
    }
}