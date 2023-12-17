#!/bin/bash

result_file_path="coverage/result.txt"

if [ -e "$result_file_path" ]; then
    echo -n > "$result_file_path"
else
    touch "$result_file_path"
fi

for ((i=0; i<10;i++));
 do
   python coverage/baseline.py Button.py --t 500 --l 3 --r $i
   python coverage/baseline.py IfStatementConditional.py --t 500 --l 3 --r $i
   python coverage/baseline.py StateChangeDetection.py --t 500 --l 3 --r $i
   python coverage/baseline.py SwitchCase.py --t 500 --l 3 --r $i
   python coverage/baseline.py LoveOMeter.py --t 1000 --l 12 --r $i
   python coverage/baseline.py SegmentDisplay.py --t 500 --l 3 --r $i
   python coverage/baseline.py WarmButton.py --t 1000 --l 12 --r $i
   python coverage/baseline.py ComplexButton.py --t 1000 --l 10 --r $i
 done

echo "Done calculating baseline coverage!"