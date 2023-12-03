#!/bin/bash

python coverage/baseline_coverage.py Button.py
python coverage/baseline_coverage.py IfStatementConditional.py
python coverage/baseline_coverage.py LoveOMeter.py
python coverage/baseline_coverage.py StateChangeDetection.py
python coverage/baseline_coverage.py SwitchCase.py

echo "Done calculating baseline coverage!"