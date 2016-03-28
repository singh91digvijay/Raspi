from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context
from django.shortcuts import render
from StringIO import StringIO
from zipfile import ZipFile
import urllib2
import sqlite3
import requests
import csv
from glob import glob;
from os.path import expanduser
from django.shortcuts import *
import cmd
import sys

def index(request):
    hosts = 0
    try:
        db = sqlite3.connect(r'C:\Users\Administrator\Desktop\Raspi\mysite\newdb.db')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM connhistory')
        data = cursor.fetchall()
        cursor.execute('SELECT ip, name FROM connhistory WHERE status="Active";')
        data1 = cursor.fetchall()
        cursor.execute('SELECT max(hostid) FROM connhistory WHERE status="Active";')
        hosts = cursor.fetchone()[0]

        for i in range(len(data1)):
            data1[i] = list(data1[i])
            data1[i].insert(0, i+1)
            hosts = data1[-1]
        hosts = len(data1)
        print hosts
        context = {'data1': data1, 'data': data, 'HOSTS': hosts}
        cursor.close()
        db.close()
    except Exception as e:
        context = {'HOSTS': str(e)}

    return render(request, 'personal/home.html', context)

def logs(request):
    db = sqlite3.connect(r'C:\Users\Administrator\Desktop\Raspi\mysite\newdb.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM connhistory')
    data = cursor.fetchall()

    with open("data.csv", 'wb')as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(list(row))

    with open("data.csv", 'rb')as csvfile:
        data = csvfile.read()
                    
    in_memory = StringIO()
    zip = ZipFile(in_memory, "a")
    zip.writestr("data.csv",data)
    zip.close()
                    
    response = HttpResponse(content_type="application/zip;")
    response["Content-Disposition"] = "attachment; filename=zipfiles.zip"

    in_memory.seek(0)
    response.write(in_memory.read())
    return response



    
   
