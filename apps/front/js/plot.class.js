// Plot class
class Plot {
    
    constructor(title,click){
        this.div = this.createDiv()
        this.divPlotForm = this.createDivPlotForm()
        this.content = $('#content')
        this.content_title = $('#content-title')
        this.title = title
        this.click = click
    }
    
    createDiv(){
        return $('<div>')
            .addClass('min-50')
            .attr('id','plot')
    }
    createDivPlotForm(){
        return $('<div>')
            .attr('id','plot-form')
    }
    
    getDates(){
        let dates = {}
        dates['from'] = $('#datepicker-from').val()
        dates['to'] = $('#datepicker-to').val()
        dates['timescale'] = $('#timescale').val()
        if(dates['from'] === '' || dates['to'] === '' || dates['timescale'] === 'Timescale') {
            alert('Fill the form')
            return false
        }
        return dates
    }
    
    getTitle(title){
        return $('<h3>'+title+'</h3>')
    }
    
    setClick(){
        $('#button-plot').click(()=>{this.click(this)})
    }
    
    setDatepickersFormat(){
        $('#datepicker-from').datepicker({format:'yyyy-mm-dd'})
        $('#datepicker-to').datepicker({format:'yyyy-mm-dd'})
    }
    
    showLoading(node,next){
        $.get('/loading.html',(html)=>{node.html(html)
            next()
        })
    }
    
    hideLoading(node){
        node.children('#loading').remove()
    }
    
    show(){
        $.get('/plot_form.html',(html)=>{
            this.divPlotForm.prepend(html)
            this.content_title.html(this.title)
            this.content
                .html(this.divPlotForm)
                .append(this.div)
            this.setClick()
            this.setDatepickersFormat()
        })
    }
    
    createSubPlot(name){
        let plotDivId = 'plot-'+name
        if ($('#'+plotDivId)[0]) $('#'+plotDivId).remove()
        const plotDiv = $('<div>').attr('id',plotDivId)
        this.div.append(plotDiv)
        return plotDiv
    }
}

// PlotLc class
class PlotLc extends Plot {

    constructor(title,click){
        super(title,click)
        this.ul = this.createUl()
        this.indicatorsAvail = {
            'rsi': plotFinanceRSI,
            'macd': plotFinanceMACD,
            'adx': plotFinanceADX,
            'apo': plotFinanceAPO,
            'aroonup': plotFinanceAroonUp,
            'aroondown': plotFinanceAroonDown,
            'aroonosc': plotFinanceAroonOsc,
            'bop': plotFinanceBOP,
            'cci': plotFinanceCCI,
            'cmo': plotFinanceCMO,
            'dx': plotFinanceDX,
            'mfi': plotFinanceMFI,
            'minusdi': plotFinanceMinusDI,
            'minusdm': plotFinanceMinusDM,
            'mom': plotFinanceMOM,
            'plusdi': plotFinancePlusDI,
            'plusdm': plotFinancePlusDM,
            'ppo': plotFinancePPO,
            'roc': plotFinanceROC,
            'slowk': plotFinanceSlowK,
            'slowd': plotFinanceSlowD,
            'fastk': plotFinanceFastK,
            'fastd': plotFinanceFastD,
            'fastkrsi': plotFinanceFastKRSI,
            'fastdrsi': plotFinanceFastDRSI,
            'trix': plotFinanceTrix,
            'ultosc': plotFinanceUltosc,
            'willr': plotFinanceWillr,
            'ichimoku': plotFinanceIchimoku,
        }
    }
    
    createUl(){
        return $('<ul>')
            .attr('id','indicators')
            .addClass('list-unstyled ps-0')
    }
    
    createCheckbox(indicator){
        let div = $('<div>')
            .addClass('form-check form-check-inline')
        let input = $('<input>')
            .addClass('form-check-input')
            .attr('id','checkbox-indicator-'+indicator)
            .attr('type','checkbox')
            .attr('value',indicator)
            .prop('checked',true)
        let label = $('<label>')
            .addClass('form-check-label')
            .attr('for','checkbox-indicator-'+indicator)
            .text(indicator)
        div.append(input)
        div.append(label)
        return div
    }

    show(){
        super.show()
        for(const indicator in this.indicatorsAvail){
            this.ul.append(this.createCheckbox(indicator))
        }
        this.divPlotForm.html(this.ul)
    }
    
    extractKeyAsValue(data,key){
        let ret = []
        for (const i in data) {
            ret.push({'time':data[i]['time'],'value':data[i][key]})
        }
        return ret
    }
    
    getIndicators(){
        this.indicatorsSel = []
        for(const indicator in this.indicatorsAvail){
            if ($('#checkbox-indicator-'+indicator).is(':checked') === true) this.indicatorsSel.push(indicator)
        }
    }
    
    createLcChart(plotDiv,height=200){
        return LightweightCharts.createChart(document.getElementById(plotDiv.attr('id')),{height:height})
    }

    createSubPlotLc(name,category,features,dates,next){
        const plotDiv = this.createSubPlot(name)
        this.showLoading(plotDiv,()=>{
            $.get('/api/plotter/'+category+'/'+features+'/'+dates['timescale']+'/'+dates['from']+'/'+dates['to'],(data)=>{
                next(plotDiv,JSON.parse(data))
                plotDiv.prepend(this.getTitle(name))
                this.hideLoading(plotDiv)
            })
        })
    }
}

class PlotImg extends Plot {
    
    constructor(title,click){
        super(title,click)
    }
    
    createSubPlotImg(name,category,features,dates){
        const plotDiv = this.createSubPlot(name)
        this.showLoading(plotDiv,()=>{
            let img = new Image()
            img.onload = ()=>{this.hideLoading(plotDiv)}
            img.src = '/api/plotter/'+category+'/'+features+'/'+dates['timescale']+'/'+dates['from']+'/'+dates['to']+'/'+features+'.png'
            plotDiv.prepend(this.getTitle(name))
            plotDiv.append(img)
        })
    }
}