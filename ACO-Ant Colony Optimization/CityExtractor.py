def getCountry(filename, countryCode):
    lines = dict()
    inFile = open(filename, "r", encoding="iso-8859-1")
    found = False
    for line in inFile:
        if line[0:2] == "no":
            found = True
            city = getItem(line, 1)
            if city not in lines:
                lines[city] = line

            # lines.append(line)
        # since the file is sorted on country, then once we are finished with the
        # countryCode, we can quit.
        elif found == True:
            break

    inFile.close()
    return lines


def getItem(line, n):
    parts = line.split(",")
    return parts[n]


def saveResultsToFile(filename, lines):
    outFile = open(filename, "w")
    outFile.writelines(lines.values())

    outFile.close()


worldfile = "worldcitiespop.txt"
norwayfile = "nocitiespop.txt"

no_lines = getCountry(worldfile, "no")
saveResultsToFile(norwayfile, no_lines)