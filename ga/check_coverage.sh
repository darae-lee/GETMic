#!/bin/bash

result_file_path="ga/result.txt"

if [ -e "$result_file_path" ]; then
    echo -n > "$result_file_path"
else
    touch "$result_file_path"
fi

python ga/sbst.py Button.py --p 10 --l 4
python ga/sbst.py IfStatementConditional.py --p 10 --l 4
python ga/sbst.py StateChangeDetection.py --p 10 --l 6
python ga/sbst.py SwitchCase.py --p 10 --l 6
python ga/sbst.py LoveOMeter.py --p 10 --l 6

echo "Done calculating GA coverage!"