google-spreadsheet-dns
======================

This is a set of scripts to manage DNS using google spreadsheet files as a storage medium.

hostmaker.py creates a hosts file from a google spreadsheet and tries to put it in (designed to do headless updates)

hostUpdater.py updates a google spreadsheet from a hosts file.

Both scripts assume the file is at /etc/hosts

To use it, one must have a google account and be using google drive

The basic syntax that one must adhere to is this:

a column should be named "DNS Entries" that will hold entries that go into the hosts file. In this column,
entries are denoted as <IPAddress>=<Hostname> <Alias> <Alias>... This is the only column that hostmaker.py uses.

HostUpdater.py will use the first column in the row to set the hostname, a column called "interfaces" and the
DNS Entries Column to write information to.
