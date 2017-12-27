#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import sys
import sqlite3 as lite
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def printElm(element, inserted):
  if inserted == 1:
    print '[P] '+ element['created_at'] + ", " + element['type'] + ", " + element['actor']['display_login'] + ", " + element['repo']['name']
  else:
    print '[+] '+ element['created_at'] + ", " + element['type'] + ", " + element['actor']['display_login'] + ", " + element['repo']['name']

def checkElm(c, con, element):
  c.execute("SELECT * FROM events WHERE repo = :repo LIMIT 0,1", {"repo": element['repo']['name']})
  con.commit()
  row = c.fetchone()
  return row

def insertElm(c, con, element):
  c.execute("INSERT INTO events (user, repo, event, data) VALUES(:user, :repo, :event, :data)", {
    "user": element['actor']['display_login'],
    "repo": element['repo']['name'],
    "event": element['type'],
    "data": element['created_at']
  })
  con.commit()

def getFeed(url):
  try:
    response = requests.get (url, allow_redirects=False, timeout=7, verify=False)
    data = json.loads(response.text)
    con = None
    try:
      con = lite.connect('~/gitevents.sdb')
      c = con.cursor()
      sql = 'create table if not exists events (id INTEGER PRIMARY KEY AUTOINCREMENT, user text NOT NULL, repo text NOT NULL, event text NOT NULL, data text)'
      c.execute(sql)
      con.commit()

      for element in data:
        with con:
          row = checkElm(c, con, element)
          if row:
            printElm(element, 1)
          else:
            insertElm(c, con, element)
            printElm(element, 0)
    finally:
      if con:
        con.close()


  except Exception as e:
    print e

def main (argv):
  URL = 'https://api.github.com/users/' + argv[0] + '/received_events/public'
  getFeed(URL)

if __name__ == "__main__":
  main(sys.argv[1:])
