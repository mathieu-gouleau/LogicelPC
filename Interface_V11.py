# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 15:12:44 2018

@author: antho

                    ATTENTION!!!
                    
Lancement sur Raspberry :
    
    Passer les lignes suivantes en commentaire:
        import tkinter as Tk
        import tkinter.messagebox as msg
        fenetre.geometry("800x480+350+200")
        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=1,param2=10,maxRadius=20)
        CheminPhoto0="..."
        CheminPhoto1="..."
        CheminPhoto2="..."
    
    Enlever le # des lignes suivantes :
        #import Tkinter as Tk
        #import tkMessageBox as msg
        #import picamera
        #fenetre.attributes('-fullscreen',True)
        #circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=1,param2=10,maxRadius=20)
        #camera.*
        #CheminPhoto0="Photos/Photo0.png"
        #CheminPhoto1="Photos/Photo1.png"
        #CheminPhoto2="Photos/Photo2.png"
"""

import tkinter as Tk
import tkinter.messagebox as msg
#import Tkinter as Tk
#import tkMessageBox as msg
#import picamera
from PIL import Image
from PIL import ImageTk
import numpy as np
from tkinter import filedialog
import firebase
from google.cloud import storage
from google.cloud.storage import client
import pyrebase 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os
import uuid
import cv2




def clean():
    #camera.stop_preview()
    for item in fenetre.winfo_children():
        item.place_forget()
    bouton_home.place(x=bouton_home_x,y=bouton_home_y)
    bouton_return.place(x=bouton_return_x,y=bouton_return_y)
    bouton_quit.place(x=bouton_quit_x,y=bouton_quit_y)

def Start():
    #Configuration de la page

    config = {
    "apiKey": "AIzaSyDk9Y_vRsmSB-_keAx-SbGOYncRjgkjbPQ",
    "authDomain": "novastepdb.firebaseapp.com",
    "databaseURL": "https://novastepdb.firebaseio.com",
    "projectId": "novastepdb",
    "storageBucket": "novastepdb.appspot.com",
    "messagingSenderId": "14365121179",
    "appId": "1:14365121179:web:cf2bdb7ff66b931b9a043e",
    "measurementId": "G-PKCX76F1K8"
    }
    global pageActuelle
    global pagePrecedente
    pageActuelle="Accueil"
    pagePrecedente=""
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    storage.child("images/new.jpg").download("jamgeTendue.png")
    storage.child("images/new1.jpg").download("jambePlié.png")    
    
    clean()

    #Items ajoutés
    logoAccueil_label.place(x=logoAccueil_label_x,y=logoAccueil_label_y)
    bouton_start.place(x=Coord_Bouton_Centr[0],y=Coord_Bouton_Centr[1])


def Home():
    #camera.stop_preview()
    global pageActuelle
    if (pageActuelle!="Accueil"):
        Accueil=msg.askokcancel(title="Retour à l'accueil?",message="Voulez-vous vraiment retourner à l'accueil?")
        if (Accueil) :
            Start()
        #elif (Accueil==False and pageActuelle=="Cadrage"):
            #camera.start_preview(fullscreen=False, window=(120,0,560,350))
    
def Quit():
    #camera.stop_preview()
    Quitter=msg.askokcancel(title='Quitter?',message="Voulez-vous vraiment quitter?")
    if (Quitter) :
        fenetre.destroy()
    #elif (Quitter==False and pageActuelle=="Cadrage"):
        #camera.start_preview(fullscreen=False, window=(120,0,560,350))

def Return():
    print (pageActuelle,pagePrecedente)
    if (pageActuelle=="Cadrage"):
        Home()
    elif (pageActuelle=="Manuelle" and pagePrecedente!="prepaPhoto1" and pagePrecedente!="prepaPhoto2"):
        Cadrage()
    elif ((pageActuelle=="detecRatee" or pageActuelle=="detecOK") and pagePrecedente!="prepaPhoto1" and pagePrecedente!="prepaPhoto2"):
        detecManuelle(CheminPhoto0)
    elif (pageActuelle=="Force"):
        detecOK(CheminPhoto0)
    elif (pageActuelle=="Manuelle" and pagePrecedente=="prepaPhoto1"):
        resultatPhoto1()
    elif (pageActuelle=="prepaPhoto1"):
        pageForce()
    elif (pageActuelle=="resultatPhoto1"or (pageActuelle=="detecRatee" and pagePrecedente=="prepaPhoto1")):
        prepaPhoto1()
    elif (pageActuelle=="prepaPhoto2"):
        resultatPhoto1()
    elif (pageActuelle=="resultatPhoto2" or (pageActuelle=="detecRatee" and pagePrecedente=="prepaPhoto2")):
        prepaPhoto2()
    elif (pageActuelle=="Manuelle" and pagePrecedente=="prepaPhoto2"):
        resultatPhoto2()
    elif (pageActuelle=="resultatFinal"):
        resultatPhoto2()
        

def Cadrage():
    #Configuration de la page
    global pageActuelle
    pageActuelle="Cadrage"
    
    clean()
        
    #Items ajoutés
    #camera.start_preview(fullscreen=False, window=(120,0,560,350))
    #Label_cadrage.place(x=Label_cadrage_x,y=y_label)
    Label_photo1Titre.place(x=Label_photoTitre_x,y=y_titre)
    Label_DocumentChoix.place(x=Label_DocumentChoix_x,y=Label_DocumentChoix_y)
    bouton_valider.place(x=Coord_Bouton_DDroit[0],y=Coord_Bouton_DDroit[1])
    bouton_ChoixDoc.configure(command = Ouvrir,background = couleurNovastep)
    bouton_ChoixDoc.place(x=Coord_Bouton_Gauch[0],y=Coord_Bouton_Gauch[1])
    

def Valider():
    global Force
    print (pageActuelle,pagePrecedente)
    if (pageActuelle=="Cadrage"):
        prendrePhoto()
        detecManuelle(CheminPhoto0)
    elif (pageActuelle=="Manuelle"and pagePrecedente!="prepaPhoto1" and pagePrecedente!="prepaPhoto2"):
        detection(CheminPhoto0)
        bouton_zoomMoins.configure(command = Pass,background = 'grey')
        bouton_zoomPlus.configure(command = ZoomPlus,background = couleurNovastep)
    elif (pageActuelle=="detecOK" and pagePrecedente!="prepaPhoto1" and pagePrecedente!="prepaPhoto2"):
        prendrePhoto()
        resultatPhoto1()
    elif (pageActuelle=="resultatPhoto1"):
        prepaPhoto2()
    elif (pageActuelle=="prepaPhoto2" or pagePrecedente=="prepaPhoto2" and pageActuelle!="resultatPhoto2"):
        prendrePhoto()
        resultatPhoto2()
    elif (pageActuelle=="resultatPhoto2"):
        resultatFinal()

def retry():
    print (pageActuelle,pagePrecedente)
    if (pagePrecedente!="prepaPhoto1" and pagePrecedente!="prepaPhoto2"):
        detecManuelle(CheminPhoto0)
    if (pageActuelle=="detecRatee"and pagePrecedente=="prepaPhoto1"):
        prepaPhoto1()
    if (pageActuelle=="detecRatee"and pagePrecedente=="prepaPhoto2"):
        prepaPhoto2()
    elif (pageActuelle=="resultatPhoto1"):
        prepaPhoto1()
    elif (pageActuelle=="resultatPhoto2"):
        prepaPhoto2()
      
def recalibrer():
    if (pagePrecedente=="prepaPhoto1"):
        detecManuelle(CheminPhoto1)
    elif (pagePrecedente=="prepaPhoto2"):
        detecManuelle(CheminPhoto2)
        
def detecManuelle(CheminPhoto):
    #Configuration de la page
    global pageActuelle
    global pagePrecedente
    global largeur
    global hauteur
    global photo
    global img
    global canvas
    global lineV
    global lineH
    global x,y,x1,y1
    #pagePrecedente="Manuelle"
    pageActuelle="Manuelle"
    
    clean()
    
    #Items ajoutés    
    img = Image.open(CheminPhoto)
    hauteur = img.size[1]
    hauteurVoulue=370
    largeur = (int) (img.size[0]*hauteurVoulue/hauteur)
    img=img.resize((largeur, hauteurVoulue), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    largeur = img.size[0]
    hauteur = img.size[1]
    canvas = Tk.Canvas(fenetre, width = largeur, height = hauteur)
    canvas.create_image(0,0, anchor = Tk.NW, image=photo) 
    canvas.bind('<Button-1>', ReperageCouleur)
    lineV=canvas.create_line(0,0,0,0)
    lineH=canvas.create_line(0,0,0,0)
    
    Label_detecManuelle.place(x=Label_detecManuelle_x,y=y_label)
    canvas.place(x=Photo_x,y=Photo_y)
    canvasCouleur.place(x='15',y='250')
    bouton_valider.place(x=Coord_Bouton_Centr[0],y=Coord_Bouton_Centr[1])
    
    x=largeur/2
    y=hauteur/2
    x1=0
    y1=0
    bouton_zoomPlus.place(x='10',y='100')
    bouton_zoomMoins.place(x='10',y='160')


def ZoomPlus():
    global img
    global x,y,x1,y1
    global hauteur
    global largeur
    global Photo

    zoom=3
    
    if(x<largeur/(2*zoom)):
        x=largeur/(2*zoom)
    elif(x>largeur-largeur/(2*zoom)):
        x=largeur-largeur/(2*zoom)
    if (y<hauteur/(2*zoom)):
        y=hauteur/(2*zoom)
    elif(y>hauteur-hauteur/(2*zoom)):
        y=hauteur-hauteur/(2*zoom)
    x, y = zoom*(x)-largeur/2, zoom*(y)-hauteur/2
    x1,y1=x,y
    print(x,y)
    img=img.resize((largeur*zoom, hauteur*zoom), Image.ANTIALIAS)
    Photo=ImageTk.PhotoImage(img)
    canvas.create_image(-x, -y, anchor='nw', image=Photo)
    bouton_zoomPlus.configure(command = Pass,background = 'grey')
    bouton_zoomMoins.configure(command = ZoomMoins,background = couleurNovastep)

def ZoomMoins():
    global img
    global hauteur
    global largeur
    global Photo
    global x,y,x1,y1
    
    x=largeur/2
    y=hauteur/2
    x1,y1=0,0
    img=img.resize((largeur, hauteur), Image.ANTIALIAS)
    Photo=ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor='nw', image=Photo)
    bouton_zoomMoins.configure(command = Pass,background = 'grey')
    bouton_zoomPlus.configure(command = ZoomPlus,background = couleurNovastep)
    
def Pass():
    pass





def Ouvrir():
    global filename
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select A File", filetype = (("png", "*.png"),("jpeg","*.jpg"),("All Files", "*.*")))
    
def ReperageCouleur(event):
    global couleurReperee
    global canvas
    global img
    global lineV
    global lineH
    global hsv
    global x,y,x1,y1

    canvas.delete(lineV,lineH)
    x, y = event.x+x1, event.y+y1
    couleurReperee=img.getpixel((x,y))[0:3]
    hsv = cv2.cvtColor(np.uint8([[couleurReperee]]),cv2.COLOR_RGB2HSV)[0][0]
    couleurReperee=rgb_to_hex(couleurReperee)
    print("HSV = ",hsv)

    lineV=canvas.create_line(event.x,0,event.x,hauteur)
    lineH=canvas.create_line(0,event.y,largeur,event.y)
    canvasCouleur.create_rectangle(0,0,100,100,fill=couleurReperee)
    
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def detection(CheminPhoto):
    pageAttente()
    traitement_image(CheminPhoto)
    detection_cercle()
    if circles is None :
        detecRatee(CheminPhoto)
    else:
        if (circles.size==9):
            detecOK(CheminPhoto)
        else:
            detecRatee(CheminPhoto)

def pageAttente():
    bouton_valider.place_forget()
    Label_detecManuelle.place_forget()
    Label_Attente.place(x=Label_Attente_x,y=y_label)
    fenetre.update()

def prendrePhoto():
    global CheminPhoto0
    global CheminPhoto1
    global CheminPhoto2
    
    if(pageActuelle=="Cadrage"):
        CheminPhoto0=filename
        #CheminPhoto0="Photos/Photo0.png"
        #camera.capture(CheminPhoto0)
    elif(pageActuelle=="detecOK"):
        CheminPhoto1=filename
        #CheminPhoto1="Photos/Photo1.png"

        #camera.capture(CheminPhoto1)
    elif(pageActuelle=="prepaPhoto2"):
        CheminPhoto2=filename
        #CheminPhoto2="Photos/Photo2.png"
        #camera.capture(CheminPhoto2)
        
def traitement_image(CheminPhoto) :
    global couleurReperee
    global Photo_traitee
    global canvas_photoTraitee
    H=hsv[0]
    S=hsv[1]

    HMin = H-10
    HMax = H+10
    SMin = S-80
    SMax = S+80
    VMin = 80
    VMax = 255
    minHSV = np.array([HMin, SMin, VMin])
    maxHSV = np.array([HMax, SMax, VMax])
    print(minHSV)
    print(maxHSV)
    img = cv2.imread(CheminPhoto)
    # Convert the BGR image to other color spaces
    img = cv2.resize(img,(largeur,hauteur))
    imageHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # Create the mask using the min and max values obtained from trackbar and apply bitwise and operation to get the results               
    maskHSV = cv2.inRange(imageHSV,minHSV,maxHSV)
    resultHSV = cv2.bitwise_and(img, img, mask = maskHSV)

    img_gray=cv2.cvtColor(resultHSV, cv2.COLOR_RGB2GRAY)
    (thresh,img_bw)=cv2.threshold(img_gray,128,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    cv2.imwrite("Photos/Photo_modif.png", img_bw)
    """
    img2 = cv2.imread("Photos/Photo_modif.png")
    rgb=cv2.cvtColor(img2, cv2.COLOR_HSV2RGB)
    img_gray=cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    (thresh,img_bw)=cv2.threshold(img_gray,128,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    cv2.imwrite("Photos/Photo_modif2.png", img_bw)
    """
        
def detection_cercle() :
    global circles
    
    img = cv2.imread("Photos/Photo_modif.png",0)
    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1.20,20,param1=1,param2=10,maxRadius=20)
    print(circles)
    #circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=1,param2=10,maxRadius=20)
    if circles is None : 
        print ("Pas de cercles")
    else :
        circles = np.uint16(np.around(circles))
        print("cercles : ")
        for i in circles[0,:]:
            print(i)
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    cv2.imwrite("Photos/Photo_cercles.png",cimg)

def affichageFinal(CheminPhoto):
    global Photo_finale
    global circles
    
    img = cv2.imread(CheminPhoto)
    img = cv2.resize(img,(largeur,hauteur))
    if circles is None : 
        print ("Pas de cercles")
    else :
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
    cv2.imwrite("Photos/Photo_Finale.png",img)
    img_finale = Image.open("Photos/Photo_Finale.png")
    img_finale=img_finale.resize((largeur, hauteur), Image.ANTIALIAS)
    Photo_finale=ImageTk.PhotoImage(img_finale)
    canvas_photoFinale = Tk.Canvas(fenetre, width = largeur, height = hauteur)
    canvas_photoFinale.create_image(0,0, anchor = Tk.NW, image=Photo_finale) 
    canvas_photoFinale.place(x=Photo_x,y=Photo_y)

def detecOK(CheminPhoto):
    global pageActuelle
    pageActuelle="detecOK"

    clean()
    
    #Items ajoutés
    Label_detecOK.place(x=Label_detecOK_x,y=y_label)
    bouton_retry.place(x=Coord_Bouton_Gauch[0],y=Coord_Bouton_Gauch[1])
    bouton_valider.place(x=Coord_Bouton_Droit[0],y=Coord_Bouton_Droit[1])
    affichageFinal(CheminPhoto)

def detecRatee(CheminPhoto):
    global pageActuelle
    pageActuelle="detecRatee"
    print(pageActuelle,pagePrecedente)

    clean()
    
    #Items ajoutés
    Label_detecRatee.place(x=Label_detecRatee_x,y=y_label)   
    affichageFinal(CheminPhoto)
    if (pagePrecedente=="prepaPhoto1" or pagePrecedente=="prepaPhoto2"):
        bouton_recalibrer.place(x=Coord_Bouton_Droit[0],y=Coord_Bouton_Droit[1])
        bouton_retry.place(x=Coord_Bouton_Gauch[0],y=Coord_Bouton_Gauch[1])
    else :
        bouton_retry.place(x=Coord_Bouton_Centr[0],y=Coord_Bouton_Centr[1])
    
    
def pageForce():
    global pageActuelle
    pageActuelle="Force"
    
    clean()
    
    #Items ajoutés
    Scale_force.place(x=Scale_force_x,y=Scale_force_y)
    bouton_valider.place(x=Coord_Bouton_Centr[0],y=Coord_Bouton_Centr[1])
    Label_force.place(x=Label_force_x,y=Label_force_y)
    bouton_plus.place(x=bouton_plus_x,y=bouton_plus_y)
    bouton_moins.place(x=bouton_moins_x,y=bouton_moins_y)

def Plus():
    v=value.get()
    value.set(v+1)
    
def Moins():
    v=value.get()
    value.set(v-1)

def calcul_angle():
    global angle
    global point1
    global point2
    global cheville
    
    cercle1=circles[0,0]
    x1=(int)(cercle1[0])
    y1=(int)(hauteur-cercle1[1])
    
    cercle2=circles[0,1]
    x2=(int)(cercle2[0])
    y2=(int)(hauteur-cercle2[1])
    
    cercle3=circles[0,2]
    x3=(int)(cercle3[0])
    y3=(int)(hauteur-cercle3[1])
    
    if ((x1>x2 and x1<x3) or (x1<x2 and x1>x3)):
        cheville=(x1,hauteur-y1)
        point1=(x2,hauteur-y2)
        point2=(x3,hauteur-y3)
        vecteur1=(x2-x1,y2-y1)
        vecteur2=(x3-x1,y3-y1)
    elif ((x2>x1 and x2<x3) or (x2<x1 and x2>x3)):
        cheville=(x2,hauteur-y2)
        point1=(x1,hauteur-y1)
        point2=(x3,hauteur-y3)
        vecteur1=(x1-x2,y1-y2)
        vecteur2=(x3-x2,y3-y2)
    else :
        cheville=(x3,hauteur-y3)
        point1=(x1,hauteur-y1)
        point2=(x2,hauteur-y2)
        vecteur1=(x2-x3,y2-y3)
        vecteur2=(x1-x3,y1-y3)
    
    print("cheville : ",cheville)

    norme1=np.sqrt(vecteur1[0]*vecteur1[0]+vecteur1[1]*vecteur1[1])
    norme2=np.sqrt(vecteur2[0]*vecteur2[0]+vecteur2[1]*vecteur2[1])

    angle=float(int(np.arccos((vecteur1[0]*vecteur2[0]+vecteur1[1]*vecteur2[1])/(norme1*norme2))*180/np.pi*100))/100
    print (angle)


    """
Fonction receiveMessages
- Ecriture de la valeur d'intervalle choisie dans un txt
- Ecriture de la valeur de la force choisie dans un txt
- Attente de la réception de l'information par Bluetooth
- Si on reçoit la bonne information, prise de photo
"""

def receiveMessages(CheminPhoto):
    global data
    data_intervalle=open('/home/pi/Desktop/Equinometre/txt/intervalle.txt','w+')
    v=valueIntervalle.get()
    data_intervalle.write(str(v))
    data_intervalle.close()
    data_force=open('/home/pi/Desktop/Equinometre/txt/force.txt','w+')
    v=value.get()
    data_force.write(str(v))
    data_force.close()
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)
    client_sock,address = server_sock.accept()
    data = client_sock.recv(1024)
    client_sock.close()
    server_sock.close()
    if ("OK" in data):
        prendrePhoto(CheminPhoto)  

"""
Fonction sendMessageTo
- Récupération de l'intervalle de force et la force choisis sur la jauge
- Envoi de ces informations au module de mesure de force
"""

def sendMessageTo():
    global Force
    global sock
    global Intervalle
    Intervalle=valueIntervalle.get()
    sock.send((str)(Force)+","+(str)(Intervalle))
    sock.close()
    
"""
Fonction connectTo
- Connexion à la Raspberry du module de mesure de force
"""

def connectTo(targetBluetoothMacAddress):
    global sock
    port = 1
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((targetBluetoothMacAddress, port))



"""
Fonction prepaPhoto1
- Récupération de la force choisie 
- Appel de la fonction clean
- Affichage des différentes information sur l'interface graphique
- Essai de connexion à la Raspberry du capteur de force
- Appel de la fonction sendMessageTo et ReceiveMessages
- En cas d'erreur : appel de la fonction erreurBluetooth
"""

def prepaPhoto1():
    global pageActuelle
    pageActuelle="prepaPhoto1"
    
    clean()
    
    #Items ajoutés
    Label_prepaPhoto1.place(x=Label_prepaPhoto_x,y=Label_prepaPhoto_y)
    bouton_valider.place(x=Coord_Bouton_Centr[0],y=Coord_Bouton_Centr[1])
    Label_photo1Titre.place(x=Label_photoTitre_x,y=y_titre)
    
def resultatPhoto1():
    global pageActuelle
    global pagePrecedente
    global angle
    global angle1
    global Photo_angle1
    pagePrecedente="prepaPhoto1"
    pageActuelle="resultatPhoto1"
    
    pageAttente()
    traitement_image(CheminPhoto1)
    detection_cercle()
    affichageFinal(CheminPhoto1)
    
    clean()
    
    if circles is None :
        detecRatee(CheminPhoto1)
    else:
        if (circles.size==9):
            calcul_angle()
    
            #Items ajoutés    
            image_angle1=cv2.imread("Photos/Photo_Finale.png")
            cv2.line(image_angle1,point1,cheville,(0,255,0),2)
            cv2.line(image_angle1,point2,cheville,(0,255,0),2)
            cv2.imwrite("Photos/Photo_angle1.png",image_angle1)
            img_angle1 = Image.open("Photos/Photo_angle1.png")
            Photo_angle1=ImageTk.PhotoImage(img_angle1)
            canvas_angle1 = Tk.Canvas(fenetre, width = largeur, height = hauteur)
            canvas_angle1.create_image(0,0, anchor = Tk.NW, image=Photo_angle1) 
            canvas_angle1.place(x=Photo_x,y=Photo_y)
            
            angle1=angle
            text_angle1="Angle = "+ (str) (angle1) +"°"
            Label_resultatPhoto1.config(text=text_angle1)
            bouton_retry.place(x=Coord_Bouton_GGauch[0],y=Coord_Bouton_GGauch[1])
            bouton_valider.place(x=Coord_Bouton_DDroit[0],y=Coord_Bouton_DDroit[1])
            bouton_recalibrer.place(x=Coord_Bouton_Centr[0],y=Coord_Bouton_Centr[1])
            Label_resultatPhoto1.place(x=Label_resultatPhoto_x,y=y_label)
        else:
            detecRatee(CheminPhoto1)
    
def prepaPhoto2():
    global pageActuelle
    pageActuelle="prepaPhoto2"
    
    clean()
    
    #Items ajoutés
    Label_prepaPhoto2.place(x=Label_prepaPhoto_x,y=Label_prepaPhoto_y)
    bouton_ChoixDoc.configure(command = Ouvrir,background = couleurNovastep)
    bouton_ChoixDoc.place(x=Coord_Bouton_Gauch[0],y=Coord_Bouton_Gauch[1])
    bouton_valider.place(x=Coord_Bouton_Centr[0],y=Coord_Bouton_Centr[1])
    Label_photo2Titre.place(x=Label_photoTitre_x,y=y_titre)

def resultatPhoto2():
    global pageActuelle
    global pagePrecedente
    global angle
    global angle2
    global Photo_angle2
    pagePrecedente="prepaPhoto2"
    pageActuelle="resultatPhoto2"
    
    pageAttente()
    traitement_image(CheminPhoto2)
    detection_cercle()
    affichageFinal(CheminPhoto2)
    
    clean()
    
    if circles is None :
        detecRatee(CheminPhoto2)
    else:
        if (circles.size==9):
            calcul_angle()
    
            #Items ajoutés
            image_angle2=cv2.imread("Photos/Photo_Finale.png")
            cv2.line(image_angle2,point1,cheville,(0,255,0),2)
            cv2.line(image_angle2,point2,cheville,(0,255,0),2)
            cv2.imwrite("Photos/Photo_angle2.png",image_angle2)
            img_angle2 = Image.open("Photos/Photo_angle2.png")
            Photo_angle2=ImageTk.PhotoImage(img_angle2)
            canvas_angle2 = Tk.Canvas(fenetre, width = largeur, height = hauteur)
            canvas_angle2.create_image(0,0, anchor = Tk.NW, image=Photo_angle2) 
            canvas_angle2.place(x=Photo_x,y=Photo_y)
            
            angle2=angle
            text_angle2="Angle = "+ (str) (angle2) +"°"
            Label_resultatPhoto2.config(text=text_angle2)
            bouton_retry.place(x=Coord_Bouton_GGauch[0],y=Coord_Bouton_GGauch[1])
            bouton_valider.place(x=Coord_Bouton_DDroit[0],y=Coord_Bouton_DDroit[1])
            bouton_recalibrer.place(x=Coord_Bouton_Centr[0],y=Coord_Bouton_Centr[1])
            Label_resultatPhoto2.place(x=Label_resultatPhoto_x,y=y_label)
        else:
            detecRatee(CheminPhoto2)
    

def resultatFinal():
    global pageActuelle
    global pagePrecedente
    global angle1
    global angle2
    pageActuelle="resultatFinal"
    pagePrecedente="resultatFinal"
    
    clean()
    
    #Items ajoutés
    angle_final=float(int(np.abs(angle1-angle2)*100))/100
    text_final="Angle jambe tendue = " + (str)(angle1) + "°" + '\n' + "Angle jambe fléchie = " + (str)(angle2) + "°" + '\n' + '\n' + "Différence d'angle = " + (str)(angle_final) + "°"
    Label_resultatFinal.config(text=text_final)
    Label_resultatFinalTitre.place(x=Label_resultatFinalTitre_x,y=y_titre)
    Label_resultatFinal.place(x=Label_resultatFinal_x,y=Label_resultatFinal_y)
    bouton_home2.place(x=Coord_Bouton_Droit[0],y=Coord_Bouton_Droit[1])
    bouton_RefaireManip.place(x=Coord_Bouton_Gauch[0],y=Coord_Bouton_Gauch[1])
    
def recommencerManip():
    Recommencer=msg.askokcancel(title="Recommencer la manipulation?",message="Voulez-vous vraiment recommencer la manipulation?")
    if (Recommencer) :
        prepaPhoto1()
    

#initialisation caméra
#camera = picamera.PiCamera()
#camera.framerate=float(15)#a accorder avec la vitesse d'acquisition du capteur
#camera.saturation=100
#camera.hflip=True

#Création de la fenêtre del'interface
fenetre = Tk.Tk()
fenetre.geometry("800x480+350+200")
#fenetre.attributes('-fullscreen',True)
fenetre.title('Interface Novastep')
couleurNovastep="#b11556"
couleurBackground="#f5f5f5"
fenetre['bg']=couleurBackground

#Création des images
logoAccueil = Image.open("Images/logoAccueil.png")
logoAccueil_photo = ImageTk.PhotoImage(logoAccueil)
logoAccueil_label=Tk.Label(image=logoAccueil_photo)
logoAccueil_label_x='-75'
logoAccueil_label_y='-150'

IconeAccueil = Image.open("Images/Icone_Home.png")
IconeAccueil=IconeAccueil.resize((50, 50), Image.ANTIALIAS)
IconeAccueil_photo = ImageTk.PhotoImage(IconeAccueil)

IconeRetour = Image.open("Images/Fleche_retour.png")
IconeRetour=IconeRetour.resize((50, 50), Image.ANTIALIAS)
IconeRetour_photo = ImageTk.PhotoImage(IconeRetour)

IconeQuitter = Image.open("Images/Croix.png")
IconeQuitter=IconeQuitter.resize((50, 50), Image.ANTIALIAS)
IconeQuitter_photo = ImageTk.PhotoImage(IconeQuitter)

IconePlus = Image.open("Images/Plus.png")
IconePlus=IconePlus.resize((70, 70), Image.ANTIALIAS)
IconePlus_photo = ImageTk.PhotoImage(IconePlus)

IconeMoins = Image.open("Images/Moins.png")
IconeMoins=IconeMoins.resize((70, 70), Image.ANTIALIAS)
IconeMoins_photo = ImageTk.PhotoImage(IconeMoins)

#Création des boutons
Coord_Bouton_Centr=('315','415')
Coord_Bouton_Gauch=('170','415')
Coord_Bouton_Droit=('470','415')
Coord_Bouton_GGauch=('130','415')
Coord_Bouton_DDroit=('500','415')


bouton_ChoixDoc= Tk.Button(fenetre,text="Ouvrir", command=Ouvrir, fg="white", background = couleurNovastep,
                         height = "1", width = "10",font='size 22')


bouton_home = Tk.Button(fenetre, image=IconeAccueil_photo, command=Home, background = couleurNovastep)
bouton_home_x='0'
bouton_home_y='0'

bouton_return = Tk.Button(fenetre, image=IconeRetour_photo, command=Return, background = couleurNovastep)
bouton_return_x='56'
bouton_return_y='0'

bouton_quit = Tk.Button(fenetre, image=IconeQuitter_photo, command=Quit, background = couleurNovastep)
bouton_quit_x='744'
bouton_quit_y='0'

bouton_start = Tk.Button(fenetre, text="Commencer", command=Cadrage, fg="white", background = couleurNovastep,
                         height = "1", width = "10",font='size 22')

bouton_valider = Tk.Button(fenetre, text="Valider", command=Valider, fg="white", background = couleurNovastep,
                           height = "1", width = "10",font='size 22')

bouton_zoomPlus = Tk.Button(fenetre, text="Zoom +", command=ZoomPlus, fg="white", background = couleurNovastep,
                           height = "1", width = "6",font='size 20')

bouton_zoomMoins = Tk.Button(fenetre, text="Zoom -", command=Pass, fg="white", background = 'grey',
                           height = "1", width = "6",font='size 20')

bouton_retry = Tk.Button(fenetre, text="Réessayer", command=retry, fg="white", background = couleurNovastep, 
                         height = "1", width = "10",font='size 22')

bouton_recalibrer = Tk.Button(fenetre, text="Recalibrer", command=recalibrer, fg="white", background = couleurNovastep, 
                         height = "1", width = "10",font='size 22')

bouton_plus = Tk.Button(fenetre, image=IconePlus_photo, command=Plus, relief='flat', 
                        background = couleurBackground, repeatdelay=500, repeatinterval=50)
bouton_plus_x='710'
bouton_plus_y='205'

bouton_moins = Tk.Button(fenetre, image=IconeMoins_photo, command=Moins, relief='flat', 
                         background = couleurBackground, repeatdelay=500, repeatinterval=50)
bouton_moins_x='15'
bouton_moins_y='205'

bouton_home2 = Tk.Button(fenetre, text="Accueil", command=Home, fg="white", background = couleurNovastep, 
                         height = "1", width = "10",font='size 22')

bouton_RefaireManip = Tk.Button(fenetre, text="Refaire", command=recommencerManip, fg="white", background = couleurNovastep, 
                         height = "1", width = "10",font='size 22')


#Création des labels
y_label='370'
y_titre='50'

Label_DocumentChoix=Tk.Label(fenetre, text="Choisissez une photo jambe tendu et cliquez sur valider", font='-size 20', background = couleurBackground)
Label_DocumentChoix_x='50'
Label_DocumentChoix_y='250'


Label_cadrage=Tk.Label(fenetre, text="Cliquez sur 'Valider' lorsque les 3 points sont visibles à l'écran",
                       font='-size 20', background = couleurBackground)
Label_cadrage_x='20'

Label_detecManuelle=Tk.Label(fenetre, text="Cliquez sur un point sur la photo",
                             font='-size 20', background = couleurBackground)
Label_detecManuelle_x='200'

Label_Attente=Tk.Label(fenetre, text="Veuillez patienter, l'image est en cours de traitement",
                             font='-size 20', background = couleurBackground)
Label_Attente_x='100'

Label_detecRatee=Tk.Label(fenetre, text="Nombre de points trouvés incorrect",
                          font='-size 20', background = couleurBackground)
Label_detecRatee_x='200'

Label_detecOK=Tk.Label(fenetre, text="3 points trouvés. Cela vous convient-il?",
                       font='-size 20', background = couleurBackground)
Label_detecOK_x='170'

Label_force=Tk.Label(fenetre, text="CHOISSISSEZ LA FORCE A APPLIQUER (en kg)",
                     font='-size 22 -weight bold', background = couleurBackground ,fg=couleurNovastep)
Label_force_x='85'
Label_force_y='100'

Label_photo1Titre=Tk.Label(fenetre, text="JAMBE TENDUE",font = '-size 40 -weight bold', 
                           background = couleurBackground,fg=couleurNovastep)

Label_prepaPhoto1=Tk.Label(fenetre, text="METTEZ LE GANT/CHAUSSETTE ET" + '\n' 
                           + "MAINTENEZ LA JAMBE DU PATIENT TENDUE." + '\n' + '\n' 
                           + "PUIS APPLIQUEZ LA FORCE DEMANDEE",font='-size 22', background = couleurBackground)

Label_photo2Titre=Tk.Label(fenetre, text="JAMBE FLECHIE",font = '-size 40 -weight bold', 
                           background = couleurBackground,fg=couleurNovastep)

Label_prepaPhoto2=Tk.Label(fenetre, text="Choisissez une photo jambe fléchi et cliquez sur valider"
                           ,font='-size 22', background = couleurBackground)
Label_photoTitre_x='180'
Label_prepaPhoto_x='50'
Label_prepaPhoto_y='170'

Label_resultatPhoto1=Tk.Label(fenetre, font='-size 20', background = couleurBackground)
Label_resultatPhoto2=Tk.Label(fenetre,font='-size 20', background = couleurBackground)
Label_resultatPhoto_x='320'

Label_resultatFinalTitre=Tk.Label(fenetre, text="RESULTATS",font = '-size 40 -weight bold', 
                                  background = couleurBackground,fg=couleurNovastep)
Label_resultatFinalTitre_x='250'

Label_resultatFinal=Tk.Label(fenetre, font='-size 20', background = couleurBackground)
Label_resultatFinal_x='230'
Label_resultatFinal_y='170'


#Création des scales
global value
value=Tk.DoubleVar()
Scale_force=Tk.Scale(fenetre, from_=0,to=10,showvalue=True,variable=value,tickinterval=1,orient='h',
                     width=70,sliderlength=70,length=600, background = couleurBackground, 
                     highlightbackground = couleurBackground,font='size 22')
Scale_force_x='100'
Scale_force_y='170'
value.set(2)

#Création des canvas*
Photo=Tk.Canvas(fenetre, bg='black', height=350, width=560)
Txt_Photo = Photo.create_text(290, 150, text="Photo/Vidéos", fill = 'white', font="-size 40 -weight bold")
Photo_x='120'
Photo_y='0'

#Création des photos
global couleurReperee
couleurReperee="#386559"

canvasCouleur=Tk.Canvas(fenetre, width = 100, height = 100)
canvasCouleur.create_rectangle(0,0,100,100,fill=couleurReperee)
couleurReperee=hex_to_rgb(couleurReperee)

#Lancement programme
Start()

fenetre.mainloop()