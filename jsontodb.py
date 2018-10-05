#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*- 
import json
import sqlite3
import os
import time
import datetime
import random

#tarkistaa jos tietokanta tiedosto loytyy, jos ei tekee ohjelma seuraavan tiedoston:
#(numero 1-9999 valilla)_date_(vuosi)_(kuukausi)_(paiva)_time_(tunti)_(minuutti)_(sekuntti)_dbfile.db tiedoston

def database_check():
    f = os.chdir("xxx")
    global database_checked_name
    want = lambda f: os.path.isfile(f) and f.endswith(".db")
    valid_files = [f for f in os.listdir(os.curdir) if want(f)]
    if len(valid_files) == 0:
        unixinfo = time.time()
        randomID = str(random.randint(1, 9999))+("_")
        unixdb = str(randomID + datetime.datetime.fromtimestamp(unixinfo).strftime("date_" + "%Y_%m_%d" + "_time_" "%H_%M_%S" + "_dbfile.db")) 
        conn = sqlite3.connect(unixdb)
        c = conn. cursor()
        c.execute("CREATE TABLE IF NOT EXISTS tunnistus(unix REAL, status TEXT, artist_name TEXT, song_name TEXT, album_release_date TEXT, label TEXT, album_name TEXT, acrid TEXT, timestamp_1 TEXT)")
        c.close()
        conn.close()

    for filename in valid_files:
        pass
        

#etsii tietokannan nimea

def database_name_lookup():
    f = os.chdir("xxx")
    global database_name
    want = lambda f: os.path.isfile(f) and f.endswith(".db")
    valid_files = [f for f in os.listdir(os.curdir) if want(f)]
    if len(valid_files) == 0:
        exit()
    for filename in valid_files:
        database_name = filename
        
#etsii .json tiedostoja, jos ei loyda .json tiedoston, lopettaa ohjelman
#jos loytaa .json tiedoston, menee data_entry:yn ja kuin tama on valmis, poistaa kyseisen .json tiedoston

def json_file_lookup():
    f = os.chdir("xxx")
    global jsonfile
    want = lambda f: os.path.isfile(f) and f.endswith(".json")
    valid_files = [f for f in os.listdir(os.curdir) if want(f)]
    if len(valid_files) == 0:
        exit()
    for filename in valid_files:
        jsonfile = filename
        data_entry()
        json_file_delete()
        json_file_lookup()
        

#lukee ensiksi tiedoston, taman jalkeen ottaa arvot tietyltä paikoilta .json tiedostosta
#taman jalkeen lisaa otetut JSON arvot ja lisää ne tietokantaan
#jos ei loyda arvoja tietylta paikalta, lisaa no data arvon

def data_entry():
        with open (jsonfile) as f:
            data = json.load(f)
            unix_data = time.time()

            try:
                status_data = (data["status"]["msg"])
            except KeyError:
                status_data = "no data"
            else:
                pass

            try:
                artist_name_data = (data["metadata"]["music"][0]["artists"][0]["name"])
            except KeyError:
                artist_name_data = "no data"
            else:
                pass

            try:
                song_name_data = (data["metadata"]["music"][0]["title"])
            except KeyError:
                song_name_data = "no data"
            else:
                pass

            try:
                album_release_date_data = (data["metadata"]["music"][0]["release_date"])
            except KeyError:
                album_release_date_data = "no data"
            else:
                pass

            try:
                label_data = (data["metadata"]["music"][0]["label"])
            except KeyError:
                label_data = "no data"
            else:
                pass

            try:
                album_name_data = (data["metadata"]["music"][0]["album"]["name"])
            except KeyError:
                album_name_data = "no data"
            else:
                pass

            try:
                acrid_data = (data["metadata"]["music"][0]["acrid"])
            except KeyError:
                acrid_data = "no data"
            else:
                pass

            try:
                timestamp_data = (data["metadata"]["timestamp_utc"])
            except KeyError:
                timestamp_data = "no data"
            else:
                pass


            c.execute("INSERT INTO tunnistus (unix, status, artist_name, song_name, album_release_date, label, album_name, acrid, timestamp_1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (unix_data, status_data, artist_name_data, song_name_data, album_release_date_data, label_data, album_name_data, acrid_data, timestamp_data))
            conn.commit()

#poistaa json tiedoston
def json_file_delete():
    os.remove(jsonfile)


database_check()
database_name_lookup()
conn = sqlite3.connect(database_name)
c = conn.cursor()
json_file_lookup()
#sulkee yhteydet tietokantaan
c.close()
conn.close()
