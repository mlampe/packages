#!/bin/sh
[ -x /lib/udev/udev-acl ] || exit 0
for i in /dev/nvidia*; do
  /lib/udev/udev-acl "--action=change" "--device=$i"
done
