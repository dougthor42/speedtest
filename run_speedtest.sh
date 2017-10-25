#! /bin/bash
source ~/speedtest/.venv-speedtest/bin/activate
speedtest --csv >> ~/speedtest/results.csv
deactivate
