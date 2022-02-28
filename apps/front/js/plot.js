function loading(){
    $.get('/loading.html',function(html){$('#plot').html(html)})
}

function initForm(){
    $.get('/plot.html',function(html){$('#content').html(html)})
    $('#datepicker-from').datepicker({format:'yyyy-mm-dd'})
    $('#datepicker-to').datepicker({format:'yyyy-mm-dd'})
}

function getFormValues(){
    var values = {}
    values['from'] = $('#datepicker-from').val()
    values['to'] = $('#datepicker-to').val()
    values['timescale'] = $('#timescale').val()
    if(values['from'] == undefined || values['to'] == undefined || values['timescale'] == 'Timescale'){
        alert('Fill the form')
        return false
    } else {
        return values
    }
}