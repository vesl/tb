// Nav map
const navMap = {
    'Scrapper': {
        'Status': function(){showStatus('scrapper')}
    },
    'Plotter': {
        'Status': function(){showStatus('plotter')},
        'Finance': function(){setupPlotFinance()},
        'Labels': function(){showPlotsLabels()},
        'Correlation': function(){showPlotsCorrelation()},
    },
}

// Create Nav
window.onload = function () {

    for (const app in navMap) {
        navApp = new NavApp(app)
        for (const appSubNav in navMap[app]) {
            subnav = new SubNav(appSubNav,navMap[navApp.app][appSubNav])
            navApp.div.append(subnav.render())
        }
        $('#nav').append(navApp.render())
    }
}