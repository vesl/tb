function contentClear(){
    $('#content-title').empty()
    $('#content').empty()
}

function contentTitle(title) {
    $('#content-title').text(title)
}

function contentHTML(html){
    $('#content').append(html)
}


function contentPre(html,cls=''){
    contentHTML('<pre class="bg-light text-dark rounded '+cls+'">'+html+'</pre>')
}

function contentButton(title,fn){
    var button = $('<button class="btn btn-primary m-2" data-bs-toggle="button" type="button">')
    button.append(title)
    button.click(fn)
    contentHTML(button)
}

function contentCollapse(title,html){
    var id = title.replace(' ','-').toLowerCase()
    contentButton(title,()=>{$('.collapse-'+id).collapse('toggle')})
    contentPre(html,'mt-3 collapse collapse-'+id)
}

function contentDatePicker(next){
    contentHTML($('<div id="datepicker" class="mt-3 mb-3">'))
    $('#datepicker').load('/datepicker.html')
}

function contentShowLoading(node){
    node.load('/loading.html')
}

function contentRemoveLoading(node){
    node.children("#loading").remove()
}