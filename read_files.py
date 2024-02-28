import re
import numpy as np
import os
import pandas as pd
import sys


#def insert(originalfile,string):
#    with open(originalfile,'r') as f:
#        with open('newfile.txt','w') as f2: 
#            f2.write(string)
#            f2.write(f.read())
#    os.remove(originalfile)
#    os.rename('newfile.txt',originalfile)
    
    
#folder = "teste_3"
#process_name = "com.physphil.android.unitconverterultimate"
#process_name = "com.vrem.wifianalyzer"
#process_name = "com.baidu.searchbox"

folder = sys.argv[1]
process_name = sys.argv[2]
num_samples = int(sys.argv[3])
'''
print('----------------- read_files.py ------------------------')
print(folder)
print(process_name)
print(num_samples)
'''

data = []
timestamps = []

gc_timestamps = []
#gc_timestamps_2 = []

base_system_server_PSS = 0
base_free_RAM = 0
base_cached_RAM = 0
base_lost_RAM = 0
base_zram_used = 0
base_total_PSS = 0
base_consumption = 0

for i in range(1,num_samples,1):
    system_server_PSS = 0
    free_RAM = 0
    cached_RAM = 0
    lost_RAM = 0
    zram_used = 0
    total_PSS = 0
    consumption = 0
    system_server_gc_total_time = 0
    system_server_gc_pause_time = 0
    #system_ui_gc_total_time = 0
    #system_ui_gc_pause_time = 0
         
    total_frames_rendered = 0
    janky_frames = 0
    janky_ratio = 0
    percentile_50=0
    percentile_90=0
    percentile_95=0
    percentile_99=0
    
    try:
        with open("C:/Users/pedro/Desktop/TESE/"+folder+"/memory/mem1_"+str(i)+".txt", "r") as file:
            #print(file.name)
            line=file.readlines()
            for j in range(0,len(line),1):
                regex = re.compile('Free RAM:[ ]+([0-9,]+)K')  #WATCHOUT, could be M (MB)?
 
                if free_RAM == 0 and regex.search(line[j]):
                    try:
                        free_RAM = regex.search(line[j]).group(1).replace(',', '')
                    except:
                        free_RAM = 0
                    #print("Free RAM: " + free_RAM)
                
                regex = re.compile('Lost RAM:[ ]+([0-9,]+)K')  #WATCHOUT, could be M (MB)?
                if lost_RAM == 0 and regex.search(line[j]):
                    try:
                        lost_RAM = regex.search(line[j]).group(1).replace(',', '')
                    except:
                        lost_RAM = 0
                    #print("Lost RAM: " + lost_RAM)
                
                regex = re.compile('([0-9,]+)K physical used for')  #WATCHOUT, could be M (MB)?
                if zram_used == 0 and regex.search(line[j]):
                    try:
                        zram_used = regex.search(line[j]).group(1).replace(',', '')
                    except:
                        zram_used = 0   
                    #print("ZRAM Used: " + zram_used) 
                
                regex = re.compile('([0-9,]+)K: '+process_name) #com.vrem.wifianalyzer
                #for j in range(0,len(line),1):
                if total_PSS == 0 and regex.search(line[j]):
                    try:
                        total_PSS = regex.search(line[j]).group(1).replace(',', '')
                    except:
                        total_PSS = 0
                    #print("Total PSS: " + total_PSS)
        
        with open("C:/Users/pedro/Desktop/TESE/"+folder+"/timestamps/timestamp_"+str(i)+".txt", "r") as file:
            #print(file.name)
            timestamp=file.readline()
            timestamps.append(timestamp[:-1])
            #print("=======> " + timestamp)
                    
        with open("C:/Users/pedro/Desktop/TESE/"+folder+"/memory/mem2_"+str(i)+".txt", "r") as file:
            #print(file.name)
            line=file.readlines()
            for j in range(0,len(line),1):
                regex = re.compile('TOTAL:[ ]+([0-9]+)')
                regex2 = re.compile('TOTAL PSS:[ ]+([0-9]+)') 
                if regex.search(line[j]):
                    system_server_PSS = regex.search(line[j]).group(1).replace(',', '')
                    #print("System_server PSS: " + system_server_PSS)
                elif regex2.search(line[j]): 
                    system_server_PSS = regex2.search(line[j]).group(1).replace(',', '')
                    
                    

        with open("C:/Users/pedro/Desktop/TESE/"+folder+"/memory/mem3_"+str(i)+".txt", "r") as file:
            #print(file.name)
            line=file.readlines()
            for j in range(0,len(line),1):
                regex = re.compile('Cached:[ ]+([0-9]+)')  #WATCHOUT, could be M (MB)?
                if regex.search(line[j]):
                    cached_RAM = regex.search(line[j]).group(1).replace(',', '')
                    #print("Cached RAM: " + cached_RAM)   
                    
        with open("C:/Users/pedro/Desktop/TESE/"+folder+"/battery/batterystats_"+str(i)+".txt", "r") as file:
            line=file.readlines()
            uid = ""
            #print(line)
            for j in range(0,len(line),1):
                regex = re.compile('top=([0-9a-zA-Z]+):\"'+process_name+'\"')
                if uid=="" and regex.search(line[j]):
                    uid = regex.search(line[j]).group(1)
                    #print("UID: " + uid)
                if uid!="":
                    regex2 = re.compile("Uid " + uid + ": ([0-9.]+) ")
                    regex3 = re.compile("UID " + uid + ": ([0-9.]+) ")
                    if regex2.search(line[j]):
                        consumption = regex2.search(line[j]).group(1)
                    elif regex3.search(line[j]):
                        consumption = regex3.search(line[j]).group(1)
                        #print("Consumption: " + consumption)
                        
        with open("C:/Users/pedro/Desktop/TESE/"+folder+"/gc/gc_"+str(i)+".txt", "r") as file:       
            line=file.readlines()
            
            pause1=0
            pause2=0
            
            for j in range(0,len(line),1):
                timestamp = line[j][:18]
                #regex = re.compile('system_server: Background young concurrent copying GC freed ([0-9]+)\(([0-9]+)(K|M)?B\) 337713(15MB) AllocSpace objects, 95(4320KB) LOS objects, 21% free, 54MB/69MB, paused 805us,749us total 145.646ms')
                if "system_server" in line[j] and timestamp not in gc_timestamps:
                    index = line[j].find("system_server")
                    values = re.findall(r'\d+\.?\d+', line[j][index:])
                    size = len(values)
                    
                    
                    metrics = re.findall(r'ms|us|\ds',line[j][index:])
                    metrics = metrics[1:]   #remove 'us' from 'paused'
                    #print(metrics)
                    
                    size2 = len(metrics)
                    if size2!=3:
                        print("Paused diff")
                        print(file.name)
                    
                    if metrics[0] =='us':
                        pause1 = int(values[size-3])/1000
                    elif metrics[0] == 'ms':
                        pause1 = float(values[size-3])
                    else:
                        pause1 = float(values[size-3])*1000
                    
                    if metrics[1] =='us':
                        pause2 = int(values[size-2])/1000
                    elif metrics[1] == 'ms':
                        pause2 = float(values[size-2])
                    else:
                        pause2 = float(values[size-2])*1000
                    
                    #print(pause1)
                    #print(pause2)
                    system_server_gc_pause_time += (pause1+pause2)
                    
                    
                    if metrics[2]=='us':
                        system_server_gc_total_time += int(values[size-1])/1000
                    elif metrics[2] == 'ms':
                        system_server_gc_total_time += float(values[size-1])
                    else:
                        system_server_gc_total_time += float(values[size-1])*1000
                    
                    system_server_gc_total_time = round(system_server_gc_total_time,3)
                    system_server_gc_pause_time  = round(system_server_gc_pause_time,3) 
                    #print("Total: ")
                    #print(system_server_gc_total_time)
                    #print("Paused: ")
                    #print(system_server_gc_pause_time)

                    gc_timestamps.append(timestamp)
                       
            pause1_2=0
            pause2_2=0
            """
            for j in range(0,len(line),1):
                timestamp = line[j][:18]
                #regex = re.compile('system_server: Background young concurrent copying GC freed ([0-9]+)\(([0-9]+)(K|M)?B\) 337713(15MB) AllocSpace objects, 95(4320KB) LOS objects, 21% free, 54MB/69MB, paused 805us,749us total 145.646ms')
                if "ndroid.systemu" in line[j] and timestamp not in gc_timestamps_2:
                    index = line[j].find("ndroid.systemu")
                    values = re.findall(r'\d+\.?\d+', line[j][index:])
                    size = len(values)
                    
                    
                    metrics = re.findall(r'ms|us|\ds',line[j][index:])
                    metrics = metrics[1:]   #remove 'us' from 'paused'
                    #print(metrics)
                    
                    size2 = len(metrics)
                    if size2!=3:
                        print("Paused diff")
                        print(file.name)
                    
                    if metrics[0] =='us':
                        pause1_2 = int(values[size-3])/1000
                    elif metrics[0] == 'ms':
                        pause1_2 = float(values[size-3])
                    else:
                        pause1_2 = float(values[size-3])*1000
                    
                    if metrics[1] =='us':
                        pause2_2 = int(values[size-2])/1000
                    elif metrics[1] == 'ms':
                        pause2_2 = float(values[size-2])
                    else:
                        pause2_2 = float(values[size-2])*1000
                    
                    #print(pause1_2)
                    #print(pause2_2)
                    system_ui_gc_pause_time += (pause1_2+pause2_2)
                    
                    
                    if metrics[2]=='us':
                        system_ui_gc_total_time += int(values[size-1])/1000
                    elif metrics[2] == 'ms':
                        system_ui_gc_total_time += float(values[size-1])
                    else:
                        system_ui_gc_total_time += float(values[size-1])*1000
                    
                    system_ui_gc_total_time = round(system_ui_gc_total_time,3)
                    system_ui_gc_pause_time  = round(system_ui_gc_pause_time,3) 
                    #print("Total: ")
                    #print(system_server_gc_total_time)
                    #print("Paused: ")
                    #print(system_server_gc_pause_time)

                    gc_timestamps_2.append(timestamp)
        """
        """ 
        with open("C:/Users/pedro/Desktop/TESE/"+folder+"/frames/frames_"+str(i)+".txt", "r") as file:
            line=file.readlines()
            
            for j in range(0,len(line),1):
                
                regex = re.compile('Total frames rendered: ([0-9]+)')
                if regex.search(line[j]):
                    total_frames_rendered = regex.search(line[j]).group(1)
                    
                regex = re.compile('Janky frames: ([0-9]+) \(([0-9.]+)%\)')
                if regex.search(line[j]):
                    janky_frames = regex.search(line[j]).group(1)
                    janky_ratio = regex.search(line[j]).group(2)
                    
                regex = re.compile('50th percentile: ([0-9]+)ms')
                if regex.search(line[j]):
                    percentile_50 = regex.search(line[j]).group(1)\
                
                regex = re.compile('90th percentile: ([0-9]+)ms')
                if regex.search(line[j]):
                    percentile_90 = regex.search(line[j]).group(1)
                    
                regex = re.compile('95th percentile: ([0-9]+)ms')
                if regex.search(line[j]):
                    percentile_95 = regex.search(line[j]).group(1)
                    
                regex = re.compile('99th percentile: ([0-9]+)ms')
                if regex.search(line[j]):
                    percentile_99 = regex.search(line[j]).group(1)
                    
        """ 
       # data.append([system_server_PSS, free_RAM, cached_RAM, lost_RAM, zram_used, total_PSS, consumption])
        #if int(free_RAM) != 0 and int(lost_RAM) != 0 and int(zram_used) != 0:
        if i == 1:
            data.append([
                int(system_server_PSS),
                int(free_RAM), 
                int(cached_RAM),
                int(lost_RAM),
                int(zram_used),
                int(total_PSS),
                system_server_gc_total_time,
                system_server_gc_pause_time,
                #system_ui_gc_total_time,
                #system_ui_gc_pause_time,
                float(consumption),
                0
                ])
        else:
            consumption_difference =  float(consumption) - data[i-2][8]
            if consumption_difference < 0:
                print("ALERT CONSUMPTION NEGATIVE: ")
                print("Previous: ", data[i-2][8])
                print("This: ", float(consumption))
                print("-------------")
                if float(consumption) < 5:
                    data.append([
                        int(system_server_PSS),
                        int(free_RAM), 
                        int(cached_RAM),
                        int(lost_RAM),
                        int(zram_used),
                        int(total_PSS),
                        system_server_gc_total_time,
                        system_server_gc_pause_time,
                        #system_ui_gc_total_time,
                        #system_ui_gc_pause_time,
                        float(consumption),
                        float(consumption)
                    ])
                    print("New:", float(consumption))
                else:
                    data.append([
                        int(system_server_PSS),
                        int(free_RAM), 
                        int(cached_RAM),
                        int(lost_RAM),
                        int(zram_used),
                        int(total_PSS),
                        system_server_gc_total_time,
                        system_server_gc_pause_time,
                        #system_ui_gc_total_time,
                        #system_ui_gc_pause_time,
                        float(consumption),
                        0
                    ])
                    print("New:", 0)
            else:
                data.append([
                    int(system_server_PSS),
                    int(free_RAM), 
                    int(cached_RAM),
                    int(lost_RAM),
                    int(zram_used),
                    int(total_PSS),
                    system_server_gc_total_time,
                    system_server_gc_pause_time,
                    #system_ui_gc_total_time,
                    #system_ui_gc_pause_time,
                    float(consumption),
                    float(consumption) - data[i-2][8]
                ])
       # else:
          #  data.append([0,0,0,0,0,0,0,0])
            
    except FileNotFoundError: #This is skipped if file exists
        print("FileNotFoundError at index ",i )
        break
