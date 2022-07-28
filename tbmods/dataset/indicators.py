from tbmods.candles import Candles
import pandas as pd
import talib

class Indicators:
    """
    Full indicators :
    open,high,low,close,volume,rsi,macd,macdsignal,macdhist,adx,adxr,apo,bop,aroondown,aroonup,aroonosc,cci,cmo,dx,mfi,minusdi,minusdm,mom,plusdi,
    plusdm,ppo,roc,rocp,rocr,rocr100,slowk,slowd,fastk,fastd,fastkrsi,fastdrsi,trix,ultosc,willr
    """
    
    def __init__(self,candles):
        self.candles = candles
    
    def load(self,feature):
        switch = {
            'rsi':self.compute_rsi,
            'adx':self.compute_adx,
            'adxr':self.compute_adxr,
            'apo':self.compute_apo,
            'aroonup':self.compute_aroonup,
            'aroondown':self.compute_aroondown,
            'aroonosc':self.compute_aroonosc,
            'bop':self.compute_bop,
            'cci':self.compute_cci,
            'cmo':self.compute_cmo,
            'dx':self.compute_dx,
            'macd':self.compute_macd,
            'macdsignal':self.compute_macdsignal,
            'macdhist':self.compute_macdhist,
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
            'slowk':self.compute_slowk,
            'slowd':self.compute_slowd,
            'fastk':self.compute_fastk,
            'fastd':self.compute_fastd,
            'fastkrsi': self.compute_fastkrsi,
            'fastdrsi': self.compute_fastdrsi,
            'trix': self.compute_trix,
            'ultosc':self.compute_ultosc,
            'willr':self.compute_willr,
            'tenkan':self.compute_tenkan,
            'kijun':self.compute_kijun,
            'ssa':self.compute_ssa,
            'ssb':self.compute_ssb
        }
        return switch[feature]()

    def compute_rsi(self):
        rsi = talib.RSI(self.candles['close'], timeperiod=24)
        self.candles = self.candles.join(rsi.rename('rsi'))
        self.candles.dropna(inplace=True)
        return ('rsi' in self.candles.columns)

    def compute_macd(self):
        macd,macdsignal,macdhist = talib.MACD(self.candles['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        self.candles = self.candles.join(macd.rename('macd'))
        self.candles.dropna(inplace=True)
        return ('macd' in self.candles.columns)
    
    def compute_macdsignal(self):
        macd,macdsignal,macdhist = talib.MACD(self.candles['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        self.candles = self.candles.join(macdsignal.rename('macdsignal'))
        self.candles.dropna(inplace=True)
        return ('macdsignal' in self.candles.columns)

    def compute_macdhist(self):
        macd,macdsignal,macdhist = talib.MACD(self.candles['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        self.candles = self.candles.join(macdhist.rename('macdhist'))
        self.candles.dropna(inplace=True)
        return ('macdhist' in self.candles.columns)

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

    def compute_aroonup(self):
        aroondown, aroonup = talib.AROON(self.candles['high'], self.candles['low'], timeperiod=14)
        self.candles = self.candles.join(aroonup.rename('aroonup'))
        self.candles.dropna(inplace=True)
        return ('aroonup' in self.candles.columns)

    def compute_aroondown(self):
        aroondown, aroonup = talib.AROON(self.candles['high'], self.candles['low'], timeperiod=14)
        self.candles = self.candles.join(aroondown.rename('aroondown'))
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

    def compute_slowk(self):
        slowk, slowd = talib.STOCH(self.candles['high'], self.candles['low'], self.candles['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        self.candles = self.candles.join(slowk.rename('slowk'))
        self.candles.dropna(inplace=True)
        return ('slowk' in self.candles.columns)

    def compute_slowd(self):
        slowk, slowd = talib.STOCH(self.candles['high'], self.candles['low'], self.candles['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        self.candles = self.candles.join(slowk.rename('slowd'))
        self.candles.dropna(inplace=True)
        return ('slowd' in self.candles.columns)

    def compute_fastk(self):
        fastk,fastd = talib.STOCHF(self.candles['high'], self.candles['low'], self.candles['close'], fastk_period=5, fastd_period=3, fastd_matype=0)
        self.candles = self.candles.join(fastk.rename('fastk'))
        self.candles.dropna(inplace=True)
        return ('fastk' in self.candles.columns)

    def compute_fastd(self):
        fastk,fastd = talib.STOCHF(self.candles['high'], self.candles['low'], self.candles['close'], fastk_period=5, fastd_period=3, fastd_matype=0)
        self.candles = self.candles.join(fastd.rename('fastd'))
        self.candles.dropna(inplace=True)
        return ('fastd' in self.candles.columns)

    def compute_fastkrsi(self):
        fastkrsi, fastdrsi = talib.STOCHRSI(self.candles['close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        self.candles = self.candles.join(fastkrsi.rename('fastkrsi'))
        self.candles.dropna(inplace=True)
        return ('fastkrsi' in self.candles.columns)

    def compute_fastdrsi(self):
        fastkrsi, fastdrsi = talib.STOCHRSI(self.candles['close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        self.candles = self.candles.join(fastdrsi.rename('fastdrsi'))
        self.candles.dropna(inplace=True)
        return ('fastdrsi' in self.candles.columns)

    def compute_trix(self):
        trix = talib.TRIX(self.candles['close'], timeperiod=30)
        self.candles = self.candles.join(trix.rename('trix'))
        self.candles.dropna(inplace=True)
        return ('trix' in self.candles.columns)

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

    def compute_tenkan(self):
        self.candles["tenkan"] = (self.candles.high.rolling(9).max()+self.candles.low.rolling(9).min())/2
        self.candles.dropna(inplace=True)
        return ('tenkan' in self.candles.columns)
        
    def compute_kijun(self):
        self.candles["kijun"] = (self.candles.high.rolling(26).max()+self.candles.low.rolling(26).min())/2
        self.candles.dropna(inplace=True)
        return ('kijun' in self.candles.columns)
        
    def compute_ssa(self):
        self.compute_kijun()
        self.compute_tenkan()
        self.candles["ssa"] = ((self.candles.tenkan+self.candles.kijun)/2).shift(26)
        self.candles.dropna(inplace=True)
        return ('ssa' in self.candles.columns)

    def compute_ssb(self):
        self.candles["ssb"] = ((self.candles.high.rolling(52).max()+self.candles.low.rolling(52).min())/2).shift(26)
        self.candles.dropna(inplace=True)
        return ('ssb' in self.candles.columns)