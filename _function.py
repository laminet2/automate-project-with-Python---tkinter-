def complet():
    global Automate
    Aut=Automate
    aut=Aut[2]
    alpha=Aut[1]
    sommet=Aut[0]
    liste=list(sommet)
    puit=max(liste)+1
    ok=True
    for i in sommet:
        for j in alpha:
            if (i,j) not in aut:
                aut[(i,j)]={puit}
                ok=False
    if ok==False:
        for j in alpha:
            aut[(puit,j)]={puit}
        sommet.add(puit)
    return (Aut[0],Aut[1],aut,Aut[3],Aut[4])

def analyseMot(motEntrer):
    global Automate,temporisateur,motAnalyser,nextEtat,sectionSortDuMot,sortDuMot,sectionDessein,positionx,postionxSave
    (Etat,alphabet,tt,initiaux,acceptant)=Automate
    lettreEnListe=[]
    rayon=50
    y=72
    dist=50
    if(AFN):
        messagebox.showinfo("En Attente","La lecture d'un mot par un AFD n'est pas encore prise en compte")
        return False
    
    if(motEntrer==motAnalyser and motEntrer!=""):
        lettreEnListe=[k for k in motEntrer]
        #Dessein
        if(temporisateur>=len(lettreEnListe)):
            #donner le sort final du mot
            sectionSortDuMot.pack()
            if(nextEtat in acceptant):
                sortDuMot.config(bg="green")
                sortDuMot["text"]="MOT ACCEPTER"
            else:
                sortDuMot.config(bg="red")
                sortDuMot["text"]="MOT REFUSER"
            sortDuMot.pack()
                
            return True
        
        sectionDessein.create_line(positionx,95,positionx+dist,95,arrow=LAST)
        sectionDessein.create_oval(positionx+dist,y,positionx+dist+rayon,y+rayon)
        if(nextEtat in acceptant):
            sectionDessein.create_oval(positionx+dist+(5),y+(5),positionx+dist+(rayon-5),y+(rayon-5))
        sectionDessein.create_text(dist+positionx+(rayon//2),95,text=f"{nextEtat}",font=("Lato",14,"bold"))

    elif(motEntrer!=""):
        #premiere analyse
        temporisateur=0
        motAnalyser=motEntrer
        nextEtat=list(initiaux)[0]
        for k in motEntrer:
            if(k not in alphabet):
                messagebox.showerror("Invalide","Le mot entrer contient des elements n'ont mentionner dans l'alphabet ")
                return False
            lettreEnListe.append(k)
        #Gestion Dessein
        sectionDessein.pack()
        sectionDessein.create_line(positionx,95,positionx+dist,95,arrow=LAST)
        sectionDessein.create_oval(positionx+dist,72,positionx+dist+rayon,72+rayon)
        if(nextEtat in acceptant):
            sectionDessein.create_oval(30+(5),72+(5),30+(rayon-5),72+(rayon-5))
        sectionDessein.create_text(positionx+dist+(rayon//2),95,text=f"{nextEtat}",font=("Lato",14,"bold"))
    lettre=lettreEnListe[temporisateur]
    if((nextEtat,lettre) in tt):
        nextEtat=list(tt[(nextEtat,lettre)])[0]
    else:
        messagebox.showinfo("Incomplet",'Automate INCOMPLET')
        return False
    temporisateur+=1
    positionx=positionx+dist+rayon

print(emonder())
          
