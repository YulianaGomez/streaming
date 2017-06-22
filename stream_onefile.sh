#!/bin/bash

for number in {1}
do
echo "some data" > filename_$number.txt

for morelines in {1..1000000}
do
echo "some more data in file $number on line_$morelines" >> filename_$number.txt
done
##random_time = $(((RANDOM%3)+1))
#sleep $(((RANDOM%3)+1))
mv /home/ubuntu/yzamora/streaming/filename_$number.txt /home/ubuntu/yzamora/streaming/test_files/. 
#mv /home/ubuntu/yzamora/streaming/filename_$number.txt //mnt/ramdisk/. 
done
exit 
