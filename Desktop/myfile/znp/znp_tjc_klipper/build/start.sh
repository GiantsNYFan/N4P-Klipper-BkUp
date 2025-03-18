#!/bin/bash
echo "Start makerbase-client"
time=$(date "+%Y%m%d%H%M%S")
# /root/makerbase-client/build/MakerbaseClient localhost > /root/mksclient/test-$time.log
/home/mks/Desktop/myfile/znp/znp_tjc_klipper/build/io -4 0xff100028 0x010000
/home/mks/Desktop/myfile/znp/znp_tjc_klipper/build/znp_tjc_klipper localhost >/dev/null 2>&1
