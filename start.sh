#!/bin/bash

rm ~/home/parallels/stream_transfer/destination/*.*

cp /home/parallels/stream_transfer/other_files/*.* /home/parallels/stream_transfer/test_files/.

python pub8_timing.py
python sub6_delete.py




