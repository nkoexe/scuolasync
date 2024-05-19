#!/bin/bash

# Get the names of connected displays
displays=$(xrandr | grep " connected" | cut -d" " -f1)

# Find the biggest resolution available among all connected displays
biggest_resolution=$(xdpyinfo | awk '/dimensions/{print $2}' | sort -nr | head -n 1)

# Set the resolution for all displays
for display in $displays; do
  xrandr --output $display --mode $biggest_resolution
done

# Mirror all displays to the primary display
primary_display=$(echo $displays | head -n 1)
for display in $displays; do
  if [ "$display" != "$primary_display" ]; then
    xrandr --output $display --same-as $primary_display
  fi
done