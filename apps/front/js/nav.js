// add item to nav
const nav = {
    'Scrapper': {
        'Status': function(){showStatus('scrapper')}
    },
    'Plotter': {
        'Status': function(){showStatus('plotter')},
        'Finance': function(){showPlotsFinance()}
    }
}

// Never touch this deathloop
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