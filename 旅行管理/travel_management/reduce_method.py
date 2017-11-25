"""
规约操作,计算一组数据的：
1.CTOT误差
2.CTOT跳变幅度
3.CTOT跳变次数
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

bad_time = datetime.strptime('1990-01-01 08:00:00', "%Y-%m-%d %H:%M:%S")


def set_null(temp_df):
    """
    将默认插值置空，避免干扰
    """
    temp_df.loc[temp_df.ATOT == bad_time, ('ATOT',)] = None
    temp_df.loc[temp_df.CTOT == bad_time, ('CTOT',)] = None
    temp_df.loc[temp_df.EOBT == bad_time, ('EOBT',)] = None
    return temp_df

def time_to_min(time):
    if time < timedelta(0):
        return (-time).seconds/60
    else:
        return time.seconds/60

def CTOT_dif(temp_df):
    """
    CTOT误差
    """
    # 将插值置空之后，剩下的ATOT值相同，min()还是max()无所谓
    ATOT = temp_df.ATOT.min()
    min_CTOT = temp_df.CTOT.min()
    # 意味着它是 NaN
    if isinstance(min_CTOT, float) or isinstance(ATOT, float):
        return np.nan

    diff = ATOT - min_CTOT

    return time_to_min(diff)

def CTOT_jump_rate(temp_df):
    """
    CTOT跳变幅度
    """
    EOBT = temp_df.EOBT.min()
    # EOBT 的值为NaN
    if isinstance(EOBT, float) or isinstance(EOBT, float):
        return np.nan
    start_time = EOBT - timedelta(0, 40 * 60)
    # 过滤出在EOBT40分钟前的CTOT
    temp_df = temp_df.loc[temp_df.CTOT >= start_time, :]

    if len(temp_df) == 0:
        return np.nan

    max_CTOT = temp_df.CTOT.max()
    min_CTOT = temp_df.CTOT.min()

    if isinstance(max_CTOT, float) or isinstance(min_CTOT, float):
        return np.nan

    jump_rate = max_CTOT - min_CTOT

    return time_to_min(jump_rate)

def CTOT_jump_count(temp_df):
    """
    CTOT跳变次数
    """
    EOBT = temp_df.EOBT.min()
    if isinstance(EOBT, float):
        return np.nan

    start_time = EOBT - timedelta(0, 40 * 60)
    temp_df = temp_df.loc[temp_df.CTOT >= start_time, :]
    if len(temp_df) <= 1:
        return np.nan
    jump_count = 0

    sortedCTOT = temp_df.sort_values(['Receive_Time']).CTOT
    sortedCTOT = sortedCTOT.reset_index(drop=True)
    for i in range(1, len(sortedCTOT)):
        diff_timedelta = sortedCTOT[i] - sortedCTOT[i-1]
        if diff_timedelta >= timedelta(0, 5 * 60) or diff_timedelta <= timedelta(0, -5 * 60):
            jump_count += 1
    return jump_count

def reduce_CTOT(group):
    try:
        group = set_null(group)
        return pd.DataFrame({
                'Area' :        [set(group.Area).pop()],
                'ARCTYP' :      [set(group.ARCTYP).pop()],
                'AP_ICAO_Code': [set(group.AP_ICAO_Code).pop()],
                'time_stamp' :  [group.ATOT.min()],
                'dif':          [CTOT_dif(group)],
                'jump_rate' :   [CTOT_jump_rate(group)],
                'jump_count' :  [CTOT_jump_count(group)],
            })
    except BaseException as e:
        print(group.ARCID.min(), group.SOBD.min())
        print(e)
        raise e
