// Edit nav
const nav = {
    'Scrapper': {
        'Status': function(){showStatus('scrapper')}
    },
    'Plotter': {
        'Status': function(){showStatus('plotter')},
        'Finance': function(){showPlotsFinance()},
        'Labels': function(){showPlotsLabels()},
    },
    'Dataset': {
        'Status': function(){showStatus('dataset')},
    }
}