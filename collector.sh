#! /bin/sh

adb shell dumpsys batterystats --reset #clear battery stats info
adb shell dumpsys batterystats enable no-auto-reset
adb logcat -c  #clear logcat
adb shell dumpsys gfxinfo $1 reset

end_time=$(($SECONDS + $3))

echo "FINISHING AT: $end_time"

i=1
while [ $SECONDS -lt $end_time ]
do
   NOW=$(date +"%d-%m-%Y %H:%M:%S")
   echo "Collecting data $i. ($SECONDS) ($NOW)"
   echo "$NOW" > C:/Users/pedro/Desktop/TESE/$2/timestamps/timestamp_$i.txt
   adb shell dumpsys batterystats > C:/Users/pedro/Desktop/TESE/$2/battery/batterystats_$i.txt
   adb shell dumpsys meminfo > C:/Users/pedro/Desktop/TESE/$2/memory/mem1_$i.txt #all processes mem stats
   adb shell dumpsys meminfo system_server -d > C:/Users/pedro/Desktop/TESE/$2/memory/mem2_$i.txt  #system_server mem stats
   adb shell "cat /proc/meminfo" > C:/Users/pedro/Desktop/TESE/$2/memory/mem3_$i.txt
   #adb shell "top" > C:/Users/pedro/Desktop/TESE/$2/memory/mem4_$i.txt
   adb shell dumpsys gfxinfo > C:/Users/pedro/Desktop/TESE/$2/frames/frames_$i.txt
   #adb logcat -d -vthreadtime | grep --line-buffered "GC freed" > C:/Users/pedro/Desktop/TESE/$2/gc/gc_$i.txt
   adb logcat -d | grep "GC freed" > C:/Users/pedro/Desktop/TESE/$2/gc/gc_$i.txt
   sleep 30
   i=$((i+1)) 
done

#adb logcat -vthreadtime | grep --line-buffered $1 > C:/Users/pedro/Desktop/TESE/$2/ltimes/logcat.txt  #logcat dump for launch times calculation
#adb logcat -vthreadtime | grep --line-buffered  "ActivityTaskManager: Displayed $1" > C:/Users/pedro/Desktop/TESE/$2/ltimes/logcat.txt  #logcat dump for launch times calculation


#adb shell "kill $(pgrep monkey)"
#adb shell "kill \$(pgrep monkey)" > "C:/Users/pedro/Desktop/TESE/$2/log.txt"


#adb logcat -vthreadtime | grep --line-buffered  "ActivityTaskManager: Displayed com.physphil.android.unitconverterultimate" > C:/Users/pedro/Desktop/TESE/teste_2/ltimes/logcat.txt

NOW=$(date +"%d-%m-%Y %H:%M:%S")
echo "FINISHED COLLECTING AT $NOW"