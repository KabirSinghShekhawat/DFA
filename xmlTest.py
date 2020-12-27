import xml.etree.ElementTree as ET

tree = ET.parse('13.xml')
root = tree.getroot()

dfa = []
for i in range(13):
    dfa.append(i)
count = 0
for state in root.iter('state'):
    state.set('id',str(count))
    state.set('name','q'+str(count))
    count += 1

for trans in root.iter('transition'):
    for From in trans.iter('from'):
        From.text = '1'
        # print(f'From : {From.text}')
    for to in trans.iter('to'):
        to.text = '3'
        # print(f'To: {to.text}')
    for read in trans.iter('read'):
        read.text = '1'
        # print(f'Read: {read.text}')
tree.write('output_13.xml')