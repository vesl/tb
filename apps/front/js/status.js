function statusContent(status) {
    var status = JSON.stringify(status,undefined, 2)
    $('#content').html('<pre class="bg-light text-dark rounded">'+status+'</pre>')
}

function statusTitle(title) {
    $('#content-title').text(title+' status')
}

function showStatus(app){
    statusTitle(app)
    return $.get("/api/"+app+"/status/",function(status){
        statusContent(status)
    })
}