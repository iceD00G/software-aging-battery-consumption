import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.stattools import adfuller

import pymannkendall as mk

from scipy.stats import pearsonr
from scipy.stats import kstest
from scipy.stats import spearmanr
from scipy.stats import pointbiserialr

import statistics
import sys

from pandas.plotting import register_matplotlib_converters

folder = sys.argv[1]
process_name = sys.argv[2]

W = 50   # window size

file_name = "C:/Users/pedro/Desktop/TESE/"+folder+"/data.xlsx"
aux_file = "C:/Users/pedro/Desktop/TESE/"+folder+"/trends_"+str(W)+"_5.xlsx"


with pd.ExcelFile(file_name) as file:
    df = file.parse('Clean Data')

df['consumption'] = df['consumption_diff']
df['timestamps'] = pd.to_datetime(df['timestamps'], format='%d-%m-%Y %H:%M:%S')
df['timestamps'] = pd.to_numeric(df['timestamps'])

# Initialize constants
C = 0.95   # confidence level
k = 5   # number of consecutive times
current_k = 0
num_kpis = 9
num_samples = len(df)

# Initialize data structures
kpi_values = np.zeros((num_kpis, num_samples))
mki_j = np.zeros((num_kpis, num_samples - W))
slopei_j = np.zeros((num_kpis+1, num_samples - W))

for j in range(1, num_kpis+1):
    #print(f'--------------- {j} ---------------')
    current_k = 0
    # Apply the Mann-Kendall test to each KPI
    for t in range(num_samples):
        # Check if the sliding window is full
        if t >= W:
            window = df.iloc[t-W+1:t+1, j]
            trend, h, p, z, Tau, s, var_s, slope, intercept = mk.original_test(window)
            mki_j[j-1, t-W] = h
            if j==9:
                if h == 0:
                    slopei_j[j-1, t-W] = 0
                else:
                    slopei_j[j-1, t-W] = slope
                slopei_j[j, t-W] = statistics.mean(window)
            else:
                if h == 0:
                    slopei_j[j-1, t-W] = 0
                else:
                    slopei_j[j-1, t-W] = slope
                
            '''
            if j in [1,2,5,6,7,8,9]:
                if trend == "increasing":
                    current_k += 1
                    #if current_k >= 5:
                        #print("5+ consecutive")
                else:
                    current_k = 0
            elif j in [3,4]:
                if trend == "decreasing":
                    current_k += 1
                    #if current_k >= 5:
                        #print("5+ consecutive")
                else:
                    current_k = 0
            '''
            
            #slopei_j[j-1, t-W] = slope
            


print(slopei_j)

df1=pd.DataFrame(mki_j.transpose(), columns=['system_server_PSS','free_RAM','cached_RAM','lost_RAM','zram_used','total_PSS','system_server_gc_total_time','system_server_gc_pause_time','consumption'])
df1.index.name="window"
df2=pd.DataFrame(slopei_j.transpose(), columns=['system_server_PSS','free_RAM','cached_RAM','lost_RAM','zram_used','total_PSS','system_server_gc_total_time','system_server_gc_pause_time','consumption_trend','consumption_mean'])
df2.index.name="window"

df3 = df2.copy()

df3['system_server_PSS']=df3['system_server_PSS'].apply(lambda x: 1 if x > 0 else 0)                     #0                   
df3['free_RAM']=df3['free_RAM'].apply(lambda x: 1 if x < 0 else 0)                                       #1
df3['cached_RAM']=df3['cached_RAM'].apply(lambda x: 1 if x > 0 else 0)                                   #2
df3['lost_RAM']=df3['lost_RAM'].apply(lambda x: 1 if x > 0 else 0)                                       #3
df3['zram_used']=df3['zram_used'].apply(lambda x: 1 if x > 0 else 0)                                     #4
df3['total_PSS']=df3['total_PSS'].apply(lambda x: 1 if x > 0 else 0)                                     #5
df3['system_server_gc_total_time']=df3['system_server_gc_total_time'].apply(lambda x: 1 if x > 0 else 0) #6
df3['system_server_gc_pause_time']=df3['system_server_gc_pause_time'].apply(lambda x: 1 if x > 0 else 0) #7
#df3['consumption']=df3['consumption'].apply(lambda x: 1 if x > 0 else 0)                                 #8
#df3['consumption_negative']=df3['consumption'].apply(lambda x: -1 if x < 0 else 0)   

