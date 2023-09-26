import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd
from tkinter import *
from tkinter import ttk
import time
import sys
import csv

zamanklasor = datetime.today()
durum = (zamanklasor.day , "-" , zamanklasor.month , "-" , zamanklasor.year)
durum1 = " ".join([str(item) for item in durum])
durum2 = os.path.exists(durum1)
path = "klasor"
resim = []
SınıfIsimleri = []
listem1 = os.listdir(path)

if durum2 == True:
    root = Tk()
    root.geometry("300x100")
    root.resizable(width=False, height=True)
    root.title('Uyarı!')
    yazi = Label(root, text="GÜN İÇERİSİNDE 1 KEZ KULLANABİLİRSİNİZ")
    yazi.pack()
    root.mainloop()
    sys.exit()
    
elif durum2 == False:
    bulunan_yer = os.getcwd()
    
    ogrenciler = pd.read_csv("ogrenci.csv")
    
    os.mkdir(durum1)
    os.chdir(durum1)
       
    olustur1 = open('gelenler.csv','w+')
    olustur1.write("AD SOYAD, ZAMAN")
    olustur2 = open('gelmeyen.csv','w+')
    olustur2.write("AD SOYAD")
    olustur1.close()
    olustur2.close()
    bulunan_yer2 = os.getcwd()
    os.chdir(bulunan_yer)


class Arayuz:
    
    def Arayuzum():
        os.chdir(bulunan_yer)
        root = Tk()


        root.geometry("300x500")
        root.resizable(width=False, height=False)


        notum = ttk.Notebook(root)

        sekme1 = Frame(notum)
        sekme2 = Frame(notum)
        sekme3 = Frame(notum)

        notum.add(sekme1, text="Öğrenciler")
        notum.add(sekme2, text="Gelen Öğrenciler")
        notum.add(sekme3, text="Gelmeyen Öğrenciler")

        notum.pack(expand=True,fill="both")
        with open("ogrenci.csv", newline = "") as file:
           okuyucu = csv.reader(file)

           r = 0
           for col in okuyucu:
              c = 0
              for row in col:
                 label = Label(sekme1, width = 42, height = 2, \
                                       text = row, relief = RIDGE)
                 label.grid(row = r, column = c)
                 c += 1
              r += 1
        
        os.chdir(durum1)    
        with open("gelenler.csv", newline = "") as file:
           okuyucu = csv.reader(file)

           r = 0
           for col in okuyucu:
              c = 0
              for row in col:
                 label = Label(sekme2, width = 20, height = 2, \
                                       text = row, relief = RIDGE)
                 label.grid(row = r, column = c)
                 c += 1
              r += 1

        with open("gelmeyen.csv", newline = "") as file:
           okuyucu = csv.reader(file)

           r = 0
           for col in okuyucu:
              c = 0
              for row in col:
                 label = Label(sekme3, width = 42, height = 2, \
                                       text = row, relief = RIDGE)
                 label.grid(row = r, column = c)
                 c += 1
              r += 1
        
        root.mainloop()

class Proje:
    

#    def olanOgrenciler():
#        ogrenciler = pd.read_csv('ogrenci.csv')
#        print(ogrenciler)
#        
#    def gelenOgrenciler():
#        gelenler = pd.read_csv('gelenler.csv')
#        print(gelenler)

    def findEncodings(resim):
        encodeList = []
        for img in resim:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def gelen_yaz(isimler):
        #time.sleep(4)
        os.chdir(bulunan_yer2)
        with open('gelenler.csv','r+') as f:
            veri_listem = f.readlines()
            #print(veri_listem)
            verilerim = []
            for satir in veri_listem:
                giris = satir.split(',')
                verilerim.append(giris[0])
            if isimler not in verilerim:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{isimler},{dtString}')
                       
    def Gelmeyen_ogrenci():
        #time.sleep(4)
        os.chdir(bulunan_yer2)
        #ogrenciler = pd.read_csv('ogrenci.csv')
        gelenler = pd.read_csv('gelenler.csv')
        gelmeyen1 = gelenler["AD SOYAD"]
        sonuc = ogrenciler.merge(gelmeyen1, indicator=True, how='outer').loc[lambda v: v['_merge'] != 'both']
        sonuc1 = sonuc["AD SOYAD"]
        sonuc1.to_csv("gelmeyen.csv",index=False)
        gelmeyenn = pd.read_csv('gelmeyen.csv')
        #print(sonuc)
        
for cl in listem1:
    curImg = cv2.imread(f'{path}/{cl}')
    resim.append(curImg)
    SınıfIsimleri.append(os.path.splitext(cl)[0])
 
kod_listem = Proje.findEncodings(resim)

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(kod_listem,encodeFace)
        faceDis = face_recognition.face_distance(kod_listem,encodeFace)
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]:
            isimler = SınıfIsimleri[matchIndex].upper()
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,isimler,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            Proje.gelen_yaz(isimler)
    if cv2.waitKey(1) & 0XFF == ord("q"):
        cv2. destroyAllWindows() 
        break
            
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)
    
#print(Proje.olanOgrenciler())
#print(Proje.gelenOgrenciler())
Proje.Gelmeyen_ogrenci()
time.sleep(3)
Arayuz.Arayuzum()
os.chdir(bulunan_yer)