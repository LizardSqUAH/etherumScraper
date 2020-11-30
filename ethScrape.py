#!/usr/bin/env python3

import requests
import lxml
from bs4 import BeautifulSoup

import mariadb
import sys
import time

import base64

def quickGrab(url):
	source = requests.get(url).text

	soup = BeautifulSoup(source, 'lxml')

	#print(soup.prettify())

	#print("-"*100)

	soup.select('input')
	soup.select('.js--converter-quote')
	ethpricetag = soup.find(attrs={"value"})
	#print(ethpricetag)
	#print("-"*100)
	ethprice = ethpricetag.getText()
	return ethprice
	#print(ethprice)

cred_file = open("credentials.txt", 'r')
hostf = cred_file.readline().replace('\n', '')
portf = int(cred_file.readline().replace('\n', ''))
userf = cred_file.readline().replace('\n', '')
passwordf = cred_file.readline().replace('\n', '')

print("hostf " + hostf)
print("portf " + str(portf))
print("userf " + userf)
print("passwordf " + passwordf)

b64_message = 'aHR0cHM6Ly9ldGhlcmV1bXByaWNlLm9yZy8='
b64_bytes = b64_message.encode('ascii')
message_bytes = base64.b64decode(b64_bytes)
message = message_bytes.decode('ascii')

try:
	conn = mariadb.connect(
		user=userf,
		password=passwordf,
		host=hostf,
		port=portf,
		database="TextGuiDB"
	)
	conn.autocommit = True
except mariadb.Error as e:
	print(f"Error connecting to MariaDB Platform: {e}")

cur = conn.cursor()
while True:
	ethprice = quickGrab(message)
	cur.execute("SELECT ID FROM TextGuiDB.UpdateDisplay1 WHERE STRCMP(Title, 'Etherum Value')=0");
	row = cur.fetchall()
	if len(row) == 0:
		cur.execute("INSERT INTO TextGuiDB.UpdateDisplay1 (Title, Data, PostDate) VALUES (?, ?, NOW())", ("Etherum Value" , ethprice))
	else:
		cur.execute("UPDATE TextGuiDB.UpdateDisplay1 SET Data = ?, PostDate = NOW() WHERE ID = ?", (ethprice, row[0][0]))
	time.sleep(60)

#print(cur.execute("INSERT INTO TextGuiDB.UpdateDisplay1 (Data, PostDate) VALUES (?, ?)", (ethprice,"2029-09-19 23:43:11")))
print(ethprice)
print(ethprice)
