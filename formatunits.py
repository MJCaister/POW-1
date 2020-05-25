file = open("weirdunits.txt", "r")
completed_file = open("FormattedUnits.txt", "w")
content = file.readlines()
file.close()

misc = open("dbunits.txt", "r")
dblist = misc.readlines()
misc.close()

intodb = []
raw = []
unitlist = []

for x in dblist:
    x.strip()
    print(x)
    unitlist.append(x)

for x in content:
    raw.append(x)

for pris in raw:
    pris.rstrip()
    spl = pris.split(" ", 1)
    pid = spl[0]
    pep = spl[1]
    print(pid)
    units = pep.split(" att ")
    unitone = units[0]
    unittwo = units[1]
    print(unitlist)
    print(unittwo)
    print(unitlist[82])
    id_one = unitlist.index(str(unitone))
    id_two = unitlist.index(unittwo)
    rel_one = str(pid + "," + id_one)
    rel_two = str(pid + "," + id_two)
    print(rel_one)
    print(rel_two)
    intodb.append(rel_one)
    intodb.append(rel_two)

#for item in intodb:
#    completed_file.write('%s\n' % item)

#completed_file.close()
#print("Complete")
