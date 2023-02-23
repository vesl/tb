import pandas as pd
import talib

class Financial:

    def __init__(self,klines):
        self.klines=klines
    
    def compute(self,feature,args):
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
        }[feature](args)

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

    def compute_bop(self,args):
        return talib.BOP(self.klines.open, self.klines.high, self.klines.low, self.klines.close)
        
    def compute_cci(self,args):
        timeperiod = int(args[0])
        return talib.CCI(self.klines.high, self.klines.low, self.klines.close, timeperiod=timeperiod)

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

    def compute_kijun(self,args):
        rolling = int(args[0])
        return (self.klines.high.rolling(rolling).max()+self.klines.low.rolling(rolling).min())/2

    def compute_ma(self,args):
        rolling = int(args[0])
        return self.klines.close.rolling(rolling).mean()
        
    def compute_macd(self,args):
        fastperiod = int(args[0])
        slowperiod = int(fastperiod*int(args[1]))
        signalperiod = int(int(fastperiod)/int(args[1])+1)
        return talib.MACD(self.klines.close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)[0]

    def compute_macdhist(self,args):
        fastperiod = int(args[0])
        slowperiod = int(fastperiod*int(args[1]))
        signalperiod = int(int(fastperiod)/int(args[1])+1)
        return talib.MACD(self.klines.close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)[2]
        
    def compute_macdsignal(self,args):
        fastperiod = int(args[0])
        slowperiod = int(fastperiod*int(args[1]))
        signalperiod = int(int(fastperiod)/int(args[1])+1)
        return talib.MACD(self.klines.close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)[1]
        
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

    def compute_trix(self,args):
        timeperiod = int(args[0])
        return talib.TRIX(self.klines.close, timeperiod=timeperiod)

    def compute_ultosc(self,args):
        timeperiod1=int(args[0])
        timeperiod2=timeperiod1*int(args[1])
        timeperiod3=timeperiod1*int(args[1])*int(args[1])
        return talib.ULTOSC(self.klines.high, self.klines.low, self.klines.close, timeperiod1=timeperiod1, timeperiod2=timeperiod2, timeperiod3=timeperiod3)

    def compute_willr(self,args):
        timeperiod = int(args[0])
        return talib.WILLR(self.klines.high, self.klines.low, self.klines.close, timeperiod=timeperiod)