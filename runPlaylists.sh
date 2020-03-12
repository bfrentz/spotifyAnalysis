 #!/bin/bash

input="./data/playlists/playlists.txt"

while IFS= read -r line
do
  echo "$line"
 python3 playlistData.py "$line"
done < "$input"
