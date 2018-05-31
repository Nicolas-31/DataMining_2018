#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys
from os import listdir
from os.path import isfile, join

path = "D:\Data for RNN\comm_use.0-9A-B.txt"
#mergedfile = "data.txt"
mergedfile= "somedata.txt"

def multifilereader(datapath):
    totalcontent = ""
    groups = listdir(datapath)
    for g in groups:
        if g.startswith("."):
            groups.remove(g)

    for g in groups:
        fullpath = join(datapath, g)
        print(fullpath)
        files = [f for f in listdir(fullpath) if isfile(join(fullpath, f))]
        for file in files:
            print(file)
            fullfilename = join(fullpath, file)
            f = open(fullfilename, 'r')

            data = f.read()
            appendtofile(data, mergedfile)
            f.close()




def writetofile(filedata, filename):
    with open(filename, 'w') as file:
        file.write(filedata)

def appendtofile(filedata, filename):
    with open(filename, 'a') as file:
        file.write(filedata)

multifilereader(path)
#writetofile("haha hehe\nog hå", mergedfile)