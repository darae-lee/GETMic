#!/bin/bash

result_file_path="ga/result.txt"

if [ -e "$result_file_path" ]; then
    echo -n > "$result_file_path"
else
    touch "$result_file_path"
fi

#for ((i=0; i<10;i++));
#  do
##    python ga/sbst.py Button.py --p 10  --l 3 --r $i
##    python ga/sbst.py IfStatementConditional.py --p 10 --l 3 --r $i
##    python ga/sbst.py StateChangeDetection.py --p 10 --l 3 --r $i
##    python ga/sbst.py SwitchCase.py --p 10 --l 3 --r $i
#    python ga/sbst.py LoveOMeter.py --p 10 --l 3 --r $i
##    python ga/sbst.py SegmentDisplay.py --p 10 --l 3 --r $i
#  done

# python ga/sbst.py WarmButton.py --p 20 --l 20 --r 0
python ga/sbst.py ButtonCounter.py --p 20 --l 20 --r 0

echo "Done calculating GA coverage!"