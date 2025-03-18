#! /bin/bash

systemctl stop moonraker.service && rm /home/mks/.moonraker_database/data.mdb
systemctl restart moonraker.service && reboot