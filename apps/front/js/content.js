function setContentTitle(title){
    $('#content-title').html("<h3>"+title.charAt(0).toUpperCase() + title.slice(1)+"</h3>")
}

function setContent(content){
    $('#content').html(content)
}