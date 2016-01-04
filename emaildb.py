#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3


conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()
# 'emaildb.sqlite' を触る（なければ作る）

cur.execute('''
DROP TABLE IF EXISTS Counts''') # Counts があればテーブルを消す:初期化
# cur.execute('sqliteへの命令')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''') # org, count の表

fname = raw_input('Enter file name: ')
fh = open(fname)
for line in fh:
    if not line.startswith('From: ') : continue # From: janedoe@gmail.com
    pieces = line.split()
    email = pieces[1]
    org = email.split('@')[1]
    print org

    cur.execute('SELECT count From Counts WHERE org = ?', (org,))
    # org(: col) が org(: mail.com) である列を見つける
    row = cur.fetchone() # その1つを取得(?)
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
            VALUES (?, 1)''', (org,))
            # なければ 'gmail.com, 1' をつくる
    else:
        cur.execute('UPDATE Counts SET count = count+1 WHERE org = ?', (org, ))
            # あれば1足す

conn.commit() # 保存

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
# count で降順ソート10個目まで の org, count
print 'Counts:'
for row in cur.execute(sqlstr):
    print str(row[0]), row[1]

cur.close()
