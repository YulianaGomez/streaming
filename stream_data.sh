#!/bin/bash

#for number in {1..100}
iter=0
while :
do
#echo "some data" > filename_$number.txt
echo "some data" > filename_$iter.txt
##random_time = $(((RANDOM%3)+1))
sleep $(((RANDOM%3)+1))
#mv /home/parallels/stream_transfer/filename_$number.txt /home/parallels/stream_transfer/test_files/ 
mv /home/parallels/stream_transfer/filename_$iter.txt /home/parallels/stream_transfer/zero_globus/test_files/ 
let iter++
done
exit 
