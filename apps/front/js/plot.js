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
        const chartsOhlc = plot.createLcChart(plotDiv,400)
        const ohlcSeries = chartsOhlc.addCandlestickSeries()
        const volumeSeries = chartsOhlc.addHistogramSeries({
            color: '#AEAEAE',
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
        const rsiSeries = chartRSI.addLineSeries({color:"#4B7BFD"})
        rsiSeries.setData(plot.extractKeyAsValue(data,'rsi'))
    })
    // Plotter ne retourne pas la clé RSI
}

function plotFinanceMACD(plot,dates){
    plot.createSubPlot('macd','finance','macd',dates,function(plotDiv,data){
        const chartMACD = plot.createLcChart(plotDiv)
        const macdSeries = chartMACD.addLineSeries({color:'#FF7070'})
        const macdSignalSeries = chartMACD.addLineSeries({color:'#FFBC70'})
        const macdHistSeries = chartMACD.addHistogramSeries({
                color: '#AEAEAE',
                lineWidth: 2,
                priceFormat: {type: 'volume'},
                overlay: true,
                scaleMargins: {
                    top: 0.8,
                    bottom: 0,
                }
            })
        macdSeries.setData(plot.extractKeyAsValue(data,'macd'))
        macdSignalSeries.setData(plot.extractKeyAsValue(data,'macdsignal'))
        macdHistSeries.setData(plot.extractKeyAsValue(data,'macdhist'))
    })
}

function plotFinanceADX(plot,dates){
    plot.createSubPlot('adx','finance','adx',dates,function(plotDiv,data){
        const chartADX = plot.createLcChart(plotDiv)
        const adxSeries = chartADX.addLineSeries({color:'#F3003A'})
        const adxrSeries = chartADX.addLineSeries({color:'#00F33A'})
        adxSeries.setData(plot.extractKeyAsValue(data,'adx'))
        adxrSeries.setData(plot.extractKeyAsValue(data,'adxr'))
    })
}

function plotFinanceAPO(plot,dates){
    plot.createSubPlot('apo','finance','apo',dates,function(plotDiv,data){
        const chartAPO = plot.createLcChart(plotDiv)
        const apoSeries = chartAPO.addLineSeries({color:"#0051FE"})
        apoSeries.setData(plot.extractKeyAsValue(data,'apo'))
    })
}

function plotFinanceAroon(plot,dates){
    plot.createSubPlot('aroon','finance','aroon',dates,function(plotDiv,data){
        const chartAROON = plot.createLcChart(plotDiv)
        const aroonUpSeries = chartAROON.addLineSeries({color:"#FE00DB"})
        const aroonDownSeries = chartAROON.addLineSeries({color:"#9E00FE"})
        const aroonOscSeries = chartAROON.addLineSeries({color:"#F2A9FC"})
        aroonUpSeries.setData(plot.extractKeyAsValue(data,'aroonup'))
        aroonDownSeries.setData(plot.extractKeyAsValue(data,'aroondown'))
        aroonOscSeries.setData(plot.extractKeyAsValue(data,'aroonosc'))
    })
}

function plotFinanceBOP(plot,dates){
    plot.createSubPlot('bop','finance','bop',dates,function(plotDiv,data){
        const chartBOP = plot.createLcChart(plotDiv)
        const bopSeries = chartBOP.addLineSeries({color:"#C1AA43"})
        bopSeries.setData(plot.extractKeyAsValue(data,'bop'))
    })
}

function plotFinanceCCI(plot,dates){
     plot.createSubPlot('cci','finance','cci',dates,function(plotDiv,data){
        const chartCCI = plot.createLcChart(plotDiv)
        const cciSeries = chartCCI.addLineSeries({color:"#005005"})
        cciSeries.setData(plot.extractKeyAsValue(data,'cci'))
    }) 
}

function plotFinanceCMO(plot,dates){
    plot.createSubPlot('cmo','finance','cmo',dates,function(plotDiv,data){
        const chartCMO = plot.createLcChart(plotDiv)
        const cmoSeries = chartCMO.addLineSeries({color:"#959595"})
        cmoSeries.setData(plot.extractKeyAsValue(data,'cmo'))
    })
}

function plotFinanceDX(plot,dates){
    plot.createSubPlot('dx','finance','dx',dates,function(plotDiv,data){
        const chartDX = plot.createLcChart(plotDiv)
        const dxSeries = chartDX.addLineSeries({color:"#930085"})
        dxSeries.setData(plot.extractKeyAsValue(data,'dx'))
    })
}

function plotFinanceMFI(plot,dates){
    plot.createSubPlot('mfi','finance','mfi',dates,function(plotDiv,data){
        const chartDX = plot.createLcChart(plotDiv)
        const dxSeries = chartDX.addLineSeries({color:"#DBE600"})
        dxSeries.setData(plot.extractKeyAsValue(data,'mfi'))
    })   
}

function plotFinanceMinusDI(plot,dates){
    plot.createSubPlot('minusdi','finance','minusdi',dates,function(plotDiv,data){
        const chartMINUSDI = plot.createLcChart(plotDiv)
        const minusdiSeries = chartMINUSDI.addLineSeries({color:"#0088E6"})
        minusdiSeries.setData(plot.extractKeyAsValue(data,'minusdi'))
    })  
}

function plotFinanceMinusDM(plot,dates){
    plot.createSubPlot('minusdm','finance','minusdm',dates,function(plotDiv,data){
        const chartMINUS = plot.createLcChart(plotDiv)
        const minusdmSeries = chartMINUS.addLineSeries({color:"#83CCFF"})
        minusdmSeries.setData(plot.extractKeyAsValue(data,'minusdm'))
    })
}

