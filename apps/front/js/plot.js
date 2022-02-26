function plotTitle(title){
    $('#content-title').text('Plot '+title)
}

function initPlotSkeleton(){
    $('#content').empty()
    initForm()
    $('#content').append($('<div>').attr('id','plot').addClass('min-80'))
}

function initForm(){
    var form = $('<div>').addClass('plot-form').attr('id','plot-form')
    $('#content').append(form)
    var datepickerTypes = ['from','to']
    datepickerTypes.forEach(function(type){
        var datepicker = getDatepickerFormHtml(type)
        form.append(datepicker)
        $('#datepicker-'+type).datepicker({
            format:'yyyy-mm-dd'
        })
    })
    form.append(getTimescaleFormHtml())
    form.append(getButtonFormHtml())
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

function loading(){
    return `
        <p>
            <div id="loading" align="center" class="loading">
                <div class="spinner-border text-primary" role="status"></div>
                <div class="text-light">Loading plot data...</div>
            </div>
        </p>
        `
}

function getDatepickerFormHtml(type) {
    return `
        <div class="form-check-inline">
            <div class="datepicker-inline input-group w-30">
                <span class="input-group-text" id="basic-addon1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar" viewBox="0 0 16 16">
                        <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"></path>
                    </svg>
                </span>
                <input type="text" class="form-control" placeholder="Plot `+type+`" id="datepicker-`+type+`">
            </div>
        </div>
        `
}

function getTimescaleFormHtml(){
    return `<div class="form-check-inline">
        <div class="input-group">
            <span class="input-group-text" id="basic-addon1">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clock" viewBox="0 0 16 16">
                    <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"></path>
                    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"></path>
                </svg>
            </span>
            <select id="timescale" class="form-control">
                <option selected>Timescale</option>
                <option>1m</option>
                <option>1h</option>
                <option>1d</option>
            </select>
        </div>
    </div>
    `
}

function getButtonFormHtml(){
    return `<div class="form-check-inline">
        <button class="btn btn-primary btn-plot" id="button-plot">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-graph-up" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M0 0h1v15h15v1H0V0Zm14.817 3.113a.5.5 0 0 1 .07.704l-4.5 5.5a.5.5 0 0 1-.74.037L7.06 6.767l-3.656 5.027a.5.5 0 0 1-.808-.588l4-5.5a.5.5 0 0 1 .758-.06l2.609 2.61 4.15-5.073a.5.5 0 0 1 .704-.07Z"></path>
            </svg>
            Plot
        </button>
    </div>
    `
}