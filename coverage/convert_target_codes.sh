#!/bin/bash

python coverage/convert_target_code.py target_codes/Button.py
python coverage/convert_target_code.py target_codes/IfStatementConditional.py
python coverage/convert_target_code.py target_codes/LoveOMeter.py
python coverage/convert_target_code.py target_codes/StateChangeDetection.py
python coverage/convert_target_code.py target_codes/SwitchCase.py

echo "Done converting target codes!"