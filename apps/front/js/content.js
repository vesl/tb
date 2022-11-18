function contentClear(){
    $('#content-title').empty()
    $('#content').empty()
}

function contentTitle(title) {
    $('#content-title').text(title)
}

function contentPre(text){
    $('#content').append('<pre class="bg-light text-dark rounded">'+text+'</pre>')
}