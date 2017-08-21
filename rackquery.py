#!/usr/bin/python
'''This script will take either a hostname or IP address, and query our Racktables database for information. 
    Tab completion is available if you can't quite remember the hostname. Passing a portion of a hostname 
    will render a list of all device hostnames that contain that string, IE passing 'amout' will output data for amout05-9.
    You must populate config.txt with credentials and IP for racktable_db which can be acquired on the wiki.'''

from __future__ import print_function
import ConfigParser
import readline
import MySQLdb


class MyCompleter(object):

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0: 
            if text: 
                self.matches = [s for s in self.options
                                if s and s.startswith(text)]
            else:  
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None

def config():
    config = ConfigParser.ConfigParser()
    config.read("config")
    user = config.get("config","user")
    passwd = config.get("config", "password")
    host = config.get("config", "host")
    return user, passwd

def connection(user, passwd):
    conn = MySQLdb.connect(host = rackdbip,
                            user = user,
                            passwd = passwd,
                            db = "racktables_db")
    c = conn.cursor()
    return c, conn
        
def make_dict(rackdata):
    d={}
    for name, ipaddr in rackdata:
        d.setdefault(name, ipaddr)
    return d

def main():

    user, passwd = config()
    
    c, conn = connection(user, passwd)
    c.execute("select name, INET_NTOA(ip) FROM IPv4Address")
    
    rackdict = make_dict(rackdata = c.fetchall())
    
    completerlist =[]
    for n, i in rackdict.items():
        n = n.lower()
        completerlist.append(n)
    
    completer = MyCompleter(completerlist)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')
    
    query = raw_input("Hostname or IP address: ")
    
    for n, i in rackdict.items():
        n, i, query = n.lower(), i.lower(), query.lower()
        if query in n:
             print('{:<50s} ' ' {}'.format(n, i))
        if query in i:
             print('{:<50s} ' ' {}'.format(i, n))        
    
    c.close()
    conn.close()

if __name__ == '__main__':
    main()