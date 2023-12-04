#!/bin/bash

result_file_path="coverage/result.txt"

if [ -e "$result_file_path" ]; then
    echo -n > "$result_file_path"
else
    touch "$result_file_path"
fi

python coverage/baseline_coverage.py Button.py --t 1000 --l 4
python coverage/baseline_coverage.py IfStatementConditional.py --t 1000 --l 4
python coverage/baseline_coverage.py StateChangeDetection.py --t 1000 --l 4
python coverage/baseline_coverage.py SwitchCase.py --t 1000 --l 4
python coverage/baseline_coverage.py LoveOMeter.py --t 1000 --l 4

echo "Done calculating baseline coverage!"