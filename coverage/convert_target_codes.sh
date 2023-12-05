#!/bin/bash

python3 coverage/convert_target_code.py target_codes/Button.py
python3 coverage/convert_target_code.py target_codes/IfStatementConditional.py
python3 coverage/convert_target_code.py target_codes/LoveOMeter.py
python3 coverage/convert_target_code.py target_codes/StateChangeDetection.py
python3 coverage/convert_target_code.py target_codes/SwitchCase.py
python3 coverage/convert_target_code.py target_codes/SegmentDisplay.py
python3 coverage/convert_target_code.py target_codes/LoveOMeter_button.py

echo "Done converting target codes!"