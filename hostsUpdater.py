#!/usr/bin/python
#Written by Daniel Kenner using gspread and the gspread documentation at https://github.com/burnash/gspread
#This script reads a hosts file and updates a google spreadsheet with the values

import gspread
import sys
import ConfigParser


config = ConfigParser.RawConfigParser()
config.read('spreadsheet.conf')

username = config.get("Configuration", "username")
password = config.get("Configuration", "password")
spreadsheet = config.get("Configuration", "spreadsheet")

# Login with your Google account
gc = gspread.login(username, password)

# Open a worksheet from spreadsheet with one shot
worksheet = gc.open_by_key(spreadsheet).sheet1

updateColumn = worksheet.find("DNS Entries")

updateColumn = updateColumn.col

interfaceColumn = worksheet.find("interfaces")

interfaceColumn = interfaceColumn.col

#print updateColumn

#let's get the host file

hostsFile = open("hosts.txt", "r")

hosts = hostsFile.read()

hostsFile.close()

#now we need to go through each line in the hosts file

lines = hosts.split("\n")

#for each line
for line in lines:
    #if the line is a comment, treat it special
    if line[:1] == "#":
        try:
            cell = worksheet.find(line)
            rowToAddTo = cell.row
            worksheet.update_cell(rowToAddTo, updateColumn, line)
            worksheet.update_cell(rowToAddTo, 1, line)
            continue
        except gspread.exceptions.CellNotFound:
            worksheet.add_rows(1)
            rowToAddTo = worksheet.row_count
            worksheet.update_cell(rowToAddTo, updateColumn, line)
            worksheet.update_cell(rowToAddTo, 1, line)
            continue
    #we need to examine its elements
    elements = line.split()
    if len(elements) == 0:
        continue
    foundCell = None
    #we pop the ip address off the start
    ipAddr = elements.pop(0)
    firstName = elements[0]
    otherElements = ""
    foundACell = False
    #for the other elements in the list
    for element in elements:
        otherElements = otherElements+element+" "
        #we are going to search to see if it exists
        try:
            cell = worksheet.find(element)
        except gspread.exceptions.CellNotFound:
            continue
        #if it does exist, we need to store it in foundCell and then quit this loop
        if not foundACell:
            foundCell = cell
            foundACell = True
            break
    #format the output
    output = ipAddr+"="+otherElements
    #if we found something
    if foundACell:
        #update the cell we found
        worksheet.update_cell(foundCell.row, updateColumn, output)
        
        val = worksheet.cell(foundCell.row, interfaceColumn).value
        
        #if nothing is here, we may as well update it.
        if val is "":
            worksheet.update_cell(foundCell.row, interfaceColumn, ipAddr)
            
    else:
        #make a new row and add it to it
        worksheet.add_rows(1)
        rowToAddTo = worksheet.row_count
        worksheet.update_cell(rowToAddTo, updateColumn, output)
        worksheet.update_cell(rowToAddTo, interfaceColumn, ipAddr)
        worksheet.update_cell(rowToAddTo, 1, firstName)
        