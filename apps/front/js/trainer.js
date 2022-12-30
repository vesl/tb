function trainerCheckRun(next){
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
    if (dpValues) $.get('/api/trainer/models/tech/train/'+dpValues.period+'/'+dpValues.start+'/'+dpValues.end)
    setTimeout(()=>{trainerModelTech()},2000)
}

function trainerModelTech(){
    contentTitle('Model - Tech')
    contentClearContent()
    trainerCheckRun(()=>{
        contentDatePicker()
        contentButton('Train',()=>{trainerTrainModelTech()}) 
    })
}