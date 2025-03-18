#!/bin/bash
sled2status=$(cat /sys/class/gpio/gpio66/value)

case $sled2status in
0) echo "1" > /home/mks/gpio66_value;;
1) echo "0" > /home/mks/gpio66_value;;
*) echo "control sled2 failed.";;
esac