df3['aging1'] = [0]*len(df3)
df3['aging2'] = [0]*len(df3)
df3['aging3'] = [0]*len(df3)
df3['aging4'] = [0]*len(df3)
#print(df3)

df4 = df3.copy()



#[['system_server_PSS', 'system_server_gc_total_time', 'system_server_gc_pause_time', 'free_RAM', 'cached_RAM', 'lost_RAM']]


# Create a new column 'AllOnes' with value 1 if rolling window is all ones, else 0

#================================= Window 5 ======================================

df3['aging1'] =     ((df3['system_server_PSS'].rolling(window=5, min_periods=5).sum() == 5) &
                    (df3['system_server_gc_total_time'].rolling(window=5, min_periods=5).sum() == 5)).astype(int)

df3['aging2'] =     ((df3['system_server_PSS'].rolling(window=5, min_periods=5).sum() == 5) &
                    (df3['system_server_gc_pause_time'].rolling(window=5, min_periods=5).sum() == 5)).astype(int)

df3['aging3'] = df3['system_server_PSS'].rolling(window=5, min_periods=5).apply(lambda x: 1 if x.all() else 0, raw=True)

df3['aging4'] =    ((df3['free_RAM'].rolling(window=5, min_periods=5).sum() == 5) &
                    (df3['cached_RAM'].rolling(window=5, min_periods=5).sum() == 5) &
                    (df3['lost_RAM'].rolling(window=5, min_periods=5).sum() == 5)).astype(int)

df3['aging_global'] = df3[['aging1', 'aging2', 'aging3', 'aging4']].sum(axis=1)

df3['aging_global_1'] = df3['aging_global'].apply(lambda x: 1 if x >= 1 else 0)

df3['aging_global_2'] = df3['aging_global'].apply(lambda x: 1 if x >= 2 else 0)

df3['aging_global_3'] = df3['aging_global'].apply(lambda x: 1 if x >= 3 else 0)

df3['aging_global_4'] = df3['aging_global'].apply(lambda x: 1 if x >= 4 else 0)





#================================= Window 10 ======================================

df4['aging1'] = (   (df4['system_server_PSS'].rolling(window=10, min_periods=10).sum() == 10) &
                    (df4['system_server_gc_total_time'].rolling(window=10, min_periods=10).sum() == 10)).astype(int)

df4['aging2'] = (   (df4['system_server_PSS'].rolling(window=10, min_periods=10).sum() == 10) &
                    (df4['system_server_gc_pause_time'].rolling(window=10, min_periods=10).sum() == 10)).astype(int)

df4['aging3'] = df4['system_server_PSS'].rolling(window=10, min_periods=10).apply(lambda x: 1 if x.all() else 0, raw=True)

df4['aging4'] = (   (df4['free_RAM'].rolling(window=10, min_periods=10).sum() == 10) &
                    (df4['cached_RAM'].rolling(window=10, min_periods=10).sum() == 10) &
                    (df4['lost_RAM'].rolling(window=10, min_periods=10).sum() == 10)).astype(int)

df4['aging_global'] = df4[['aging1', 'aging2', 'aging3', 'aging4']].sum(axis=1)

df4['aging_global_1'] = df4['aging_global'].apply(lambda x: 1 if x >= 1 else 0)

df4['aging_global_2'] = df4['aging_global'].apply(lambda x: 1 if x >= 2 else 0)

df4['aging_global_3'] = df4['aging_global'].apply(lambda x: 1 if x >= 3 else 0)

df4['aging_global_4'] = df4['aging_global'].apply(lambda x: 1 if x >= 4 else 0)

df8 = pd.DataFrame(np.array([df3['consumption_trend'].values, df3['consumption_mean'].values ,df3['aging_global'].values, df3['aging_global_1'].values, df3['aging_global_2'].values, df3['aging_global_3'].values, df3['aging_global_4'].values]).transpose(), columns=['consumption trend','consumption mean', 'aging 5 (normal)','aging 5 (1 combinations)', 'aging 5 (2 combinations)', 'aging 5 (3 combinations)', 'aging 5 (4 combinations)'])

