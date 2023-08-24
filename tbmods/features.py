from tbmods.klines import Klines
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd
import talib

config = Config()
log = Log(config['app'])

class Features:
    
    def __init__(self,features_map,start,end,symbol,period):
        self.features_map = features_map
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)
        self.symbol = symbol
        self.period = period
        self.klines = Klines(self.symbol,self.period)
        self.klines.load_df(self.start,self.end)
        self.df = pd.DataFrame(index=self.klines.df.index)
        self.load()

    def peel_feature_map(self,feature):
        source = self.features_map['source']
        klines_args = self.features_map['features'][feature]['klines_args'] if 'klines_args' in self.features_map['features'][feature] else []
        args = self.features_map['features'][feature]['args'] if 'args' in self.features_map['features'][feature] else {}
        lag = self.features_map['features'][feature]['lag'] if 'lag' in self.features_map['features'][feature] else 0
        tuple_index = self.features_map['features'][feature]['tuple_index'] if 'tuple_index' in self.features_map['features'][feature] else -1
        return source, klines_args, args, lag, tuple_index

    def load(self):
        for feature in self.features_map['features']:
            source, klines_args, args,lag, tuple_index = self.peel_feature_map(feature)
            try:
                feature_data = getattr(self,'load_{}'.format(source))(feature,klines_args,args,lag,tuple_index)
            except Exception as e:
                log.warning("Cant compute {} {}".format(feature,e))
                continue
            while lag >= 0:
                feature_name = feature
                feature_name += "!"+"-".join(['{}={}'.format(arg,args[arg]) for arg in args]) if len(args) > 0 else ""
                feature_name += "!lag={}".format(lag)
                self.df = self.df.join(feature_data.rename(feature_name).shift(lag))
                lag -= 1
        self.df.dropna(inplace=True)
            
    def load_talib(self,feature,klines_args,args,lag,tuple_index):
        method = feature.split('-')[0]
        positionnal_args = [self.klines.df[klines_arg] for klines_arg in klines_args]
        kwargs = { arg:args[arg] for arg in args }
        talib_data = getattr(talib,method)(*positionnal_args) if tuple_index == -1 else getattr(talib,method)(*positionnal_args)[tuple_index]
        return talib_data
        
    def load_klines(self,feature,klines_args,args,lag,tuple_index):
        klines_data = self.klines.df[feature]
        return klines_data
    
    def load_ichimoku(self,feature,klines_args,args,lag,tuple_index):
        tenkan = (self.klines.df.high.rolling(args['short_period']).max()+self.klines.df.low.rolling(args['short_period']).min())/2
        kijun = (self.klines.df.high.rolling(args['middle_period']).max()+self.klines.df.low.rolling(args['middle_period']).min())/2
        ssa = ((tenkan + kijun)/2).shift(args['middle_period'])
        ssb = ((self.klines.df.high.rolling(args['long_period']).max()+self.klines.df.low.rolling(args['long_period']).min())/2).shift(args['middle_period'])
        lagging_span = self.klines.df.close.shift(args['middle_period'])
        return {
            "tenkan": tenkan,
            "kijun": kijun,
            "ssa": ssa,
            "ssb": ssb,
            "lagging_span": lagging_span
        }[feature]