function plotFinanceMOM(plot,dates){
    plot.createSubPlot('mom','finance','mom',dates,function(plotDiv,data){
        const chartMOM = plot.createLcChart(plotDiv)
        const momSeries = chartMOM.addLineSeries({color:"#FF8383"})
        momSeries.setData(plot.extractKeyAsValue(data,'mom'))
    })
}

function plotFinancePlusDI(plot,dates){
    plot.createSubPlot('plusdi','finance','plusdi',dates,function(plotDiv,data){
        const chartPLUSDI = plot.createLcChart(plotDiv)
        const plusdiSeries = chartPLUSDI.addLineSeries({color:"#00E819"})
        plusdiSeries.setData(plot.extractKeyAsValue(data,'plusdi'))
    })
}

function plotFinancePlusDM(plot,dates){
    plot.createSubPlot('plusdm','finance','plusdm',dates,function(plotDiv,data){
        const chartPLUSDM = plot.createLcChart(plotDiv)
        const plusdmSeries = chartPLUSDM.addLineSeries({color:"#007C0D"})
        plusdmSeries.setData(plot.extractKeyAsValue(data,'plusdm'))
    })
}

function plotFinancePPO(plot,dates){
    plot.createSubPlot('ppo','finance','ppo',dates,function(plotDiv,data){
        const chartPPO = plot.createLcChart(plotDiv)
        const ppoSeries = chartPPO.addLineSeries({color:"#000F7C"})
        ppoSeries.setData(plot.extractKeyAsValue(data,'ppo'))
    })  
}

function plotFinanceROC(plot,dates){
    plot.createSubPlot('roc','finance','roc',dates,function(plotDiv,data){
        const chartROC = plot.createLcChart(plotDiv)
        const rocSeries = chartROC.addLineSeries({color:"#80209C"})
        rocSeries.setData(plot.extractKeyAsValue(data,'roc'))
    })      
}

function plotFinanceStoch(plot,dates){
    plot.createSubPlot('stoch','finance','stoch',dates,function(plotDiv,data){
        const chartSTOCH = plot.createLcChart(plotDiv)
        const slowkSeries = chartSTOCH.addLineSeries({color:"#FFEC00"})
        const slowdSeries = chartSTOCH.addLineSeries({color:"#FF9E00"})
        slowkSeries.setData(plot.extractKeyAsValue(data,'slowk'))
        slowdSeries.setData(plot.extractKeyAsValue(data,'slowd'))
    })
}

function plotFinanceStochF(plot,dates){
    plot.createSubPlot('stochf','finance','stochf',dates,function(plotDiv,data){
        const chartSTOCHF = plot.createLcChart(plotDiv)
        const fastkSeries = chartSTOCHF.addLineSeries({color:"#00CDFF"})
        const fastdSeries = chartSTOCHF.addLineSeries({color:"#002B8E"})
        fastkSeries.setData(plot.extractKeyAsValue(data,'fastk'))
        fastdSeries.setData(plot.extractKeyAsValue(data,'fastd'))
    })
}

function plotFinanceStochRSI(plot,dates){
    plot.createSubPlot('stochrsi','finance','stochrsi',dates,function(plotDiv,data){
        const chartSTOCHF = plot.createLcChart(plotDiv)
        const fastkSeries = chartSTOCHF.addLineSeries({color:"#00FF0C"})
        const fastdSeries = chartSTOCHF.addLineSeries({color:"#008E06"})
        fastkSeries.setData(plot.extractKeyAsValue(data,'fastkrsi'))
        fastdSeries.setData(plot.extractKeyAsValue(data,'fastdrsi'))
    })
}

function plotFinanceTrix(plot,dates){
    plot.createSubPlot('trix','finance','trix',dates,function(plotDiv,data){
        const chartTRIX = plot.createLcChart(plotDiv)
        const trixSeries = chartTRIX.addLineSeries({color:"#FF0078"})
        trixSeries.setData(plot.extractKeyAsValue(data,'trix'))
    })      
}

function plotFinanceUltosc(plot,dates){
    plot.createSubPlot('ultosc','finance','ultosc',dates,function(plotDiv,data){
        const chartULTOSC = plot.createLcChart(plotDiv)
        const ultoscSeries = chartULTOSC.addLineSeries({color:"#FF0078"})
        ultoscSeries.setData(plot.extractKeyAsValue(data,'ultosc'))
    })         
}

function plotFinanceWillr(plot,dates){
    plot.createSubPlot('willr','finance','willr',dates,function(plotDiv,data){
        const chartWILLR = plot.createLcChart(plotDiv)
        const willrSeries = chartWILLR.addLineSeries({color:"#7C4B00"})
        willrSeries.setData(plot.extractKeyAsValue(data,'willr'))
    })      
}

function plotFinanceIchimoku(plot,dates){
    plot.createSubPlot('ichimoku','finance','ichimoku',dates,function(plotDiv,data){
        const chartICHIMOKU = plot.createLcChart(plotDiv)
        const tenkanSeries = chartICHIMOKU.addLineSeries({color:"#FF0000"})
        const kijunSeries = chartICHIMOKU.addLineSeries({color:"#0C00FF"})
        const ssaSeries = chartICHIMOKU.addLineSeries({color:"#00FF04"})
        const ssbSeries = chartICHIMOKU.addLineSeries({color:"#8F00FF"})
        tenkanSeries.setData(plot.extractKeyAsValue(data,'tenkan'))
        kijunSeries.setData(plot.extractKeyAsValue(data,'kijun'))
        ssaSeries.setData(plot.extractKeyAsValue(data,'ssa'))
        ssbSeries.setData(plot.extractKeyAsValue(data,'ssb'))
    })    
}
