function statusContent(status) {
    var status = JSON.stringify(status,undefined, 2)
    return '<pre class="bg-light text-dark rounded">'+status+'</pre>'
}

function showStatus(app){
    return $.get("/api/"+app+"/status/",function(status){
        setContentTitle(app+" status")
        setContent(statusContent(status))
    })
}