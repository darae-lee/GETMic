#!/bin/bash

result_file_path="coverage/result.txt"

if [ -e "$result_file_path" ]; then
    echo -n > "$result_file_path"
else
    touch "$result_file_path"
fi

python3 coverage/baseline_coverage.py Button.py --t 600 --l 20
python3 coverage/baseline_coverage.py IfStatementConditional.py --t 600 --l 20
python3 coverage/baseline_coverage.py LoveOMeter.py --t 600 --l 20
python3 coverage/baseline_coverage.py StateChangeDetection.py --t 600 --l 20
python3 coverage/baseline_coverage.py SwitchCase.py --t 600 --l 20

echo "Done calculating baseline coverage!"