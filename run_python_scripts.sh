#! /bin/sh

# sh C:/Users/pedro/Desktop/TESE/scripts/run_python_scripts.sh

# python3 C:/Users/pedro/Desktop/TESE/scripts/read_files.py teste_32 com.simplemobiletools.notes 1500
# python3 C:/Users/pedro/Desktop/TESE/scripts/adarta.py teste_25 com.baidu.searchbox

scripts="C:/Users/pedro/Desktop/TESE/scripts/read_files.py C:/Users/pedro/Desktop/TESE/scripts/adarta.py"

#folders="teste_26 teste_27 teste_30 teste_31 teste_32 teste_33 teste_34 teste_35 teste_36 teste_37 teste_38 teste_39 teste_40 teste_41 teste_42 teste_43 teste_44 teste_45 teste_46 teste_47 teste_48 teste_49 teste_50 teste_51 teste_52 teste_53 teste_54 teste_55 teste_56 teste_57 teste_58 teste_59 teste_60 teste_61 teste_62 teste_63 teste_64 teste_65 teste_66 teste_67 teste_68 teste_69 teste_70 teste_71 teste_72"
folders="teste_44"

samples=1500

for folder in $folders
do

    file="C:/Users/pedro/Desktop/TESE/$folder/experiment_info.txt"

    process=$(head -n 1 $file)
    #varlen=${#line}

    echo "=============================="
    echo "$folder"
    echo "$process"
    echo "=============================="

    #python3 C:/Users/pedro/Desktop/TESE/scripts/read_files.py $folder $process $samples

    #1 2 3 4 (_5)
    python3 C:/Users/pedro/Desktop/TESE/scripts/adarta2.py $folder $process $samples



done
