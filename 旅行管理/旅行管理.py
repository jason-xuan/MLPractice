
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from travel_management import read_df, analyse, time_gap_analyse, date_block_analyse, single_day_analyse, ARCTYP_analyse
from datetime import datetime, timedelta


# In[2]:

df = read_df('data.pickle')
analysed = analyse(df)


# 1、安庆天柱山机场（代码ZSAQ），receive_time为2016年8月12日，将一天划分为八个时间段（0至3,3至6,6至9，以此类推），分别计算CTOT误差、CTOT跳变幅度、CTOT跳变次数，得到列表；

# In[3]:

date = 20160503
time_gap_analyse(analysed, date)


# 2、安庆天柱山机场（代码ZSAQ），将一年中的receive_time分为两部分，一部分是2016年3月27日（含）至2016年10月29日（含），另一部分是剩下的日期，分别计算CTOT误差、CTOT跳变幅度、CTOT跳变次数，得到列表；

# In[4]:

date_block_analyse(analysed)


# 3、安庆天柱山机场（代码ZSAQ），receive_time为2016年8月12日，分别计算CTOT误差、CTOT跳变幅度、CTOT跳变次数，得到列表；

# In[5]:

date = 20160503
single_day_analyse(analysed, date)


# 4、安庆天柱山机场（代码ZSAQ），receive_time为2016年8月12日，安机型（即列表中的ARCTYP，aircraft type）的不同，计算CTOT误差、CTOT跳变幅度、CTOT跳变次数，得到列表；

# In[6]:

date = 20160503
ARCTYP_analyse(analysed, date)