try:
    with open("C:/Users/pedro/Desktop/TESE/"+folder+"/ltimes/logcat.txt", "r") as file:
        line=file.readlines()
        #print(line)
        for j in range(0,len(line),1):
            #if "ActivityTaskManager: START" in line[j] and "cmp=com.vrem.wifianalyzer/.MainActivity" in line[j]:
            #    start_time = line[j][6:18]
            #    print("START: " + start_time)
            #    print("line: " + str(j))
            #if "Displayed com.vrem.wifianalyzer/.MainActivity" in line[j]:
            #    display_time = line[j][6:18]
            #    print("END: " + display_time)
            #    print("line: " + str(j))
            string = "Displayed "+process_name+"/.MainActivity"
            index = line[j].find(string)
            treshold = line[j][index+len(string)+3:]
            #print("TIME: " + treshold)
except FileNotFoundError: #This is skipped if file exists
        print("FileNotFoundError at index",i )
             


file_name = "C:/Users/pedro/Desktop/TESE/"+folder+"/data.xlsx"

try:
    df=pd.DataFrame(data, index = timestamps, columns=['system_server_PSS','free_RAM','cached_RAM','lost_RAM','zram_used','total_PSS','system_server_gc_total_time','system_server_gc_pause_time','consumption','consumption_diff'])
