#!/bin/bash
#
# @brief   botracked
# @version 1.0.0
# @date    Fri Sep 18 16:30:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 gates/gates/interfaces_checker.py botracked
python3 gates/gates/isp_checker.py botracked
python3 gates/gates/limits_checker.py botracked
python3 gates/gates/srp_checker.py botracked

echo "Done"
