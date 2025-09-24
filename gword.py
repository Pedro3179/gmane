# Script that makes a histogram based on the word counts found in the subjects
# and writes a gword.js file.

import sqlite3
import time
import zlib
import string

conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, subject FROM Subjects')
subjects = dict()
for message_row in cur :
    subjects[message_row[0]] = message_row[1]

# This part makes so that, if you have repeated subjects, the repeated words also count

cur.execute('SELECT subject_id FROM Messages')
counts = dict()
for message_row in cur :
    text = subjects[message_row[0]]
    text = text.translate(str.maketrans('','',string.punctuation))
    text = text.translate(str.maketrans('','','1234567890'))
    text = text.strip()
    text = text.lower()
    words = text.split()
    for word in words:
        if len(word) < 4 : continue
        counts[word] = counts.get(word,0) + 1

x = sorted([(value, key) for key, value in counts.items()], reverse=True)

#print(f'print of {x}')
top100_highest = max(x[:100])[0]
top100_lowest = min(x[:100])[0]

print(f'Range of counts: {top100_highest}, {top100_lowest}')

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

fhand = open('gword.js','w')
fhand.write("gword = [")
first = True
for v,k in x[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - top100_lowest) / float(top100_highest - top100_lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")
fhand.close()

print("Output written to gword.js")
print("Open gword.htm in a browser to see the visualization")
