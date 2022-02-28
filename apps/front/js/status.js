function showStatus(app){
    $('#content-title').text(app+' status')
    $.get("/api/"+app+"/status/",function(status){
        var status = JSON.stringify(status,undefined, 2)
        $('#content').html('<pre class="bg-light text-dark rounded">'+status+'</pre>')
    })
}