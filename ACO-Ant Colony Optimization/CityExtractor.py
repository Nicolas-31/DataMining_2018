def getCountry(filename, countryCode):
    lines = dict()
    in_handle = open(filename, "rt", encoding="iso-8859-1")
    found = False
    for line in in_handle:
        if line[0:2] == "no":
            found = True
            city = getPart(line, 1)
            if city not in lines:
                lines[city] = line

            # lines.append(line)
        # since the file is sorted on country, then once we are finished with the
        # countryCode, we can quit.
        elif found == True:
            break

    in_handle.close()
    return lines


def getPart(line, n):
    parts = line.split(",")
    return parts[n]


def saveLinesToFile(filename, lines):
    o_handle = open(filename, "w")
    o_handle.writelines(lines.values())

    o_handle.close()


worldfile = "worldcitiespop.txt"
nofile = "nocitiespop.txt"

no_lines = getCountry(worldfile, "no")
saveLinesToFile(nofile, no_lines)