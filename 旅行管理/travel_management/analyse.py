# -*- coding: utf-8 -*-
# @Author: jason-xuan
# @Date:   2017-04-24 22:22:41
# @Last Modified by:   jason-xuan
# @Last Modified time: 2017-04-24 22:43:29
import pandas as pd
from .reduce_method import reduce_CTOT
from datetime import datetime, timedelta


def analyse(dataframe):
    """
    计算三项数据指标
    """
    analysed = dataframe.groupby(['ARCID', 'SOBD']).apply(reduce_CTOT)
    analysed = analysed.dropna()
    analysed = analysed.reset_index()
    return analysed

def between(time, l, r):
    return time.hour >= l and time.hour < r

def time_gap_analyse(analysed, date):
    """
    1、安庆天柱山机场（代码ZSAQ），receive_time为2016年8月12日，将一天划分为八个时间段（0至3,3至6,6至9，以此类推），分别计算CTOT误差、CTOT跳变幅度、CTOT跳变次数，得到列表；
    :analysed:      pd.DataFrame
                    分析后的数据集
    :date:          int
                    要求的日期
    :return:        pd.DataFrame
                    根据时间段划分的结果
    """
    analysed['analyse1'] = ['other' for x in range(len(analysed))]
    analysed.loc[analysed.time_stamp.map(lambda timestamp: between(timestamp, 0 , 3 )), ('analyse1', )] = '0-3'
    analysed.loc[analysed.time_stamp.map(lambda timestamp: between(timestamp, 3 , 6 )), ('analyse1', )] = '3-6'
    analysed.loc[analysed.time_stamp.map(lambda timestamp: between(timestamp, 6 , 9 )), ('analyse1', )] = '6-9'
    analysed.loc[analysed.time_stamp.map(lambda timestamp: between(timestamp, 9 , 12)), ('analyse1', )] = '9-12'
    analysed.loc[analysed.time_stamp.map(lambda timestamp: between(timestamp, 12, 15)), ('analyse1', )] = '12-15'
    analysed.loc[analysed.time_stamp.map(lambda timestamp: between(timestamp, 15, 18)), ('analyse1', )] = '15-18'
    analysed.loc[analysed.time_stamp.map(lambda timestamp: between(timestamp, 18, 21)), ('analyse1', )] = '18-21'
    analysed.loc[analysed.time_stamp.map(lambda timestamp: between(timestamp, 21, 24)), ('analyse1', )] = '21-24'

    return analysed[analysed.SOBD == date].groupby('analyse1').mean()

def date_block_analyse(analysed):
    """
    2、安庆天柱山机场（代码ZSAQ），将一年中的receive_time分为两部分，一部分是2016年3月27日（含）至2016年10月29日（含），另一部分是剩下的日期，分别计算CTOT误差、CTOT跳变幅度、CTOT跳变次数，得到列表；
    :analysed:      pd.DataFrame
                    分析后的数据集
    :return:        pd.DataFrame
                    根据时间段划分的结果
    """
    analysed['analyse2'] = ["2016-3-27 to 2016-10-29" for x in range(len(analysed))]
    analysed.loc[analysed.time_stamp <= datetime(2016, 3, 27), ('analyse2',)] = 'other'
    analysed.loc[analysed.time_stamp >= datetime(2016, 10, 30), ('analyse2',)] = 'other'
    return analysed.groupby('analyse2').mean()

def single_day_analyse(analysed, date):
    """
    :analysed:      pd.DataFrame
                    分析后的数据集
    :date:          int
                    要求的日期
    :return:        pd.DataFrame
                    根据时间段划分的结果
    """
    return analysed[analysed.SOBD == date].mean()

def ARCTYP_analyse(analysed, date):
    """
    4、安庆天柱山机场（代码ZSAQ），receive_time为2016年8月12日，安机型（即列表中的ARCTYP，aircraft type）的不同，计算CTOT误差、CTOT跳变幅度、CTOT跳变次数，得到列表；
    :analysed:      pd.DataFrame
                    分析后的数据集
    :date:          int
                    要求的日期
    :return:        pd.DataFrame
                    根据时间段划分的结果
    """
    date = 20160503
    return analysed[analysed.SOBD == date].groupby('ARCTYP').mean()
