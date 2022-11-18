function scrapperStatus() {
    $.get('/api/scrapper/status/',(status) => {
        contentTitle('Scrapper status')
        contentPre(JSON.stringify(status,undefined, 2))
    })
}