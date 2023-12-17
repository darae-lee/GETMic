#!/bin/bash

result_file_path="sbst/result.txt"

if [ -e "$result_file_path" ]; then
    echo -n > "$result_file_path"
else
    touch "$result_file_path"
fi

for ((i=0; i<10;i++));
 do
    python sbst/main.py Button.py --p 10  --l 3 --r $i
    python sbst/main.py IfStatementConditional.py --p 10 --l 3 --r $i
    python sbst/main.py StateChangeDetection.py --p 10 --l 3 --r $i
    python sbst/main.py SwitchCase.py --p 10 --l 3 --r $i
    python sbst/main.py LoveOMeter.py --p 10 --l 12 --r $i
    python sbst/main.py SegmentDisplay.py --p 10 --l 3 --r $i
    python sbst/main.py WarmButton.py --p 10 --l 12 --r $i
    python sbst/main.py ComplexButton.py --p 10 --l 10 --r $i
 done

echo "Done generating GE test case!"