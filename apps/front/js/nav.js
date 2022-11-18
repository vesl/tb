// Nav map
const navMap = {
    'Scrapper': {
        'Status': function(){showStatus('scrapper')},
        'Candles': function(){showCandles()},
    },
    'Plotter': {
        'Status': function(){showStatus('plotter')},
        'Dataset - Tech': function(){},
    },
}

// Create Nav
window.onload = function () {
    for (const app in navMap) {
        $('#nav').append('<li><strong>'+app+'</strong></li>')
        for (const appPage in navMap[app]) {
            let a = $('<a href=#>').append(appPage).click(function(){clearContent();navMap[app][appPage]})
            let li = $('<li>').append(a)
            $('#nav').append(li)
        }
    }
}