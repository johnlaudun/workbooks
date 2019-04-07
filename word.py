import sys

filename = sys.argv[1]
target = sys.argv[2]
count = int(sys.argv[3])

with open(filename, 'r') as myfile:
  data = myfile.read()

data = data.replace("\n\n", " ")
data = data.replace(".", "")
data = data.replace(",", "")
words = data.split(" ")

targetIndices = [i for i, x in enumerate(words) if x == target]

before = []
after = []
for x, word in enumerate(words):
	for i in targetIndices:
		if x >= (i-count) and x < i:
			before.append(word)
		if x > i and x <= (i+count):
			after.append(word)

print(str(count) + " words before " + target + ":\n")
for i in range(count):
	if i <= len(before)/count:
		print(" ".join(before[i*count:(i+1)*count]) + "\n")

print(str(count) + " words after " + target + ":\n")
for i in range(count):
	if i <= len(after)/count:
		print(" ".join(after[i*count:(i+1)*count]) + "\n")

