# Sorts the text file of artists into alphabetical order
# Add artists to the end of the text file (each on their own line) and then rerun this script

with open('artists.txt') as f:
	lines = f.readlines()

lines.sort()

with open('artists.txt', 'w') as f:
	f.writelines(lines)
