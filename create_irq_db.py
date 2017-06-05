#!/usr/bin/env python
# Filename create_irq_db.py

""" Creates irq database from the provided proc interrupts file """

__author__ = "Adam R. Dalhed"
__version__ = "0.0.1"


import sqlite3
conn = sqlite3.connect('irq.db')
c = conn.cursor()
try:
	c.execute('''create table irqs (id int, cpu0 int, cpu1 int, date date)''')
except:
	print("table already exists")

#myjson = {}
myproc=open("proc_interrupts","r")
for line in myproc:
	if line.find("eth") != -1:
		a=line.split()
		my_id=int(a[0].rstrip(":"))
		c.execute("insert into irqs values (?, ?, ?, ?)",(my_id, a[1],a[2], '2017-03-25'))
myproc.close()

s = conn.execute("SELECT id, cpu0, cpu1, date from irqs")
for row in s:
   print "ID = ", row[0]
   print "CPU0 = ", row[1]
   print "CPU1 = ", row[2]
   print "DATE = ", row[3], "\n"

print "Operation done successfully";
conn.commit()
conn.close()
