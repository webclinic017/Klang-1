#
# K-line, stock datas 
# Klang 提供了全局的股票数据，和获取股票数据的方法
# Kdatas 是提供了单只股票的数据和计算方法
# 类似通达信这样的公式，经过计算的数据有时候需要 计算整个周期，有时候是单个周期
# 因此需要封装成 python 类来解决
# 例如： if CLOSE > OPEN, 判断的是单个周期
# 例如： EVERY (CLOSE > OPEN,N) 这时候判断的是多个周期

import numpy as np
import pandas

kl = None
def setstock(kl1):
    global kl
    kl = kl1

"""
df2 = df[(df.date >= '2020-10-01') & 
             (df.date <= '2021-01-01')] 
"""

#获取股票数据
#baostock volume,TDX use vol
#

def getstockdata(name):
    if isinstance(kl.currentdf.get('df'),pandas.core.frame.DataFrame):
        return kl.currentdf['df'][name]
    return []
        
#做类似C/C[1]计算
#计算涨跌率
#C和C1都是列表，numpy计算的时候需要同样list size
def match_size(*datas_list):
    size = min(len(data) for data in datas_list)
    if size == 0:
        return np.array([]),np.array([])
    #[len-size:]
    new_list = [np.array(data[len(data)-size:]) for data in datas_list]
    return new_list


#股票数据重新定义以方便计算

class Kdatas(object):
    def __init__(self,index=0):
        self._data = []
        self.currentindex = -1 #stock code index
        self.dfstart      = -1 #stock start date
        self.dfend        = -1 #stock end date
        self.index = index     #C,C[1],C[2]


    #返回最后一天的数据
    @property
    def value(self):
        return self.dtype(self.data[-1])

    #比较currentindex值的目的是切换股票的时候刷新
    @property
    def data(self):
        if len(self._data) == 0 or self.currentindex != kl.currentindex\
            or self.dfstart != kl.dfstart\
            or self.dfend   != kl.dfend:

            #reload
            self.currentindex = kl.currentindex
            self.dfstart = kl.dfstart
            self.dfend   = kl.dfend

            d = getstockdata(self.name).astype(self.dtype)
            index = len(d) - self.index
            if index > 0:
                self._data = d[:index]
            else :
                self._data = []
        return self._data

    #C,index=0,
    #C[1],index=1
    def __getitem__(self, index):
        n = self.__class__(index)
        if len(self._data) >index:
            nindex = len(self._data) - index
            n._data = self.data[:nindex]
        else:
            raise StopIteration
        return n


    def __bool__(self):
        return bool(self.value)

    # <
    def __lt__(self, other):
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d1 < d2
            return ko
        else: #int float
            return self.value < other


    # >
    def __gt__(self, other):
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d1 > d2
            return ko
        else: #int float
            return self.value > other


    # ==
    def __eq__(self, other):
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d1 == d2
            return ko
        else: #int float
            return self.value == other


    # !=
    def __ne__(self, other):
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d1 != d2
            return ko
        else: #int float
            return self.value != other


    # >=
    def __ge__(self, other):
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d1 >= d2
            return ko
        else: #int float
            return self.value >= other


    # <= 
    def __le__(self, other):
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d1 <= d2
            return ko
        else: #int float
            return self.value <= other

       # +
    def __add__(self,other):
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d1 + d2
            return ko
        else: #int float
            return self.value + other
    # -
    def __sub__(self,other):
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d1 - d2
            return ko
        else: #int float
            return self.value - other
    # -
    def __rsub__(self,other):
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d2 - d1
            return ko
        else: #int float
            return other - self.value

    # *
    def __mul__(self,other):
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d1 * d2
            return ko
        else: #int float
            return self.value * other

    # / 
    def __truediv__(self, other):
        #s1 , s2 = match_size(self.data,other.data)
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d1 / d2
            return ko
        else:
            return self.value / other

    def __rtruediv__(self, other):
        #s1 , s2 = match_size(self.data,other.data)
        if isinstance(other,Kdatas):  
            ko = KdatasOpt()
            d1,d2 = match_size(self.data,other.data)
            ko._data = d2 / d1
            return ko
        else:
            return other / self.value


    __div__ = __truediv__
    __rdiv__ = __rtruediv__

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return str(self.value)

# 这是经过计算后的数据数组
# 例如：开盘价 > 收盘价
# if C > O ,判断是否为真的时候调用bool
# 计算 C - O  的时候 统计所有的周期 C和O的大小

class KdatasOpt(Kdatas):

    def __init__(self,index=0):
        self.index = index
        self.dtype = float

    def __bool__(self):
        return bool(self._data[-1])

    @property
    def data(self):    
        return self._data

    #返回最后一天的数据
    @property
    def value(self):
        return self.dtype(self._data[-1])


# create open high low close volume datetime
# 建立全局的 o,O,OPEN,等关键词
for name in ["open", "high", "low", "close", "volume", 'vol','amount','datetime']:
    dtype = float if name != "datetime" else np.str_
    cls = type("{}Kdatas".format(name.capitalize()), (Kdatas, ), {"name": name, "dtype": dtype})
    obj = cls()
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = obj

