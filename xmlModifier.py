f = open("output_13_final.txt", "w")
f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 7.1.-->')
f2 = open("output_13.txt", "r")
f.write(f2.read())
for i in range(len(f)):
    if(f(i) == '\n'):
        f.seek(i)
        f.write('&#13;')
    else:
        continue
f2.close()
f.close()