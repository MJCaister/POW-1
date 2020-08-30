# reads the text file with records after OCR
file = open("2020powrecords.txt", "r")
# this file doesn't exist before this script is ran. it generates it to print
# the formatted records
completed_file = open("FormattedRecords.txt", "w")
content = file.readlines()
file.close()

# lists used to store data
POW_list = []
intodb = []

# loops through to add each record to a list
for x in content:
    POW_list.append(x)

# loops through each item to add a comma to seperate into db coloums
for POW in POW_list:
    # strips of trailing and leading whitespace
    POW = POW.rstrip()
    # the first 4 spaces seperate the 4 coloums
    POW = POW.replace(' ', ',', 4)
    # reverses the string to replace the final space in the string
    POW = POW[::-1]
    POW = POW.replace(' ', ',', 1)
    POW = POW[::-1]
    # adds to formatted list
    intodb.append(POW)

# this writes each list item onto a differnet line of the text file
for item in intodb:
    completed_file.write('%s\n' % item)

# closes the formatted text file so it cannot be further editted.
completed_file.close()
print("Complete")
