#!/usr/bin/python
#Written by Daniel Kenner using gspread and the gspread documentation at https://github.com/burnash/gspread
#This script writes a hosts file with information from a google spreadsheet

import gspread
import subprocess
import re
import sys
import time
import ConfigParser

#make a timestamp
def stamp():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ ",time.gmtime())

config = ConfigParser.RawConfigParser()
config.read('spreadsheet.conf')

username = config.get("Configuration", "username")
password = config.get("Configuration", "password")
spreadsheet = config.get("Configuration", "spreadsheet")
printHost = config.getboolean("Configuration", "printHost")

# Login with your Google account
gc = gspread.login(username, password)

# Open a worksheet from spreadsheet with one shot
worksheet = gc.open_by_key(spreadsheet).sheet1

# Find a cell with exact string value
cell = worksheet.find("DNS Entries")

# Get all values from the DNS Entries column
values_list = worksheet.col_values(cell.col)

#lists of hosts
hostsEntries = []

for value in values_list:
    #print value
    #if there is a value here
    if value is not None:
        #not the first one
        if value != "DNS Entries":
            #split the values if there are multiple ones
            entries = value.split("\n")
            #print entries
            for entry in entries:
                #if it's a comment, just add it
                if entry[:1] == "#":
                    tup = entry, ""
                    hostsEntries.append(tup)
                    continue
                #for each value
                #print entry
                val = entry.split("=")
                #replace for formatting later
                val[1] = val[1].replace(" ", "\t")
                #package the tuple
                tup = val[0], val[1]
                #append to the list
                hostsEntries.append(tup)
            
#now we've got all the elements, unpack them into a file
#print hostsEntries

#write the string
output = "#Hosts File Generated by hostmaker.py - Written by Daniel Kenner\n"
output = output+("#IPAddress     Hostname    		 Aliases\n")

#we are going to insert the prefix file here.
#output = output+"127.0.0.1\tlocalhost\n"

prefixFile = open("host_prefix.txt", "r")
output = output + prefixFile.read() + "\n"


for host in hostsEntries:
    ip, names = host
    output = output + ip + "\t" + names+"\n"

#now we can check against the old one.

if printHost:
    print output

outFile = open("/tmp/hosts", "w")

outFile.write(output)

outFile.close()
#print checkingFile

#print output

diffstat = subprocess.check_output("diff /etc/hosts /tmp/hosts | diffstat", shell=True)

#print diffstat

check = re.search("\|\s+(?P<numChanges>[0-9]+)", diffstat)
if check is not None:
    numChanges = check.group("numChanges")
    
    #print numChanges
    
    if int(numChanges) < 10:
        print stamp()+"Replacing File"
        #subprocess.check_output("mv -f /tmp/hosts /etc/hosts")
        outFile = open("/etc/hosts", "w")

        outFile.write(output)

        outFile.close()
    else:
        print stamp()+"Too Many Changes to /etc/hosts file, Aborting."
else:
    print stamp()+"No Changes Necessary, Hosts File is already up-to-date"