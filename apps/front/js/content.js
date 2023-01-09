function contentClear(){
    $('#content-title').empty()
    $('#content').empty()
}

function contentClearContent(){
    $('#content').empty()
}

function contentTitle(title) {
    $('#content-title').text(title)
}

function contentHTML(html){
    $('#content').append(html)
}

function contentDiv(id){
    let div = $('<div id='+id+'>')
    $('#content').append(div)
}

function contentCanvas(id){
    let div = $('<div style="position: relative; height:40vh; width:160vw"><canvas id="'+id+'" height="200"></div>')
    $('#content').append(div)
}

function contentBarChart(name,x,y){
    contentCanvas('chart-'+name)
    const ctx = document.getElementById('chart-'+name)
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: x,
            datasets: [{label: name,data: y}]
        },
    });
}

function contentLineChart(name,x,y){
    contentCanvas('chart-'+name)
    const ctx = document.getElementById('chart-'+name)
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: x,
            datasets: [{label: name,data: y}]
        },
    });
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