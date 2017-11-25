"""
io 模块，读取数据集并做以下两个操作:
1. 时间戳转换
2. drop掉空值过多的列
"""
import numpy as np
import pandas as pd


def _convert_time(df, names):
    """
    将时间字符串转换为python内置时间类型
    :df:        pd.DataFrame
                处理的数据集对象
    :names:     List
                需要转换时间戳的列名
    :return:    pd.DataFrame
    """
    date_time_format = "%Y-%m-%d %h:%m:%s"
    for name in names:
        df[name] = pd.to_datetime(df[name], format=date_time_format)
    return df

def _drop_null(df, percent=0.5):
    """
    根据每一列的空值，也就是NaN值的数量所占比例判断这一列是否被drop掉
    :df:        pd.DataFrame
                处理的数据集对象
    :percent:   float
                一个0-1之间的数，空值所占百分比大于percent的列将被drop掉
    :return:    pd.DataFrame
    """
    drop_list = []
    for column in df.columns:
        is_null = pd.isnull(df[column])
        # null 值的数量
        null_count = len(is_null[is_null == True])
        if null_count > len(df[column]) * percent:
            drop_list.append(column)
    return df.drop(drop_list, 1)

def read_df(path):
    """
    读取数据集并返回pandas的
    :path:      str

    :return:    pd.DataFrame
    """
    df = pd.read_pickle(path)
    # df = df.loc[:, ('Receive_Time','SOBD','ARCID','CTOT','ATOT','EOBT')]
    df = _drop_null(df)
    times = ['Receive_Time','EOBT','CTOT','ATOT']
    df = _convert_time(df, times)
    return df

