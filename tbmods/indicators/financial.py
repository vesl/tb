import pandas as pd
import talib

class Financial:

    def __init__(self,candles):
        self.candles=candles 
    
    def compute(self,feature):
        return {
          "adx": self.compute_adx,
          "adxr": self.compute_adxr,
          "apo": self.compute_apo,
          "aroonup": self.compute_aroonup,
          "aroondown": self.compute_aroondown,
          "aroonosc": self.compute_aroonosc,
          "bop": self.compute_bop,
          "cci": self.compute_cci,
          "cmo": self.compute_cmo,
          "dx": self.compute_dx,
          "fastk": self.compute_fastk,
          "fastd": self.compute_fastd,
          "fastkrsi": self.compute_fastkrsi,
          "fastdrsi": self.compute_fastdrsi,
          "kijun": self.compute_kijun,
          "ma": self.compute_ma,
          "macd": self.compute_macd,
          "macdhist": self.compute_macdhist,
          "macdsignal": self.compute_macdsignal,
          "mfi": self.compute_mfi,
          "minusdi": self.compute_minusdi,
          "minusdm": self.compute_minusdm,
          "mom": self.compute_mom,
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
          "trix": self.compute_trix,
          "ultosc": self.compute_ultosc,
          "willr": self.compute_willr,
        }[feature]()

    def compute_adx(self):
        return talib.ADX(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)
        
    def compute_adxr(self):
        return talib.ADXR(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)

    def compute_apo(self):
        return talib.APO(self.candles['close'], fastperiod=12, slowperiod=26, matype=0)

    def compute_aroonup(self):
        return talib.AROON(self.candles['high'], self.candles['low'], timeperiod=14)[1]

    def compute_aroondown(self):
        return talib.AROON(self.candles['high'], self.candles['low'], timeperiod=14)[0]
        
    def compute_aroonosc(self):
        return talib.AROONOSC(self.candles['high'], self.candles['low'], timeperiod=14)

    def compute_bop(self):
        return talib.BOP(self.candles['open'], self.candles['high'], self.candles['low'], self.candles['close'])
        
    def compute_cci(self):
        return talib.CCI(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)

    def compute_cmo(self):
        return talib.CMO(self.candles['close'], timeperiod=14)

    def compute_dx(self):
        return talib.DX(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)

    def compute_fastk(self):
        return talib.STOCHF(self.candles['high'], self.candles['low'], self.candles['close'], fastk_period=5, fastd_period=3, fastd_matype=0)[0]

    def compute_fastd(self):
        return talib.STOCHF(self.candles['high'], self.candles['low'], self.candles['close'], fastk_period=5, fastd_period=3, fastd_matype=0)[1]

    def compute_fastkrsi(self):
        return talib.STOCHRSI(self.candles['close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)[0]

    def compute_fastdrsi(self):
        return talib.STOCHRSI(self.candles['close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)[1]

    def compute_kijun(self):
        return (self.candles.high.rolling(26).max()+self.candles.low.rolling(26).min())/2

    def compute_ma(self):
        # A custom avec un argument
        return self.candles.close.rolling(12).mean()
        
    def compute_macd(self):
        return talib.MACD(self.candles['close'], fastperiod=12, slowperiod=26, signalperiod=9)[0]

    def compute_macdhist(self):
        return talib.MACD(self.candles['close'], fastperiod=12, slowperiod=26, signalperiod=9)[2]
        
    def compute_macdsignal(self):
        return talib.MACD(self.candles['close'], fastperiod=12, slowperiod=26, signalperiod=9)[1]
        
    def compute_mfi(self):
        return talib.MFI(self.candles['high'], self.candles['low'], self.candles['close'], self.candles['volume'], timeperiod=14)
        
    def compute_minusdi(self):
        return talib.MINUS_DI(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)

    def compute_minusdm(self):
        return talib.MINUS_DM(self.candles['high'], self.candles['low'], timeperiod=14)
        
    def compute_mom(self):
        return talib.MOM(self.candles['close'], timeperiod=10)

    def compute_plusdi(self):
        return talib.PLUS_DI(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)

    def compute_plusdm(self):
        return talib.PLUS_DM(self.candles['high'], self.candles['low'], timeperiod=14)

    def compute_ppo(self):
        return talib.PPO(self.candles['close'], fastperiod=12, slowperiod=26, matype=0)

    def compute_roc(self):
        return talib.ROC(self.candles['close'], timeperiod=10)
        
    def compute_rocp(self):
        return talib.ROCP(self.candles['close'], timeperiod=10)

    def compute_rocr(self):
        return talib.ROCR(self.candles['close'], timeperiod=10)
        
    def compute_rsi(self):
        return talib.RSI(self.candles['close'], timeperiod=24)

    def compute_slowk(self):
        return talib.STOCH(self.candles['high'], self.candles['low'], self.candles['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)[0]

    def compute_slowd(self):
        return talib.STOCH(self.candles['high'], self.candles['low'], self.candles['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)[1]

    def compute_trix(self):
        return talib.TRIX(self.candles['close'], timeperiod=30)

    def compute_tenkan(self):
        return (self.candles.high.rolling(9).max()+self.candles.low.rolling(9).min())/2

    def compute_ssa(self):
        return ((self.compute_tenkan()+self.compute_kijun())/2).shift(26)

    def compute_ssb(self):
        return ((self.candles.high.rolling(52).max()+self.candles.low.rolling(52).min())/2).shift(26)

    def compute_ultosc(self):
        return talib.ULTOSC(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)

    def compute_willr(self):
        return talib.WILLR(self.candles['high'], self.candles['low'], self.candles['close'], timeperiod=14)
