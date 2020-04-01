file = open("2020powrecords.txt", "r")
completed_file = open("FormattedRecords.txt", "w")
content = file.readlines()
file.close()

POW_list = []
intodb = []

for x in content:
    POW_list.append(x)

for POW in POW_list:
    POW = POW.rstrip()
    POW = POW.replace(' ', ',', 4)
    POW = POW[::-1]
    POW = POW.replace(' ', ',', 1)
    POW = POW[::-1]
    intodb.append(POW)

for item in intodb:
    completed_file.write('%s\n' % item)

completed_file.close()
print("Complete")
