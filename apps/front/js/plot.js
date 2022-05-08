function setupPlotFinance(){
    plot = new PlotLc('Finance plots',plotFinance)
    plot.show()
}

// Finance plots
function plotFinance(plot){
    dates = plot.getDates()
    if (dates == false) return
    // create ohlc + volume chart anyway
    plot.createSubPlot('ohlc','finance','open,high,low,close,volume',dates,function(plotDiv,data){
        const chartsOhlc = plot.createLcChart(plotDiv)
        const ohlcSeries = chartsOhlc.addCandlestickSeries()
        const volumeSeries = chartsOhlc.addHistogramSeries({
            color: '#aeaeae',
            lineWidth: 2,
            priceFormat: {type: 'volume'},
            overlay: true,
            scaleMargins: {
                top: 0.8,
                bottom: 0,
            }
        })
        ohlcSeries.setData(data)
        volumeSeries.setData(plot.extractKeyAsValue(data,'volume'))
        plot.getIndicators()
        for (const indicator in plot.indicatorsAvail){
            plot.indicatorsAvail[indicator](plot,dates)
        }
    })
}

function plotFinanceRSI(plot,dates){
    plot.createSubPlot('rsi','finance','rsi',dates,function(plotDiv,data){
        const chartRSI = plot.createLcChart(plotDiv)
        const rsiSeries = chartRSI.addLineSeries({lineWidth:2})
        console.log(plot.extractKeyAsValue(data,'rsi'))
        rsiSeries.setData(plot.extractKeyAsValue(data,'rsi'))
    })
    // Plotter ne retourne pas la clé RSI
}

function plotFinanceMACD(plot,dates){
    
}

function plotFinanceADX(plot,dates){
    
}

function plotFinanceAPO(plot,dates){
    
}

function plotFinanceAroon(plot,dates){
    
}

function plotFinanceBOP(plot,dates){
    
}

function plotFinanceCCI(plot,dates){
    
}

function plotFinanceCMO(plot,dates){
    
}

function plotFinanceDX(plot,dates){
    
}

function plotFinanceMFI(plot,dates){
    
}

function plotFinanceMinus(plot,dates){
    
}

function plotFinanceMOM(plot,dates){
    
}

function plotFinancePlus(plot,dates){
    
}

function plotFinancePPO(plot,dates){
    
}

function plotFinanceROC(plot,dates){
    
}

function plotFinanceStoch(plot,dates){
    
}

function plotFinanceUltosc(plot,dates){
    
}

function plotFinanceWillr(plot,dates){
    
}

function plotFinanceIchimoku(plot,dates){
    
}
