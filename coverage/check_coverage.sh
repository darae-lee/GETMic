#!/bin/bash

result_file_path="coverage/result.txt"

if [ -e "$result_file_path" ]; then
    echo -n > "$result_file_path"
else
    touch "$result_file_path"
fi

python3 coverage/baseline_coverage.py Button.py --t 500 --l 3 --r 101
python3 coverage/baseline_coverage.py IfStatementConditional.py --t 500 --l 3 --r 101
python3 coverage/baseline_coverage.py StateChangeDetection.py --t 500 --l 3 --r 101
python3 coverage/baseline_coverage.py SwitchCase.py --t 500 --l 3 --r 101
python3 coverage/baseline_coverage.py LoveOMeter.py --t 500 --l 10 --r 101
python3 coverage/baseline_coverage.py SegmentDisplay.py --t 500 --l 10 --r 101

echo "Done calculating baseline coverage!"