#!/bin/bash

for number in {1..100}
do
echo "some data" > filename_$number.txt
##random_time = $(((RANDOM%3)+1))
sleep $(((RANDOM%3)+1))
mv /home/parallels/stream_transfer/filename_$number.txt /home/parallels/stream_transfer/test_files/ 
done
exit 
