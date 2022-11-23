function scrapperStatus() {
    contentTitle('Scrapper status')
    $.get('/api/scrapper/status/',(status) => {
        contentPre(JSON.stringify(status,undefined, 2))
    })
}