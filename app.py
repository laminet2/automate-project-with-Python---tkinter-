from tkinter import *
import os
try:
    from PIL import Image,ImageTk
except ImportError:
    os.system("pip install pillow")
    from PIL import Image,ImageTk
from tkinter import messagebox
from collections import Counter
import _function as fc

Automate=[set(),[],dict(),set(),set()] #etat ,alphabet,Table de transition,initaux,acceptant
AFD=False

root=Tk()
root.title("Simulateur d'Automate")


#Taille de la fenetre racine et son emplacement au lancement 
window_width = 754
window_height = 521
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y-40}")


def automateValide(automate):
    #etat,alphabet,t,initaux,acceptant
    (nbrEtat,alphabet,t,initiaux,acceptant)=automate

    try:
        nbrEtat=int(nbrEtat)
        initiaux=list(map(int, initiaux.split(',')))
        acceptant=list(map(int, acceptant.split(',')))
    except Exception:
        print("initiaux et accepetant pas en chiffre")
        return False
    
    alphabet=alphabet.split(",")
    compteur=Counter(alphabet)
    for i in compteur:
        if(compteur[i]>1):
            print("2 lettre de l'alphabet sont identiques")
            return False

    if (nbrEtat==0 or len(alphabet)==0 or len(initiaux)==0 or len(acceptant)==0):
        print("longueur = 0")
        return False
    else:
        for i in initiaux:
            if(i>nbrEtat or i==0):
                print("nbr d'etat initaux> 0 ")
                return False
        for i in acceptant:
            if(i>nbrEtat or i==0):
                print("nbr d'etat initaux> 0 ")
                return False
    return True

def verificationAutomate(automate,popupWindows):
    if(automateValide(automate)):
        messagebox.showinfo("Automate Valide","Vous pouriez l'enregistrer sans compromis")

    else:
        #messagebox.showwarning("Automate Invalide","Veuillez respecter la note susmentionner,tout les \nchamps sont obligatoires et saisisez \ndes chiffres pour les etats et veuillez a ce \nque ces chiffres inférieur au nommbre d'Etat,\negelement ne saisissez pas deux lettre \nidentique pour l'alphabet")
        messagebox.showwarning("Automate Invalide","Veuillez respecter la note susmentionner,tout les \nchamps sont obligatoires et saisisez des \nchiffres pour les etats en respectant\nles régles d'écriture d'automate")

    popupWindows.focus_set()    

def enregistrerAutomate(automate,popupWindows):
    global Automate,AFD
    (nbrEtat,alphabet,t,initiaux,acceptant)=automate

    if(automateValide(automate)):
        nbrEtat=int(nbrEtat)
        initiaux=set(map(int, initiaux.split(',')))
        acceptant=set(map(int, acceptant.split(',')))
        alphabet=set(alphabet.split(","))
        Automate=({i for i in range(1,nbrEtat+1)},alphabet,t,initiaux,acceptant)

        #A Transformer en toast notification
        if(len(initiaux)>1):
            messagebox.showinfo("Automate Enregistrer","AFN enregristrer avec success")
            AFD=False
        else:
            messagebox.showinfo("Automate Enregistrer","Votre Automate a ete rengistrer avec succes")
        popupWindows.destroy()
        
    else:
        messagebox.showwarning("Automate Invalide","Veuillez respecter la note susmentionner,tout les \nchamps sont obligatoires et saisisez des \nchiffres pour les etats en respectant\nles régles d'écriture d'automate")
        popupWindows.focus_set()

