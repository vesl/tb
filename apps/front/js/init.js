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

window.onload = function () {

    for (const app in nav) {

        const appLi = $('<li>')
        const appButton = $('<button>')
        const appDiv = $('<div>')

        appLi.addClass('mb-1')
        appButton.addClass('btn btn-toggle align-items-center rounded collapsed')
        appButton.attr('data-bs-toggle','collapse')
        appButton.attr('data-bs-target','#'+app.toLowerCase())
        appButton.attr('aria-expanded','false')
        appButton.text(app)
        appDiv.addClass('collapse')
        appDiv.attr('id',app.toLowerCase())

        for (const menu in nav[app]) {
            const ulMenu = $('<ul>')
            const liMenu = $('<li>')
            const aMenu = $('<a>')
            ulMenu.addClass('btn-toggle-nav list-unstyled fw-normal pb-1 small')
            aMenu.attr('href','#')
            aMenu.addClass('link-dark rounded')
            aMenu.click(nav[app][menu])
            aMenu.text(menu)

            liMenu.append(aMenu)
            ulMenu.append(liMenu)
            appDiv.append(ulMenu)
        } 

        appLi.append(appButton)
        appLi.append(appDiv)
        $('#nav').append(appLi)
    }
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