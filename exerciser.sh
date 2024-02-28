
#! /bin/sh
#EXERCISER MONKEY: https://developer.android.com/studio/test/other-testing-tools/monkey
#		adb shell monkey [options] <event-count>
#		adb shell monkey -p your.package.name -v 500
#		adb shell monkey -p ee.dustland.android.dustlandsudoku -v --pct-touch 100 --throttle 1000 500
#			//100% touch events
#			//1000 miliseconds between each event
#			//500 events

function finish() {
    echo "CTRL+C received. Performing cleanup..."
    adb shell "kill \$(pgrep monkey)"
    exit 0
}

trap finish SIGINT

echo $1 >> "C:/Users/pedro/Desktop/TESE/$2/experiment_info.txt"

NOW=$(date +"%d-%m-%Y %H:%M:%S")
echo "STARTED EXERCISING AT $NOW"
echo "STARTED EXERCISING AT $NOW" >> "C:/Users/pedro/Desktop/TESE/$2/experiment_info.txt"

#echo "EXERCISING PROCESS: $1"
#adb shell monkey -p $1 -v --pct-touch 100 --throttle 1000 10
    #100% touch events
    #1000 miliseconds between each event
    #500 events

adb shell monkey -p $1 -v-v-v \
 --ignore-crashes \
 --ignore-timeouts \
 --ignore-security-exceptions \
 --monitor-native-crashes \
 --ignore-native-crashes \
 --pct-trackball 0 \
 --pct-nav 0 \
 --pct-syskeys 0 \
 --throttle 800 100000000

# --pct-majornav 20 \
#adb shell monkey -p com.king.candycrushsaga -v-v-v --ignore-crashes --ignore-timeouts --ignore-security-exceptions --monitor-native-crashes --ignore-native-crashes --pct-trackball 0 --pct-nav 0 --pct-syskeys 0 --throttle 800 100000000

#--pct-touch <percent>	Adjust percentage of touch events. (Touch events are a down-up event in a single place on the screen.)
#--pct-motion <percent>	Adjust percentage of motion events. (Motion events consist of a down event somewhere on the screen, a series of pseudo-random movements, and an up event.)
#--pct-trackball <percent>	Adjust percentage of trackball events. (Trackball events consist of one or more random movements, sometimes followed by a click.)
#--pct-nav <percent>	Adjust percentage of "basic" navigation events. (Navigation events consist of up/down/left/right, as input from a directional input device.)
#--pct-majornav <percent>	Adjust percentage of "major" navigation events. (These are navigation events that will typically cause actions within your UI, such as the center button in a 5-way pad, the back key, or the menu key.)
#--pct-syskeys <percent>	Adjust percentage of "system" key events. (These are keys that are generally reserved for use by the system, such as Home, Back, Start Call, End Call, or Volume controls.)
#--pct-appswitch <percent>	Adjust percentage of activity launches. At random intervals, the Monkey will issue a startActivity() call, as a way of maximizing coverage of all activities within your package.
#--pct-anyevent <percent>	Adjust percentage of other types of events. This is a catch-all for all other types of events such as keypresses, other less-used buttons on the device, and so forth.

# count=0                   # initialize counter
# while [ $count -lt 10000000 ]   # generate 10 events
# do
#     x=$(( $RANDOM % 720 ))   # generate a random x coordinate
#     y=$(( $RANDOM % 1600 ))   # generate a random y coordinate
#     adb shell input tap $x $y -p $1  # simulate a tap at the random coordinates
#     count=$((count+1))        # increment the counter

#     # if [ $((i % 10)) -eq 0 ]
#     # then
#     #     adb shell input keyevent 4 -p $1
#     # fi

#     sleep 1                   # pause the script for 1 second
# done


#NOW=$(date +"%d-%m-%Y %H:%M:%S")
#echo "FINISHED EXERCISING AT $NOW"
#echo "FINISHED EXERCISING AT $NOW" >> "C:/Users/pedro/Desktop/TESE/$2/experiment_info.txt"
