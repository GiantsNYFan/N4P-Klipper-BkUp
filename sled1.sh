#!/bin/bash
sled1status=$(cat /sys/class/gpio/gpio79/value)

case $sled1status in
0) echo "1" > /home/mks/gpio79_value;;
1) echo "0" > /home/mks/gpio79_value;;
*) echo "control sled1 failed.";;
esac
