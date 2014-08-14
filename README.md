google-spreadsheet-dns
======================

This is a set of tools to manage DNS using google spreadsheet files as a storage medium. We use "Inventory" sheets at customers which makes for an easy way to keep track of their assetts, and what better way to keep it all up to date than to have these tools automatically "pull" the updates from the user and populate them into DNS. Instant service gratification!

the scripts can be run under cron, we recommend placing them under your current file monitoring systems control. (scripted splunk input for example.. we even provide handy time stamps for easy splunk / sumologic digestion.)

__hostmaker.py__
 
 generates a temporary "hosts" file from a google spreadsheet, verifies that the amount of "change" is not beyond 10%  and then moves the hosts file into place. You specify the google "sheet" and it assumes you will have a column labeled "DNS Entries" it will use to populate the entries. Multiple entries are allowed per column (just stick them on seperate lines) "Command-Enter" on OSX will keep you in the same cell and get you to a new line.

__host_prefix.txt__

 is a standard file to place at the top of the hosts file. Hosts (under ubuntu for example) not only like their localhost (127.0.0.1) entry but a local name (127.0.1.1) entry as well for the local host. rather than have complex logic associated with divining (and possibly incorrectly) this entry, you just code it in for a given host (and any entries you want every time.)

__hostUpdater.py__

 updates a google spreadsheet from a hosts file by appending to the end of the spreadsheet. (doesn't merge) This is a great way to take your current DNSMasq driven host file and start populating your "inventory" sheet without the labor.

Both scripts assume the file is at /etc/hosts



To use, one must have a google account with a Google Spreadsheet (Google Drive) with a Column labeled "DNS Entries" (case sensitive) 

The basic syntax that one must adhere to is this:

1) a column should be named "DNS Entries" that will hold entries that go into the hosts file. In this column,
entries are <IPAddress>=<Hostname> <Alias> <Alias>... This is the only column that hostmaker.py uses.
1b) multiple entries can be seperated by "Command-Enter for multiple rows within the cell of the spreadsheet"


2) HostUpdater.py will use the first column in the row to set the hostname, a column called "interfaces" and the
DNS Entries Column to write information to.


for example (a nice entry) would include: 
192.168.1.1=myRouter.my-house.com myRouter
192
