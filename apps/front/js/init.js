function initPlotLoading(node){
    $.get('/loading.html',function(html){node.html(html)})
}

function initPlotForm(next){
    $.get('/plot.html',function(html){
        $('#content').html(html)
        $('#datepicker-from').datepicker({format:'yyyy-mm-dd'})
        $('#datepicker-to').datepicker({format:'yyyy-mm-dd'})
        next()
    })
}

function initPlotDiv(){
    divPlot = $('<div>')
    divPlot.attr('id','plot')
    divPlot.addClass('min-50')
    $('#content').append(divPlot)
}

function initPlotIndicatorsForm(){

    const indLi = $('<li>')
    const indButton = $('<button>')
    const indDiv = $('<div>')

    indLi.addClass('mb1')
    indButton.addClass('btn btn-toggle align-items-center rounded collapsed bg-white')
    indButton.attr('data-bs-toggle','collapse')
    indButton.attr('data-bs-target','#indicators-list')
    indButton.attr('aria-expanded','false')
    indButton.text('Indicators')
    indDiv.addClass('collapse')
    indDiv.attr('id','indicators-list')

    indLi.append(indButton)
    indLi.append(indDiv)
    $('#indicators-select').append(indLi)

    for (const indicator in indicators){
        const divCheckBox = $('<div>')
        const inputCheckBox = $('<input>')
        const labelCheckBox = $('<label>')

        divCheckBox.addClass('form-check form-check-inline')
        inputCheckBox.addClass('form-check-input')
        inputCheckBox.attr('id','checkbox-indicator-'+indicator)
        inputCheckBox.attr('type','checkbox')
        inputCheckBox.attr('value',indicator)
        labelCheckBox.addClass('form-check-label')
        labelCheckBox.attr('for','checkbox-indicator-'+indicator)
        labelCheckBox.text(indicator)

        divCheckBox.append(inputCheckBox)
        divCheckBox.append(labelCheckBox)
        indDiv.append(divCheckBox)
    }
}