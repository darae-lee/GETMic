#!/bin/bash

result_file_path="coverage/result.txt"

if [ -e "$result_file_path" ]; then
    echo -n > "$result_file_path"
else
    touch "$result_file_path"
fi

python coverage/sbst.py Button.py
python coverage/sbst.py IfStatementConditional.py
python coverage/sbst.py StateChangeDetection.py
python coverage/sbst.py SwitchCase.py
python coverage/sbst.py LoveOMeter.py
python coverage/sbst.py SegmentDisplay.py
python coverage/sbst.py WarmButton.py

echo "Done calculating baseline coverage!"