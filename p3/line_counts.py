import os

count = 0

for file_name in os.listdir('text'):
	with open(os.path.join('text', file_name)) as f:
		count += len(f.readlines())
	print file_name
print count