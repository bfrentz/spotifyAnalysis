#!/bin/bash

input="./data/artists/artists.txt"

while IFS= read -r line
do
  echo "$line"
  python3 artistTracks.py "$line"
done < "$input"
