#!/bin/bash

result_file_path="ga/result.txt"

if [ -e "$result_file_path" ]; then
    echo -n > "$result_file_path"
else
    touch "$result_file_path"
fi

python3 ga/sbst.py Button.py --p 8 --l 3
python3 ga/sbst.py IfStatementConditional.py --p 8 --l 3
python3 ga/sbst.py StateChangeDetection.py --p 8 --l 3
python3 ga/sbst.py SwitchCase.py --p 8 --l 3
python3 ga/sbst.py LoveOMeter.py --p 10 --l 10
python3 ga/sbst.py SegmentDisplay.py --p 10 --l 10

echo "Done calculating GA coverage!"