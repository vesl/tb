function trainerCheckRunTech(next){
    $.get('/api/trainer/models/tech/check_run',(data)=>{
        if (Object.keys(data).length > 0) {
            contentClearContent()
            contentHTML('Trainer is already running ...')
            contentPre(JSON.stringify(data,undefined, 2))
            setTimeout(()=>{trainerModelTech()},10000)
        }
        else next()
    })
}

function trainerTrainModelTech(){
    var dpValues = getDpValues()
    if (dpValues) $.get('/api/trainer/models/tech/train/'+dpValues.symbol+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end)
    setTimeout(()=>{trainerModelTech()},2000)
}

function trainerModelTech(){
    contentTitle('Model - Tech')
    contentClearContent()
    trainerCheckRunTech(()=>{
        contentDatePicker()
        contentButton('Train',()=>{trainerTrainModelTech()}) 
    })
}

function trainerCheckRunIchimoku(next){
    $.get('/api/trainer/models/ichimoku/check_run',(data)=>{
        if (Object.keys(data).length > 0) {
            contentClearContent()
            contentHTML('Trainer is already running ...')
            contentPre(JSON.stringify(data,undefined, 2))
            setTimeout(()=>{trainerModelIchimoku()},10000)
        }
        else next()
    })
}

function trainerTrainModelIchimoku(){
    var dpValues = getDpValues()
    if (dpValues) $.get('/api/trainer/models/ichimoku/train/'+dpValues.symbol+'/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end)
    setTimeout(()=>{trainerModelTech()},2000)
}

function trainerModelIchimoku(){
    contentTitle('Model - Ichimoku')
    contentClearContent()
    trainerCheckRunIchimoku(()=>{
        contentDatePicker()
        contentButton('Train',()=>{trainerTrainModelIchimoku()}) 
    })
}