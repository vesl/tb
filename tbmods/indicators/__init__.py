from tbmods.candles import Candles
import pandas as pd
import talib

class Indicators:
    """
    Full indicators :
    open,high,low,close,volume,rsi,macd,macdsignal,macdhist,adx,adxr,apo,bop,aroondown,aroonup,aroonosc,cci,cmo,dx,mfi,minusdi,minusdm,mom,plusdi,
    plusdm,ppo,roc,rocp,rocr,rocr100,slowk,slowd,fastk,fastd,fastkrsi,fastdrsi,trix,ultosc,willr
    """
    def __init__(self,candles=None):
        self.candles=candles 
        
    def candles_from_questdb(self,timescale,from_date,to_date):
        candles = Candles()
        qdbr = candles.from_questdb(timescale,from_date,to_date)
        if 'error' in qdbr: return qdbr
        self.candles = candles.candles
        return qdbr
    
    def load_indicator(self,feature):
        switch = {
            'rsi':self.compute_rsi,
            'macd':self.compute_macd,
            'adx':self.compute_adx,
            'adxr':self.compute_adxr,
            'apo':self.compute_apo,
            'aroonup':self.compute_aroon,
            'aroondown':self.compute_aroon,
            'aroonosc':self.compute_aroonosc,
            'bop':self.compute_bop,
            'cci':self.compute_cci,
            'cmo':self.compute_cmo,
            'dx':self.compute_dx,
            'macd':self.compute_macd,
            'macdsignal':self.compute_macd,
            'macdhist':self.compute_macd,
            'mfi':self.compute_mfi,
            'minusdi':self.compute_minusdi,
            'minusdm':self.compute_minusdm,
            'mom':self.compute_mom,
            'plusdi':self.compute_plusdi,
            'plusdm':self.compute_plusdm,
            'ppo':self.compute_ppo,
            'roc':self.compute_roc,
            'rocp':self.compute_rocp,
            'rocr':self.compute_rocr,
            'slowk':self.compute_stoch,
            'slowd':self.compute_stoch,
            'fastk':self.compute_stochf,
            'fastd':self.compute_stochf,
            'fastkrsi': self.compute_stochrsi,
            'fastdrsi': self.compute_stochrsi,
            'ultosc':self.compute_ultosc,
            'willr':self.compute_willr,
            'ichtenkan':self.compute_ichimoku,
            'ichkijun':self.compute_ichimoku,
            'ichssa':self.compute_ichimoku,
            'ichssb':self.compute_ichimoku,
            'ichlag':self.compute_ichimoku,
        }
        return switch[feature]()

    def compute_rsi(self):
        rsi = talib.RSI(self.candles['close'], timeperiod=14)
        self.candles = self.candles.join(rsi.rename('rsi'))
        self.candles.dropna(inplace=True)
        return ('rsi' in self.candles.columns)

    def compute_macd(self):
        macd,macdsignal,macdhist = talib.MACD(self.candles['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        self.candles = self.candles.join([macd.rename('macd'),macdsignal.rename('macdsignal'),macdhist.rename('macdhist')])
        self.candles.dropna(inplace=True)
        return ('macd' in self.candles.columns)

    def compute_adx(self):
        adx = talib.ADX(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)
        self.candles = self.candles.join(adx.rename('adx'))
        self.candles.dropna(inplace=True)
        return ('adx' in self.candles.columns)

    def compute_adxr(self):
        adxr = talib.ADXR(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)
        self.candles = self.candles.join(adxr.rename('adxr'))
        self.candles.dropna(inplace=True)
        return ('adxr' in self.candles.columns)

    def compute_apo(self):
        apo = talib.APO(self.candles['close'], fastperiod=12, slowperiod=26, matype=0)
        self.candles = self.candles.join(apo.rename('apo'))
        self.candles.dropna(inplace=True)
        return ('apo' in self.candles.columns)

    def compute_aroon(self):
        aroondown, aroonup = talib.AROON(self.candles['high'], self.candles['low'], timeperiod=14)
        self.candles = self.candles.join(aroondown.rename('aroondown'))
        self.candles = self.candles.join(aroonup.rename('aroonup'))
        self.candles.dropna(inplace=True)
        return ('aroondown' in self.candles.columns)

    def compute_aroonosc(self):
        aroonosc = talib.AROONOSC(self.candles['high'], self.candles['low'], timeperiod=14)
        self.candles = self.candles.join(aroonosc.rename('aroonosc'))
        self.candles.dropna(inplace=True)
        return ('aroonosc' in self.candles.columns)

    def compute_bop(self):
        bop = talib.BOP(self.candles['open'], self.candles['high'], self.candles['low'], self.candles['close'])
        self.candles = self.candles.join(bop.rename('bop'))
        self.candles.dropna(inplace=True)
        return ('bop' in self.candles.columns)

    def compute_cci(self):
        cci = talib.CCI(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)
        self.candles = self.candles.join(cci.rename('cci'))
        self.candles.dropna(inplace=True)
        return ('cci' in self.candles.columns)

    def compute_cmo(self):
        cmo = talib.CMO(self.candles['close'], timeperiod=14)
        self.candles = self.candles.join(cmo.rename('cmo'))
        self.candles.dropna(inplace=True)
        return ('cmo' in self.candles.columns)

    def compute_dx(self):
        dx = talib.DX(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)
        self.candles = self.candles.join(dx.rename('dx'))
        self.candles.dropna(inplace=True)
        return ('dx' in self.candles.columns)

    def compute_mfi(self):
        mfi = talib.MFI(self.candles['high'], self.candles['low'], self.candles['close'], self.candles['volume'], timeperiod=14)
        self.candles = self.candles.join(mfi.rename('mfi'))
        self.candles.dropna(inplace=True)
        return ('mfi' in self.candles.columns)

    def compute_minusdi(self):
        minusdi = talib.MINUS_DI(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)
        self.candles = self.candles.join(minusdi.rename('minusdi'))
        self.candles.dropna(inplace=True)
        return ('minusdi' in self.candles.columns)

    def compute_minusdm(self):
        minusdm = talib.MINUS_DM(self.candles['high'], self.candles['low'], timeperiod=14)
        self.candles = self.candles.join(minusdm.rename('minusdm'))
        self.candles.dropna(inplace=True)
        return ('minusdm' in self.candles.columns)

    def compute_mom(self):
        mom = talib.MOM(self.candles['close'], timeperiod=10)
        self.candles = self.candles.join(mom.rename('mom'))
        self.candles.dropna(inplace=True)
        return ('mom' in self.candles.columns)

    def compute_plusdi(self):
        plusdi = talib.PLUS_DI(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)
        self.candles = self.candles.join(plusdi.rename('plusdi'))
        self.candles.dropna(inplace=True)
        return ('plusdi' in self.candles.columns)

    def compute_plusdm(self):
        plusdm = talib.PLUS_DM(self.candles['high'], self.candles['low'], timeperiod=14)
        self.candles = self.candles.join(plusdm.rename('plusdm'))
        self.candles.dropna(inplace=True)
        return ('plusdm' in self.candles.columns)

    def compute_ppo(self):
        ppo = talib.PPO(self.candles['close'], fastperiod=12, slowperiod=26, matype=0)
        self.candles = self.candles.join(ppo.rename('ppo'))
        self.candles.dropna(inplace=True)
        return ('ppo' in self.candles.columns)

    def compute_roc(self):
        roc = talib.ROC(self.candles['close'], timeperiod=10)
        self.candles = self.candles.join(roc.rename('roc'))
        self.candles.dropna(inplace=True)
        return ('roc' in self.candles.columns)

    def compute_rocp(self):
        rocp = talib.ROCP(self.candles['close'], timeperiod=10)
        self.candles = self.candles.join(rocp.rename('rocp'))
        self.candles.dropna(inplace=True)
        return ('rocp' in self.candles.columns)

    def compute_rocr(self):
        rocr = talib.ROCR(self.candles['close'], timeperiod=10)
        self.candles = self.candles.join(rocr.rename('rocr'))
        self.candles.dropna(inplace=True)
        return ('rocr' in self.candles.columns)

    def compute_stoch(self):
        slowk, slowd = talib.STOCH(self.candles['high'], self.candles['low'], self.candles['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        self.candles = self.candles.join(slowk.rename('slowk'))
        self.candles = self.candles.join(slowd.rename('slowd'))
        self.candles.dropna(inplace=True)
        return ('slowk' in self.candles.columns)

    def compute_stochf(self):
        fastk,fastd = talib.STOCHF(self.candles['high'], self.candles['low'], self.candles['close'], fastk_period=5, fastd_period=3, fastd_matype=0)
        self.candles = self.candles.join(fastk.rename('fastk'))
        self.candles = self.candles.join(fastd.rename('fastd'))
        self.candles.dropna(inplace=True)
        return ('fastk' in self.candles.columns)

    def compute_stochrsi(self):
        fastkrsi, fastdrsi = talib.STOCHRSI(self.candles['close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        self.candles = self.candles.join(fastkrsi.rename('fastkrsi'))
        self.candles = self.candles.join(fastdrsi.rename('fastdrsi'))
        self.candles.dropna(inplace=True)
        return ('fastkrsi' in self.candles.columns)

    def compute_ultosc(self):
        ultosc = talib.ULTOSC(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)
        self.candles = self.candles.join(ultosc.rename('ultosc'))
        self.candles.dropna(inplace=True)
        return ('ultosc' in self.candles.columns)

    def compute_willr(self):
        willr = talib.WILLR(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)
        self.candles = self.candles.join(willr.rename('willr'))
        self.candles.dropna(inplace=True)
        return ('willr' in self.candles.columns)

    def compute_ichimoku(self):
        self.candles["ichtenkan"] = (self.candles.high.rolling(9).max()+self.candles.low.rolling(9).min())/2
        self.candles["ichkijun"] = (self.candles.high.rolling(26).max()+self.candles.low.rolling(26).min())/2
        self.candles["ichssa"] = ((self.candles.ichtenkan+self.candles.ichkijun)/2).shift(26)
        self.candles["ichssb"] = ((self.candles.high.rolling(52).max()+self.candles.low.rolling(52).min())/2).shift(26)
        # Disable lagging span because of nans
        #self.candles["ichlag"] = self.candles.close.shift(-26)
        self.candles.dropna(inplace=True)
        return ('ichtenkan' in self.candles.columns)