except ValueError:
    timestamps=timestamps[:-1]
    df=pd.DataFrame(data, index = timestamps, columns=['system_server_PSS','free_RAM','cached_RAM','lost_RAM','zram_used','total_PSS','system_server_gc_total_time','system_server_gc_pause_time','consumption','consumption_diff'])
    
df.index.name = 'timestamps'




with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Raw Data')
    df = df.loc[(df != 0).all(axis=1)]
    df.to_excel(writer, sheet_name='Clean Data')
    writer.sheets['Raw Data'].set_column(0, 10, 20)
    writer.sheets['Clean Data'].set_column(0, 10, 20)
    
    
""" 
base_system_server_PSS = np.mean([row[0] for row in data[:100]])
base_free_RAM = np.mean([row[1] for row in data[:100]])
base_cached_RAM = np.mean([row[2] for row in data[:100]])
base_lost_RAM = np.mean([row[3] for row in data[:100]])
base_zram_used = np.mean([row[4] for row in data[:100]])
base_total_PSS = np.mean([row[5] for row in data[:100]])
base_consumption = np.mean([row[6] for row in data[:100]])

#print(data[:100])
print(base_system_server_PSS)
print(base_free_RAM)
print(base_cached_RAM)
print(base_lost_RAM)
print(base_zram_used)
print(base_total_PSS)
print(base_consumption)

baseline= [[base_system_server_PSS, base_free_RAM, base_cached_RAM, base_lost_RAM, base_zram_used, base_total_PSS, base_consumption]]

file_name_2 = "C:/Users/pedro/Desktop/TESE/"+folder+"/baseline_values.xlsx"
df_2=pd.DataFrame(baseline, columns=['system_server_PSS','free_RAM','cached_RAM','lost_RAM','zram_used','total_PSS','consumption'])



with pd.ExcelWriter(file_name_2, engine='xlsxwriter') as writer_2:
    df_2.to_excel(writer_2, sheet_name='Sheet1')
    
    writer_2.sheets['Sheet1'].set_column(0, 8, 20)
    
"""