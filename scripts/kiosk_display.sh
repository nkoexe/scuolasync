#!/bin/bash

# Get a list of connected displays and their resolutions
displays=$(xrandr | grep " connected" | awk '{print $1, $3}')

# Find the display with the highest width
highest_width=0
primary_display=""
for display in $displays; do
  # Extract width from resolution string (e.g., 1920x1080)
  width=${display#*x}
  
  if [[ $width -gt $highest_width ]]; then
    highest_width=$width
    primary_display=${display%% *}
  fi
done

# Loop through displays and set configurations
for display in $displays;
do
  display_name=${display%% *}
  
  # Set the display with highest width as primary
  if [[ "$display_name" == "$primary_display" ]]; then
    xrandr --output $display_name --auto --primary
  else
    # Mirror other displays to the primary display
    xrandr --output $display_name --same-as $primary_display
  fi
done