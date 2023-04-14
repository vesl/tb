import pandas as pd
import numpy as np

class Ichimoku:
    
    def __init__(self,klines,lag,factor):
        self.df=klines.df
        self.lag = lag
        self.short_factor=factor
        self.middle_factor=self.short_factor*3
        self.long_factor=self.middle_factor*2
        self.compute_tenkan()
        self.compute_kijun()
        self.compute_ssa()
        self.compute_ssb()
        self.compute_laggingspan()
        self.compute_ratios()
        self.compute_kumos()
        self.scale()
        self.drop_features()
        self.rename()
        
    def compute_tenkan(self):
        rolling = '{}H'.format(self.short_factor)
        tenkan = (self.df.high.rolling(rolling).max()+self.df.low.rolling(rolling).min())/2
        self.df = self.df.join(tenkan.rename('tenkan'))
    
    def compute_kijun(self):
        rolling = '{}H'.format(self.middle_factor)
        kijun = (self.df.high.rolling(rolling).max()+self.df.low.rolling(rolling).min())/2
        self.df = self.df.join(kijun.rename('kijun'))
    
    def compute_ssa(self):
        ssa = ((self.df.tenkan + self.df.kijun)/2).shift(self.middle_factor)
        self.df = self.df.join(ssa.rename('ssa'))

    def compute_ssb(self):
        rolling = '{}H'.format(self.long_factor)
        ssb = ((self.df.high.rolling(rolling).max()+self.df.low.rolling(rolling).min())/2).shift(self.middle_factor)
        self.df = self.df.join(ssb.rename('ssb'))
        
    def compute_laggingspan(self):
        laggingspan = self.df.close.shift(self.middle_factor)
        self.df = self.df.join(laggingspan.rename('laggingspan'))
        
    def compute_ratios(self):
        self.df['closetenkan'] = self.df.close / self.df.tenkan
        self.df['closekijun'] = self.df.close / self.df.kijun
        self.df['closessa'] = self.df.close / self.df.ssa
        self.df['closessb'] = self.df.close / self.df.ssb
        self.df['closelaggingspan'] = self.df.close/self.df.laggingspan
        self.df['tenkankijun'] = self.df.tenkan / self.df.kijun
        self.df['tenkanssa'] = self.df.tenkan / self.df.ssa
        self.df['tenkanssb'] = self.df.tenkan / self.df.ssb
        self.df['tenkanlaggingspan'] = self.df.tenkan / self.df.laggingspan
        self.df['kijunssa'] = self.df.kijun / self.df.ssa
        self.df['kijunssb'] = self.df.kijun / self.df.ssb
        self.df['kijunlaggingspan'] = self.df.kijun / self.df.laggingspan
        self.df['ssassb'] = self.df.ssa / self.df.ssb
        self.df['ssalaggingspan'] = self.df.ssa / self.df.laggingspan
        self.df['ssblaggingspan'] = self.df.ssb / self.df.laggingspan
            
    def compute_kumos(self):
        self.df['closeoverkumo'] = np.where((self.df.close >= self.df.ssa) & (self.df.close >= self.df.ssb),1,0)
        self.df['closeunderkumo'] = np.where((self.df.close <= self.df.ssa) & (self.df.close <= self.df.ssb),1,0)
        self.df['closeinkumo'] = np.where((self.df.closeoverkumo == 0) & (self.df.closeunderkumo == 0),1,0)
        self.df['kijunoverkumo'] = np.where((self.df.close >= self.df.ssa) & (self.df.close >= self.df.ssb),1,0)
        self.df['kijununderkumo'] = np.where((self.df.close <= self.df.ssa) & (self.df.close <= self.df.ssb),1,0)
        self.df['kijuninkumo'] = np.where((self.df.closeoverkumo == 0) & (self.df.closeunderkumo == 0),1,0)
        self.df['tenkanoverkumo'] = np.where((self.df.close >= self.df.ssa) & (self.df.close >= self.df.ssb),1,0)
        self.df['tenkanunderkumo'] = np.where((self.df.close <= self.df.ssa) & (self.df.close <= self.df.ssb),1,0)
        self.df['tenkaninkumo'] = np.where((self.df.closeoverkumo == 0) & (self.df.closeunderkumo == 0),1,0)

    def scale(self):
        self.df.open = self.df.open.pct_change()
        self.df.high = self.df.high.pct_change()
        self.df.low = self.df.low.pct_change()
        self.df.close = self.df.close.pct_change()
        self.df.volume = self.df.volume.pct_change()
        self.df.tenkan = self.df.tenkan.pct_change()
        self.df.kijun = self.df.kijun.pct_change()
        self.df.ssa = self.df.ssa.pct_change()
        self.df.ssb = self.df.ssb.pct_change()
        self.df.laggingspan = self.df.laggingspan.pct_change()

    def drop_features(self):
        self.df.drop(['close_time','volume','number_of_trades','quote_asset_volume','taker_buy_base_asset_volume','taker_buy_quote_asset_volume','ignore'],axis=1,inplace=True)
        
    def rename(self):
        rename_columns = {column:'{}-{}-{}'.format(column,self.lag,self.short_factor) for column in self.df.columns}
        self.df.rename(columns=rename_columns,inplace=True)