df9 = pd.DataFrame(np.array([df4['consumption_trend'].values, df4['consumption_mean'].values, df4['aging_global'].values, df4['aging_global_1'].values, df4['aging_global_2'].values, df4['aging_global_3'].values, df4['aging_global_4'].values]).transpose(), columns=['consumption trend', 'consumption mean', 'aging 10 (normal)','aging 10 (1 combinations)', 'aging 10 (2 combinations)', 'aging 10 (3 combinations)', 'aging 10 (4 combinations)'])
#rolling_window = df3.rolling(window=5)
#df3['aging'] = rolling_window.apply(lambda x: x['aging'] + 1 if all(x['system_server_PSS'] == 1) and all(x['system_server_gc_total_time'] == 1) else x['aging'])
#df3['aging'] = rolling_window.apply(lambda x: x['aging'] + 1 if all(x['system_server_PSS'] == 1) and all(x['system_server_gc_pause_time'] == 1) else x['aging'])
#df3['aging'] = rolling_window.apply(lambda x: x['aging'] + 1 if all(x['system_server_PSS'] == 1) else x['aging'])
#df3['aging'] = rolling_window.apply(lambda x: x['aging'] + 1 if all(x['free_RAM'] == 1) and all(x['cached_RAM'] == 1) and all(x['lost_RAM'] == 1) else x['aging'])


with pd.ExcelWriter(aux_file, engine='xlsxwriter') as writer:
    df1.to_excel(writer, sheet_name='Trends')
    df2.to_excel(writer, sheet_name='Slopes')
    df3.to_excel(writer, sheet_name='Aging 5')
    df4.to_excel(writer, sheet_name='Aging 10')

    df8.to_excel(writer, sheet_name='Short 5')
    df9.to_excel(writer, sheet_name='Short 10')
    
    writer.sheets['Trends'].set_column(0, 9, 20)
    writer.sheets['Slopes'].set_column(0, 10, 20)
    writer.sheets['Aging 5'].set_column(0, 19, 20)
    writer.sheets['Aging 10'].set_column(0, 19, 20)

    writer.sheets['Short 5'].set_column(0, 7, 30)
    writer.sheets['Short 10'].set_column(0, 7, 30)
        
    workbook = writer.book
    
    red_bg_format = workbook.add_format({'bg_color': '#FF0000'})
    green_bg_format = workbook.add_format({'bg_color': '#00FF00'})
    
    neg_cond = {'type': 'cell', 'criteria': '<', 'value': 0, 'format': red_bg_format}
    pos_cond = {'type': 'cell', 'criteria': '>', 'value': 0, 'format': green_bg_format}
        
    writer.sheets['Slopes'].conditional_format('B2:Z2000',neg_cond)
    writer.sheets['Slopes'].conditional_format('B2:Z2000',pos_cond)
        
    writer.sheets['Aging 5'].conditional_format('B2:K2000',pos_cond)
    writer.sheets['Aging 5'].conditional_format('P2:T2000',pos_cond)
    
    writer.sheets['Aging 10'].conditional_format('B2:K2000',pos_cond)
    writer.sheets['Aging 10'].conditional_format('P2:T2000',pos_cond)
    
    """ writer.sheets['Aging Min 2'].conditional_format('B2:J2000',pos_cond)
    
    writer.sheets['Aging Min 2'].conditional_format('O2:O2000',pos_cond)
    
    writer.sheets['Aging Min 3'].conditional_format('B2:J2000',pos_cond)
    
    writer.sheets['Aging Min 3'].conditional_format('O2:O2000',pos_cond)
    
    writer.sheets['Aging Min 4'].conditional_format('B2:J2000',pos_cond)
    
    writer.sheets['Aging Min 4'].conditional_format('O2:O2000',pos_cond) """
    
    writer.sheets['Short 5'].conditional_format('B2:H2000',pos_cond)
    writer.sheets['Short 5'].conditional_format('B2:H2000',neg_cond)
    
    writer.sheets['Short 10'].conditional_format('B2:H2000',pos_cond)
    writer.sheets['Short 10'].conditional_format('B2:H2000',neg_cond)
'''

1 - system server PSS +
2 - free RAM -
3 - cached RAM -
4 - lost RAM +
5 - zRAM used +?
6 - total PSS +
7 - consumption (+) 

system server PSS and Launch Time VERY HIGH
system server PSS and GC Paused or Total Time VERY HIGH
Launch Time HIGH
system server PSS HIGH
Free Memory, Cached Memory, Lost RAM MEDIUM
Used PSS, ZRAMinSWAP, ZRAMPhysicalUsed MEDIUM
systemui, huawei.systemManager GC Paused/Total
Time LOW
One of KSM-*, Used slab, Used buffers LOW
One of systemui, surfaceflinger, mediaserver PSS VERY LOW

'''