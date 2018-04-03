#!/bin/bash
display=$(xrandr | grep -wi connected | grep -i hdmi | cut -f1 -d" ")
xrandr --output ${display} --primary
