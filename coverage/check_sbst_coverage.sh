#!/bin/bash

result_file_path="coverage/result.txt"

if [ -e "$result_file_path" ]; then
    echo -n > "$result_file_path"
else
    touch "$result_file_path"
fi

for ((i=0; i<10;i++));
 do
   python coverage/sbst.py Button.py --t 500 --l 3 --r $i
  #  python coverage/sbst.py IfStatementConditional.py --t 500 --l 3 --r $i
  #  python coverage/sbst.py StateChangeDetection.py --t 500 --l 3 --r $i
  #  python coverage/sbst.py SwitchCase.py --t 500 --l 3 --r $i
  #  python coverage/sbst.py LoveOMeter.py --t 500 --l 10 --r $i
  #  python coverage/sbst.py SegmentDisplay.py --t 500 --l 3 --r $i
  #  python coverage/sbst.py WarmButton.py --t 1000 --l 12 --r $i
 done

echo "Done calculating baseline coverage!"