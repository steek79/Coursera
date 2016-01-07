#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import sqlite3


conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
# 初期化後4つのテーブルを作る
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')


fname = raw_input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'Library.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
# <key>Genre</key><string>Rock</string>

# d の <key> が key のところの内容を返す
def lookup(d, key):
    found = False
    for child in d:
        if found: return child.text
        if child.tag == 'key' and child.text == key: # <key> の中身が key(<-変数) なら
            found = True
    return None


stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict') # 3つ目の階層なので
print 'Dict count: ', len(all)
for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    genre = lookup(entry, 'Genre') # 上の関数をつかってそれぞれ入れる

    if name is None or artist is None or album is None or genre is None:
        continue # 揃ってなければ無視

    print name, artist, album, genre
    # 得た4つの変数をテーブルにinsert

    # 参照先から追加してく感じ
    cur.execute(''' INSERT OR IGNORE INTO Artist (name)
        VALUES ( ? )''', (artist, ) ) # artist の名前がなければ追加、あれば何もなし
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, )) # その artist にふられた id を選択
    artist_id = cur.fetchone()[0] # artist_id としてとっておく

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id)
        VALUES ( ?, ? )''', ( album, artist_id ) ) # アルバムタイトル／アーティスト
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, )) # アルバムにふられた id 選択
    album_id = cur.fetchone()[0] # album_id としてとっておく

    cur.execute('''INSERT OR IGNORE INTO Genre (name)
        VALUES ( ? )''', (genre, ) )
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ) )
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT  OR REPLACE INTO Track
        (title, album_id, genre_id)
        VALUES (?, ?, ?)''', # なければ追加、あれば更新
        ( name, album_id, genre_id ) )

    conn.commit()
