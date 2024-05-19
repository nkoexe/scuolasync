#!/bin/bash

# Get a list of connected displays
displays=$(xrandr | grep " connected" | cut -d ' ' -f1)

#first display is primary
primary_display=${displays[0]}

# Loop through displays and set configurations
for display in $displays; do
  # Set the display with highest width as primary
  if [[ "$display" == "$primary_display" ]]; then
    xrandr --output "$display" --auto --primary
  else
    # Mirror other displays to the primary display
    xrandr --output "$display" --same-as "$primary_display"
  fi
done
