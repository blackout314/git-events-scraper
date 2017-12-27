import falcon
import sqlite3 as lite

class GitEvents:
  def getElm(self, c, con, start, numbers):
    c.execute("SELECT * FROM events ORDER BY id DESC LIMIT :start,:num", {'start': start, 'num': numbers})
    con.commit()
    #row = c.fetchone()
    rows = c.fetchall()
    return rows

  def on_get(self, req, resp, start, numbers):
    """Handles GET requests"""
    try:
      con = lite.connect('~/gitevents.sdb')
      c = con.cursor()
      rows = self.getElm(c, con, start, numbers)
      event = {
        'repo': rows
      }
    finally:
      if con:
        con.close()

    resp.media = event 

api = falcon.API()
api.add_route('/events/{start}/{numbers}', GitEvents())
