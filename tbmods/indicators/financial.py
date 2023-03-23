import pandas as pd
import talib

class Financial:

    def __init__(self,klines):
        self.klines=klines
        self.matype = talib.MA_Type.SMA
        # 20/08 23h SMA
    
    def compute(self,feature,args=None):
        return {
          "ad": self.compute_ad,
          "adosc": self.compute_adosc,
          "adx": self.compute_adx,
          "adxr": self.compute_adxr,
          "apo": self.compute_apo,
          "aroonup": self.compute_aroonup,
          "aroondown": self.compute_aroondown,
          "aroonosc": self.compute_aroonosc,
          "atr": self.compute_atr,
          "avgprice": self.compute_avgprice,
          "bop": self.compute_bop,
          "cci": self.compute_cci,
          "cdl2crows": self.compute_cdl2crows,
          "cdl3blackcrows": self.compute_cdl3blackcrows,
          "cdl3inside": self.compute_cdl3inside,
          "cdl3linestrike": self.compute_cdl3linestrike,
          "cdl3outside": self.compute_cdl3outside,
          "cdl3starinsouth": self.compute_cdl3starinsouth,
          "cdl3whitesoldiers": self.compute_cdl3whitesoldiers,
          "cdlabandonedbaby": self.compute_cdlabandonedbaby,
          "cdladvanceblock": self.compute_cdladvanceblock,
          "cdlbelthold": self.compute_cdlbelthold,
          "cdlbreakaway": self.compute_cdlbreakaway,
          "cdlclosingmarubozu": self.compute_cdlclosingmarubozu,
          "cdlconcealbabywall": self.compute_cdlconcealbabywall,
          "cdlcounterattack": self.compute_cdlcounterattack,
          "cdldarkcloudcover": self.compute_cdldarkcloudcover,
          "cdldoji": self.compute_cdldoji,
          "cdldojistar": self.compute_cdldojistar,
          "cdldragonflydoji": self.compute_cdldragonflydoji,
          "cdlengulfing": self.compute_cdlengulfing,
          "cdleveningdojistar": self.compute_cdleveningdojistar,
          "cdleveningstar": self.compute_cdleveningstar,
          "cdlgapsidesidewhite": self.compute_cdlgapsidesidewhite,
          "cdlgravestonedoji": self.compute_cdlgravestonedoji,
          "cdlhammer": self.compute_cdlhammer,
          "cdlhangingman": self.compute_cdlhangingman,
          "cdlharami": self.compute_cdlharami,
          "cdlharamicross": self.compute_cdlharamicross,
          "cdlhighwave": self.compute_cdlhighwave,
          "cdlhikkake": self.compute_cdlhikkake,
          "cdlhikkakemod": self.compute_cdlhikkakemod,
          "cdlhomingpigeon": self.compute_cdlhomingpigeon,
          "cdlidentical3crows": self.compute_cdlidentical3crows,
          "cdlinneck": self.compute_cdlinneck,
          "cdlinvertedhammer": self.compute_cdlinvertedhammer,
          "cdlkicking": self.compute_cdlkicking,
          "cdlkickingbylength": self.compute_cdlkickingbylength,
          "cdlladderbottom": self.compute_cdlladderbottom,
          "cdllongleggeddoji": self.compute_cdllongleggeddoji,
          "cdllongline": self.compute_cdllongline,
          "cdlmarubozu": self.compute_cdlmarubozu,
          "cdlmatchinglow": self.compute_cdlmatchinglow,
          "cdlmathold": self.compute_cdlmathold,
          "cdlmorningstardojistar": self.compute_cdlmorningstardojistar,
          "cdlmorningstar": self.compute_cdlmorningstar,
          "cdlonneck": self.compute_cdlonneck,
          "cdlpiercing": self.compute_cdlpiercing,
          "cdlrickshawman": self.compute_cdlrickshawman,
          "cdlrisefall3methods": self.compute_cdlrisefall3methods,
          "cdlseparatinglines": self.compute_cdlseparatinglines,
          "cdlshootingstar": self.compute_cdlshootingstar,
          "cdlshortline": self.compute_cdlshortline,
          "cdlspinningtop": self.compute_cdlspinningtop,
          "cdlstalledpattern": self.compute_cdlstalledpattern,
          "cdlsticksandwich": self.compute_cdlsticksandwich,
          "cdltakuri": self.compute_cdltakuri,
          "cdltasukigap": self.compute_cdltasukigap,
          "cdlthrusting": self.compute_cdlthrusting,
          "cdltristar": self.compute_cdltristar,
          "cdlunique3river": self.compute_cdlunique3river,
          "cdlupsidegap2crows": self.compute_cdlupsidegap2crows,
          "cdlxsidegap3methods": self.compute_cdlxsidegap3methods,
          "cmo": self.compute_cmo,
          "dx": self.compute_dx,
          "fastk": self.compute_fastk,
          "fastd": self.compute_fastd,
          "fastkrsi": self.compute_fastkrsi,
          "fastdrsi": self.compute_fastdrsi,
          "hcdcperiod": self.compute_hcdcperiod,
          "hcdcphase": self.compute_hcdcphase,
          "htphasorin": self.compute_htphasorin,
          "htphasorqua": self.compute_htphasorqua,
          "htsinesine": self.compute_htsinesine,
          "htsinelead": self.compute_sinelead,
          "httrendmode": self.compute_httrendmode,
          "kijun": self.compute_kijun,
          "laggingspan": self.compute_laggingspan,
          "ma": self.compute_ma,
          "macd": self.compute_macd,
          "macdhist": self.compute_macdhist,
          "macdsignal": self.compute_macdsignal,
          "medprice": self.compute_medprice,
          "mfi": self.compute_mfi,
          "minusdi": self.compute_minusdi,
          "minusdm": self.compute_minusdm,
          "mom": self.compute_mom,
          "natr": self.compute_natr,
          "obv": self.compute_obv,
          "plusdi": self.compute_plusdi,
          "plusdm": self.compute_plusdm,
          "ppo": self.compute_ppo,
          "roc": self.compute_roc,
          "rocp": self.compute_rocp,
          "rocr": self.compute_rocr,
          "rsi": self.compute_rsi,
          "ssa": self.compute_ssa,
          "ssb": self.compute_ssb,
          "slowk": self.compute_slowk,
          "slowd": self.compute_slowd,
          "tenkan": self.compute_tenkan,
          "trange": self.compute_trange,
          "trix": self.compute_trix,
          "typprice": self.compute_typprice,
          "ultosc": self.compute_ultosc,
          "willr": self.compute_willr,
          "wclprice": self.compute_wclprice,
        }[feature](args)

    def compute_ad(self,args):
        return talib.AD(self.klines.high, self.klines.low, self.klines.close, self.klines.volume)
        
    def compute_adosc(self,args):
        fastperiod = int(args[0])
        slowperiod = int(args[0])*int(args[1])
        return talib.ADOSC(self.klines.high, self.klines.low, self.klines.close, self.klines.volume, fastperiod=fastperiod, slowperiod=slowperiod)

    def compute_adx(self,args):
        timeperiod = int(args[0])
        return talib.ADX(self.klines.high, self.klines.low, self.klines.close, timeperiod=timeperiod)
        
    def compute_adxr(self,args):
        timeperiod = int(args[0])
        return talib.ADXR(self.klines.high, self.klines.low, self.klines.close, timeperiod=timeperiod)

    def compute_apo(self,args):
        fastperiod=int(args[0])
        slowperiod=int(fastperiod*int(args[1]))
        return talib.APO(self.klines.close, fastperiod=fastperiod, slowperiod=slowperiod, matype=0)

    def compute_aroonup(self,args):
        timeperiod = int(args[0])
        return talib.AROON(self.klines.high, self.klines.low, timeperiod=timeperiod)[1]

    def compute_aroondown(self,args):
        timeperiod = int(args[0])
        return talib.AROON(self.klines.high, self.klines.low, timeperiod=timeperiod)[0]

    def compute_aroonosc(self,args):
        timeperiod = int(args[0])
        return talib.AROONOSC(self.klines.high, self.klines.low, timeperiod=timeperiod)

    def compute_atr(self,args):
        timeperiod = int(args[0])
        return talib.ATR(self.klines.high, self.klines.low, self.klines.close, timeperiod=14)

    def compute_avgprice(self,args):
        return talib.AVGPRICE(self.klines.open, self.klines.high, self.klines.low, self.klines.close)

    def compute_bop(self,args):
        return talib.BOP(self.klines.open, self.klines.high, self.klines.low, self.klines.close)
        
    def compute_cci(self,args):
        timeperiod = int(args[0])
        return talib.CCI(self.klines.high, self.klines.low, self.klines.close, timeperiod=timeperiod)

    def compute_cdl2crows(self,args):
        return talib.CDL2CROWS(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdl3blackcrows(self,args):
        return talib.CDL3BLACKCROWS(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdl3inside(self,args):
        return talib.CDL3INSIDE(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdl3linestrike(self,args):
        return talib.CDL3LINESTRIKE(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdl3outside(self,args):
        return talib.CDL3OUTSIDE(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdl3starinsouth(self,args):
        return talib.CDL3STARSINSOUTH(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdl3whitesoldiers(self,args):
        return talib.CDL3WHITESOLDIERS(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlabandonedbaby(self,args):
        return talib.CDLABANDONEDBABY(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdladvanceblock(self,args):
        return talib.CDLADVANCEBLOCK(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlbelthold(self,args):
        return talib.CDLBELTHOLD(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlbreakaway(self,args):
        return talib.CDLBREAKAWAY(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlclosingmarubozu(self,args):
        return talib.CDLCLOSINGMARUBOZU(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlconcealbabywall(self,args):
        return talib.CDLCONCEALBABYSWALL(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlcounterattack(self,args):
        return talib.CDLCOUNTERATTACK(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdldarkcloudcover(self,args):
        return talib.CDLDARKCLOUDCOVER(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdldoji(self,args):
        return talib.CDLDOJI(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdldojistar(self,args):
        return talib.CDLDOJISTAR(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdldragonflydoji(self,args):
        return talib.CDLDRAGONFLYDOJI(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlengulfing(self,args):
        return talib.CDLENGULFING(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdleveningdojistar(self,args):
        return talib.CDLEVENINGDOJISTAR(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdleveningstar(self,args):
        return talib.CDLEVENINGSTAR(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlgapsidesidewhite(self,args):
        return talib.CDLGAPSIDESIDEWHITE(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlgravestonedoji(self,args):
        return talib.CDLGRAVESTONEDOJI(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlhammer(self,args):
        return talib.CDLHAMMER(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlhangingman(self,args):
        return talib.CDLHANGINGMAN(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlharami(self,args):
        return talib.CDLHARAMI(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlharamicross(self,args):
        return talib.CDLHARAMICROSS(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlhighwave(self,args):
        return talib.CDLHIGHWAVE(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlhikkake(self,args):
        return talib.CDLHIKKAKE(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlhikkakemod(self,args):
        return talib.CDLHIKKAKEMOD(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlhomingpigeon(self,args):
        return talib.CDLHOMINGPIGEON(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlidentical3crows(self,args):
        return talib.CDLIDENTICAL3CROWS(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlinneck(self,args):
        return talib.CDLINNECK(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlinvertedhammer(self,args):
        return talib.CDLINVERTEDHAMMER(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlkicking(self,args):
        return talib.CDLKICKING(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlkickingbylength(self,args):
        return talib.CDLKICKINGBYLENGTH(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlladderbottom(self,args):
        return talib.CDLLADDERBOTTOM(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdllongleggeddoji(self,args):
        return talib.CDLLONGLEGGEDDOJI(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdllongline(self,args):
        return talib.CDLLONGLINE(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlmarubozu(self,args):
        return talib.CDLMARUBOZU(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlmatchinglow(self,args):
        return talib.CDLMATCHINGLOW(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlmathold(self,args):
        return talib.CDLMATHOLD(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlmorningstardojistar(self,args):
        return talib.CDLMORNINGDOJISTAR(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlmorningstar(self,args):
        return talib.CDLMORNINGSTAR(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlonneck(self,args):
        return talib.CDLONNECK(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlpiercing(self,args):
        return talib.CDLPIERCING(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlrickshawman(self,args):
        return talib.CDLRICKSHAWMAN(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlrisefall3methods(self,args):
        return talib.CDLRISEFALL3METHODS(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlseparatinglines(self,args):
        return talib.CDLSEPARATINGLINES(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlshootingstar(self,args):
        return talib.CDLSHOOTINGSTAR(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlshortline(self,args):
        return talib.CDLSHORTLINE(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlspinningtop(self,args):
        return talib.CDLSPINNINGTOP(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlstalledpattern(self,args):
        return talib.CDLSTALLEDPATTERN(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlsticksandwich(self,args):
        return talib.CDLSTICKSANDWICH(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdltakuri(self,args):
        return talib.CDLTAKURI(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdltasukigap(self,args):
        return talib.CDLTASUKIGAP(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlthrusting(self,args):
        return talib.CDLTHRUSTING(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdltristar(self,args):
        return talib.CDLTRISTAR(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlunique3river(self,args):
        return talib.CDLUNIQUE3RIVER(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlupsidegap2crows(self,args):
        return talib.CDLUPSIDEGAP2CROWS(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cdlxsidegap3methods(self,args):
        return talib.CDLXSIDEGAP3METHODS(self.klines.open,self.klines.high,self.klines.low,self.klines.close)

    def compute_cmo(self,args):
        timeperiod = int(args[0])
        return talib.CMO(self.klines.close, timeperiod=timeperiod)

    def compute_dx(self,args):
        timeperiod = int(args[0])
        return talib.DX(self.klines.high, self.klines.low, self.klines.close, timeperiod=timeperiod)

    def compute_fastk(self,args):
        fastk_period=int(args[0])
        fastd_period=int(args[1])
        return talib.STOCHF(self.klines.high, self.klines.low, self.klines.close, fastk_period=fastk_period, fastd_period=fastd_period, fastd_matype=0)[0]

    def compute_fastd(self,args):
        fastk_period=int(args[0])
        fastd_period=int(args[1])
        return talib.STOCHF(self.klines.high, self.klines.low, self.klines.close, fastk_period=fastk_period, fastd_period=fastd_period, fastd_matype=0)[1]

    def compute_fastkrsi(self,args):
        timeperiod = int(args[0])
        fastk_period = int(args[1])
        fastd_period = int(args[2])
        return talib.STOCHRSI(self.klines.close, timeperiod=timeperiod, fastk_period=fastk_period, fastd_period=fastd_period, fastd_matype=0)[0]

    def compute_fastdrsi(self,args):
        timeperiod = int(args[0])
        fastk_period = int(args[1])
        fastd_period = int(args[2])
        return talib.STOCHRSI(self.klines.close, timeperiod=timeperiod, fastk_period=fastk_period, fastd_period=fastd_period, fastd_matype=0)[1]

    def compute_hcdcperiod(self,args):
        return talib.HT_DCPERIOD(self.klines.close)
        
    def compute_hcdcphase(self,args):
        return talib.HT_DCPHASE(self.klines.close)

    def compute_htphasorin(self,args):
        return talib.HT_PHASOR(self.klines.close)[0]
        
    def compute_htphasorqua(self,args):
        return talib.HT_PHASOR(self.klines.close)[1]
        
    def compute_htsinesine(self,args):
        return talib.HT_SINE(self.klines.close)[0]
        
    def compute_sinelead(self,args):
        return talib.HT_SINE(self.klines.close)[1]
        
    def compute_httrendmode(self,args):
        return talib.HT_TRENDMODE(self.klines.close)

    def compute_kijun(self,args):
        rolling = int(args[0])
        return (self.klines.high.rolling(rolling).max()+self.klines.low.rolling(rolling).min())/2

    def compute_laggingspan(self,args):
        lag = int(args[0])
        return self.klines.close.shift(lag)

    def compute_ma(self,args):
        rolling = int(args[0])
        return self.klines.close.rolling(rolling).mean()
        
    def compute_macd(self,args):
        fastperiod = int(args[0])
        slowperiod = int(fastperiod*int(args[1]))
        signalperiod = int(int(fastperiod)/int(args[1])+1)
        return talib.MACD(self.klines.close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)[0] #, fastmatype=self.matype, slowmatype=self.matype, signalmatype=self.matype)[0]

    def compute_macdhist(self,args):
        fastperiod = int(args[0])
        slowperiod = int(fastperiod*int(args[1]))
        signalperiod = int(int(fastperiod)/int(args[1])+1)
        return talib.MACD(self.klines.close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)[2] #, fastmatype=self.matype, slowmatype=self.matype, signalmatype=self.matype)[2]
        
    def compute_macdsignal(self,args):
        fastperiod = int(args[0])
        slowperiod = int(fastperiod*int(args[1]))
        signalperiod = int(int(fastperiod)/int(args[1])+1)
        return talib.MACD(self.klines.close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)[1] #, fastmatype=self.matype, slowmatype=self.matype, signalmatype=self.matype)[1]

    def compute_medprice(self,args):
        return talib.MEDPRICE(self.klines.high,self.klines.low)

    def compute_mfi(self,args):
        timeperiod = int(args[0])
        return talib.MFI(self.klines.high, self.klines.low, self.klines.close, self.klines.volume, timeperiod=timeperiod)
        
    def compute_minusdi(self,args):
        timeperiod = int(args[0])
        return talib.MINUS_DI(self.klines.high, self.klines.low, self.klines.close, timeperiod=timeperiod)

    def compute_minusdm(self,args):
        timeperiod = int(args[0])
        return talib.MINUS_DM(self.klines.high, self.klines.low, timeperiod=timeperiod)
        
    def compute_mom(self,args):
        timeperiod = int(args[0])
        return talib.MOM(self.klines.close, timeperiod=timeperiod)

    def compute_natr(self,args):
        timeperiod = int(args[0])
        return talib.ATR(self.klines.high, self.klines.low, self.klines.close, timeperiod=14)

    def compute_obv(self,args):
        return talib.OBV(self.klines.close, self.klines.volume)

    def compute_plusdi(self,args):
        timeperiod = int(args[0])
        return talib.PLUS_DI(self.klines.high, self.klines.low, self.klines.close, timeperiod=timeperiod)

    def compute_plusdm(self,args):
        timeperiod = int(args[0])
        return talib.PLUS_DM(self.klines.high, self.klines.low, timeperiod=timeperiod)

    def compute_ppo(self,args):
        fastperiod=int(args[0])
        slowperiod=int(fastperiod*int(args[1]))
        return talib.PPO(self.klines.close, fastperiod=fastperiod, slowperiod=slowperiod, matype=0)

    def compute_roc(self,args):
        timeperiod = int(args[0])
        return talib.ROC(self.klines.close, timeperiod=timeperiod)
        
    def compute_rocp(self,args):
        timeperiod = int(args[0])
        return talib.ROCP(self.klines.close, timeperiod=timeperiod)

    def compute_rocr(self,args):
        timeperiod = int(args[0])
        return talib.ROCR(self.klines.close, timeperiod=timeperiod)
        
    def compute_rsi(self,args):
        timeperiod = int(args[0])
        return talib.RSI(self.klines.close, timeperiod=timeperiod)

    def compute_ssa(self,args):
        shift = int(args[0])
        arg_tenkan = [int(shift/3)+1]
        arg_kijun = [shift]
        return ((self.compute_tenkan(arg_tenkan)+self.compute_kijun(arg_kijun)/2).shift(shift))

    def compute_ssb(self,args):
        rolling = int(args[0])
        return ((self.klines.high.rolling(rolling).max()+self.klines.low.rolling(rolling).min())/2).shift(int(rolling/2))

    def compute_slowk(self,args):
        fastk_period=int(args[0])
        slowk_period=int(fastk_period*int(args[1]))
        slowd_period=int(fastk_period*int(args[1]))
        return talib.STOCH(self.klines.high, self.klines.low, self.klines.close, fastk_period=fastk_period, slowk_period=slowk_period, slowk_matype=0, slowd_period=slowd_period, slowd_matype=0)[0]

    def compute_slowd(self,args):
        fastk_period=int(args[0])
        slowk_period=int(fastk_period*int(args[1]))
        slowd_period=int(fastk_period*int(args[1]))
        return talib.STOCH(self.klines.high, self.klines.low, self.klines.close, fastk_period=fastk_period, slowk_period=slowk_period, slowk_matype=0, slowd_period=slowd_period, slowd_matype=0)[1]

    def compute_tenkan(self,args):
        rolling = int(args[0])
        return (self.klines.high.rolling(rolling).max()+self.klines.low.rolling(rolling).min())/2

    def compute_trange(self,args):
        return talib.TRANGE(self.klines.high, self.klines.low, self.klines.close)

    def compute_trix(self,args):
        timeperiod = int(args[0])
        return talib.TRIX(self.klines.close, timeperiod=timeperiod)
        
    def compute_typprice(self,args):
        return talib.TYPPRICE(self.klines.high, self.klines.low, self.klines.close)

    def compute_ultosc(self,args):
        timeperiod1=int(args[0])
        timeperiod2=timeperiod1*int(args[1])
        timeperiod3=timeperiod1*int(args[1])*int(args[1])
        return talib.ULTOSC(self.klines.high, self.klines.low, self.klines.close, timeperiod1=timeperiod1, timeperiod2=timeperiod2, timeperiod3=timeperiod3)

    def compute_wclprice(self,args):
        return talib.WCLPRICE(self.klines.high, self.klines.low, self.klines.close)

    def compute_willr(self,args):
        timeperiod = int(args[0])
        return talib.WILLR(self.klines.high, self.klines.low, self.klines.close, timeperiod=timeperiod)