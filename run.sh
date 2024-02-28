#! /bin/sh

# sh C:/Users/pedro/Desktop/TESE/scripts/run.sh

# adb shell dumpsys battery | grep leve


#process="com.physphil.android.unitconverterultimate"
#process="net.sourceforge.opencamera"
#process="com.free.turbocleaner"
#process="notion.id"

#process="com.matteljv.uno"
#process="com.scopely.monopolygo"
process="sonic.bubbleshoot.classic"
#process="com.king.candycrushsaga"
#process="beetles.puzzle.solitaire"

#process="com.baidu.searchbox"
#process="com.android.chrome"
#process="com.brave.browser"
#process="org.mozilla.firefox"
#process="com.microsoft.emmx"

#process="com.sina.weibo"
#process="com.reddit.frontpage"
#process="com.zhiliaoapp.musically"
#process="com.twitter.android"
#process="com.facebook.lite"

#----------- OTHERS -------------------
#process="com.simplemobiletools.notes"
#process="app.dogo.com.dogo_android"
#process="com.joytunes.simplypiano"
#process="org.wikipedia"
#process="com.fixeads.olxportugal"


folder="teste_72" 

duration=$((24 * 60 * 60))  # 24 hours in seconds

if [ -d "C:/Users/pedro/Desktop/TESE/$folder" ]; then
    echo "Folder already exists: $folder"
    echo "What would you like to do?"
    echo "1. Clean up the existing folder."
    echo "2. Change the folder path."
    read -p "Enter your choice (1 or 2): " choice

    case $choice in
        1)
            echo "Performing cleanup for $folder_path..."
            # Add your cleanup actions here
            rm -rf "C:/Users/pedro/Desktop/TESE/$folder"/*
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/battery"
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/frames"
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/ltimes"
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/memory"
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/timestamps"
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/gc"
            touch "C:/Users/pedro/Desktop/TESE/$folder/monkey.txt"
            touch "C:/Users/pedro/Desktop/TESE/$folder/experiment_info.txt"
            touch "C:/Users/pedro/Desktop/TESE/$folder/log.txt"
            ;;
        2)
            read -p "Enter a new folder path: " new_folder_path
            folder=$new_folder_path

            echo $folder

            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder"
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/battery"
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/frames"
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/ltimes"
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/memory"
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/timestamps"
            mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/gc"
            touch "C:/Users/pedro/Desktop/TESE/$folder/monkey.txt"
            touch "C:/Users/pedro/Desktop/TESE/$folder/experiment_info.txt"
            touch "C:/Users/pedro/Desktop/TESE/$folder/log.txt"
            
            ;;
        *)
            echo "Invalid choice. Exiting..."
            exit 1
            ;;
    esac
else
    mkdir -p "C:/Users/pedro/Desktop/TESE/$folder"
    mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/battery"
    mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/frames"
    mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/ltimes"
    mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/memory"
    mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/timestamps"
    mkdir -p "C:/Users/pedro/Desktop/TESE/$folder/gc"
    touch "C:/Users/pedro/Desktop/TESE/$folder/monkey.txt"
    touch "C:/Users/pedro/Desktop/TESE/$folder/experiment_info.txt"
    touch "C:/Users/pedro/Desktop/TESE/$folder/log.txt"
fi

echo "---------------------- Experiment running --------------------"
echo "Time: ${duration} seconds"
echo "Process: ${process}"
echo "Folder: ${folder}"

echo "---------------------- Usefull commands --------------------"
echo "sh C:/Users/pedro/Desktop/TESE/scripts/run.sh"
echo "adb shell \"kill \$(pgrep monkey)\""
echo "adb shell ps -A > C:/Users/pedro/Desktop/processes.txt"
echo "adb shell kill -s QUIT "
echo "adb shell dumpsys battery"

#adb pair 192.168.1.99:34801 488288
#adb connect 192.168.1.99:37641

C:/Programas/WindowsApps/Microsoft.WindowsTerminalPreview_1.18.1462.0_x64__8wekyb3d8bbwe/wt.exe --window 0 new-tab --profile "cmd" --title "Exerciser" sh C:/Users/pedro/Desktop/TESE/scripts/exerciser.sh $process $folder $duration
C:/Programas/WindowsApps/Microsoft.WindowsTerminalPreview_1.18.1462.0_x64__8wekyb3d8bbwe/wt.exe --window 0 new-tab --profile "cmd" --title "Collector" sh C:/Users/pedro/Desktop/TESE/scripts/collector.sh $process $folder $duration