def automateWindows(root):
    global window_width,window_height,Automate
    popup_widht=window_width-409
    popup_height=window_height-230
    x,y=((screen_width - popup_widht) // 2),((screen_height - popup_height) // 2)

    popupWindows=Toplevel(root)
    popupWindows.title("Definisions Automate")
    popupWindows.geometry(f"{popup_widht}x{popup_height}+{x}+{y-40}")

    frame=Frame(popupWindows,width=popup_widht)
    noteFrame=LabelFrame(frame,text="A noter")
    noteFrame.grid(row=0,column=0,pady=2)
    label1=Label(noteFrame,text="A noter, afin de mentionner plusieurs états,veuillez les séparer \npar des virgules. Par ailleurs pas besoins de specifier si \nl’automate fini est deterministe (AFD) ou non (AFN)",justify='left')
    label1.pack()

    automateFrame=Frame(frame)
    automateFrame.grid(column=0,row=1,pady=20)

    text1=Label(automateFrame,text="Alphabet")
    text1.grid(column=0,row=0,padx=5)
    text2=Label(automateFrame,text="Nombre d'etat")
    text2.grid(column=1,row=0,padx=5)
    text3=Label(automateFrame,text="Etat(s) initial(aux)")
    text3.grid(column=0,row=2,padx=5)
    text4=Label(automateFrame,text="Etat(s) acceptant(s)")
    text4.grid(column=1,row=2,padx=5)

    alphabet=Entry(automateFrame)
    alphabet.insert(0,(','.join(list(Automate[1])))) 
    alphabet.grid(column=0,row=1,padx=5)

    # Variable pour stocker la valeur de la Spinbox
    spinbox_value = IntVar(value=len(Automate[0]))
    nbrEtat=Spinbox(automateFrame,from_=0,to=100,textvariable=spinbox_value)

    nbrEtat.grid(row=1,column=1,padx=5)
    etatInitiaux=Entry(automateFrame)
    etatInitiaux.insert(0,(','.join(map(str,list(Automate[3])))))
    etatInitiaux.grid(row=3,column=0,padx=5)
    etatAcceptant=Entry(automateFrame)
    etatAcceptant.insert(0,(','.join(map(str,list(Automate[4])))))
    etatAcceptant.grid(row=3,column=1,padx=5)


    buttonFrame=Frame(frame)
    buttonFrame.grid(column=0,row=2)
    cancelButton=Button(buttonFrame,text="Annuler",command=popupWindows.destroy)
    cancelButton.grid(column=0,row=0) 
    verificationButton=Button(buttonFrame,text="Verifier\n Automate Valide",command=lambda:verificationAutomate([nbrEtat.get(),alphabet.get(),[],etatInitiaux.get(),etatAcceptant.get()],popupWindows))
    verificationButton.grid(column=1,row=0,pady=15,padx=15)
    validateButton=Button(buttonFrame,text="Enregistrer",command=lambda:enregistrerAutomate([nbrEtat.get(),alphabet.get(),[],etatInitiaux.get(),etatAcceptant.get()],popupWindows))
    validateButton.grid(column=2,row=0)
    frame.pack()
    popupWindows.mainloop()

#--------- ACCEUILL --------------
## MENU

#-Menu principal
rootMenu=Menu(root)
automate_menu=Menu(rootMenu,tearoff=0)
transition_menu=Menu(rootMenu,tearoff=0)

rootMenu.add_cascade(label="Automate",menu=automate_menu)
rootMenu.add_cascade(label="Table de transition",menu=transition_menu)

#-Transition Menu
transition_menu.add_command(label="Afficher la Table de transitions")
transition_menu.add_separator()
transition_menu.add_command(label="Modifier/mettre a jour la table")
#-Automate menu
automate_menu.add_command(label="Definir/modifier un automate",command=lambda:automateWindows(root))
root.config(menu=rootMenu)

# BACKGROUND
bg=Image.open("images/bg.jpg")
resizedPictures=bg.resize((window_width,window_height))
convertedImage=ImageTk.PhotoImage(resizedPictures)
bgimage=Label(root,image=convertedImage)
bgimage.place(relheight=1,relwidth=1)

#- TEXTE LAYOUT

texteEntrer = Label(root, text="SIMULATEUR D'AUTOMATE",font=("Lato",24,"bold"))
texteEntrer.pack(padx=20, pady=40)

# - Layout that start with recommendatation
recommendation=Canvas()
#recommendation.pack()
subtext=Label(recommendation,text="AVANT DE POUVOIR ANALYSER UN MOT,\n VEUILLEZ RESPECTER CES ETAPES",font=("Helvetica Light",12),justify="center")
subtext.pack()

frame1=Frame(recommendation,height=window_height-368,padx=100)

#column 1
picture11=ImageTk.PhotoImage(Image.open("icons/number1.png").resize((74,76)))
picture1=Label(frame1,image=picture11)
picture1.grid(row=0,column=0,padx=10,pady=5)
text1=Label(frame1,text="DEFINISER UN\n AUTOMATE",justify="center")
text1.grid(row=1,column=0)

#column 2
picture12=ImageTk.PhotoImage(Image.open("icons/number2.png").resize((74,76)))
picture2=Label(frame1,image=picture12)
picture2.grid(row=0,column=1,padx=10,pady=5)
text2=Label(frame1,text="MODIFIER LA TABLE\n DE TRANSITION",justify="center")
text2.grid(row=1,column=1,padx=10)

#column 3
picture13=ImageTk.PhotoImage(Image.open("icons/check.png").resize((74,76)))
picture3=Label(frame1,image=picture13)
picture3.grid(row=0,column=2,padx=10,pady=5)
text3=Label(frame1,text="ANALYSER LE \n MOT",justify="center",font=("Lato",10,"bold"),fg="#32B55E")
text3.grid(row=1,column=2)
frame1.pack()



# Layout with the champ  mot a analyser


#Function systeme
def renitianiliser_saisie():
    #Il manque a renitialisez la fonction de traitement des mots
    #effacer et depackager la zone de dessein
    #effacer et depackager le sort du mot
    wordToAnalyse.delete(0, 'end')


#champ saisir mot
champ_analyse=Canvas(root)
champ_analyse.pack()
champMotAnalyse=Frame(champ_analyse,width=window_width-285,height=43)
texte1=Label(champMotAnalyse,text="ENTRER LE MOT A ANALYSER",font=('Inter Light',13))
texte1.grid(column=0,row=0,padx=30,pady=20)

wordToAnalyse=Entry(champMotAnalyse)
wordToAnalyse.grid(column=1,row=0,padx=5)

iconeNext=ImageTk.PhotoImage(Image.open("icons/next.png").resize((27,25)))
nextButton=Button(champMotAnalyse,image=iconeNext)
nextButton.grid(row=0,column=2,padx=5)

iconeRenitialiser=ImageTk.PhotoImage(Image.open("icons/reset.png").resize((27,25)))
renitianilserButton=Button(champMotAnalyse,image=iconeRenitialiser,command=renitianiliser_saisie)
renitianilserButton.grid(row=0,column=3,padx=5)

#champ dessein
sectionDessein=Canvas(root,width=window_width-108,height=window_height-250,bg='white')
sectionDessein.pack()
#Background section dessein
# bg2 = ImageTk.PhotoImage(Image.open("images/RectangleBlur.png").resize((window_width-108,window_height-250)))
# sectionDessein.create_image(0, 0, anchor="nw", image=bg2)

#champ mot refuser ou accepter
sectionSortDuMot=Canvas(root,width=window_width-484,height=34,bg='red')
sortDuMot=Label(sectionSortDuMot, width=30,font=('Lato',14,'bold'),fg='white',bg='red')
sortDuMot["text"]="Mot accepter"
sectionSortDuMot.pack()
sortDuMot.pack()

champMotAnalyse.pack()
root.mainloop()