#!/bin/bash

result_file_path="coverage/result.txt"

if [ -e "$result_file_path" ]; then
    echo -n > "$result_file_path"
else
    touch "$result_file_path"
fi

for ((i=0; i<10;i++));
  do
#    python3 coverage/baseline_coverage.py Button.py --t 500 --l 3 --r $i
#    python3 coverage/baseline_coverage.py IfStatementConditional.py --t 500 --l 3 --r $i
#    python3 coverage/baseline_coverage.py StateChangeDetection.py --t 500 --l 3 --r $i
#    python3 coverage/baseline_coverage.py SwitchCase.py --t 500 --l 3 --r $i
    python3 coverage/baseline_coverage.py LoveOMeter.py --t 500 --l 10 --r $i
#    python3 coverage/baseline_coverage.py SegmentDisplay.py --t 500 --l 3 --r $i
  done


echo "Done calculating baseline coverage!"