import tkinter

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
