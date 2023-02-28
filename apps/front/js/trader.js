function traderBacktestCheckRun(next){
    $.get('/api/trader/market/backtest/check_run',(data)=>{
        if (Object.keys(data).length > 0) {
            contentClearContent()
            contentHTML('Backtest is already running ...')
            contentPre(JSON.stringify(data,undefined, 2))
            setTimeout(()=>{traderBacktest()},10000)
        }
        else next()
    })
}

function traderTradeBacktest(){
    var dpValues = getDpValues()
    if (dpValues) $.get('/api/trader/market/backtest/'+dpValues.symbol+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end)
    setTimeout(()=>{traderBacktest()},2000)
}

function traderBacktest(){
    contentTitle('Backtest')
    contentClearContent()
    traderBacktestCheckRun(()=>{
        contentDatePicker()
        contentButton('Backtest',()=>{traderTradeBacktest()})
    })
}