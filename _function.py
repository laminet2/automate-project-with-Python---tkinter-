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

def lireNDe(aut,m):
    (etats,al,T,init,Ac)=aut
    #On calcule une bonne fois toute les clôtures
    Cl={i:cloture(aut,i) for i in etats}
    L=[init] # Une liste d'ensembles
    et=list(init)
    for c in m:
        # On calcule l'ensemble des états accessibles par lecture de la lettre c
        # à partir d'un des états actuels
        et2=set()
        for i in et:
            for e in Cl[i]:  #On calcule les transitions étendues à toute la clôture
                if (e,c) in T :
                    et2=et2.union(T[(e,c)])
        L.append(et2)
        et=list(et2)
        if et==[]:
            return(false,L)
    #On n'oublie pas de faire hériter le caractère acceptant aux états 
    #possédant un état acceptant dans leur clôture
    Ac2=set(Ac)
    for e in etats:
        if Cl[e].intersection(Ac)!={} and not e in Ac2:
            Ac2.add(e)
    return (et2.intersection(Ac2)!={},L)

def cloture(aut,i):
    (etats,al,T,init,Ac)=aut

    Cl={i} # La clôture de l'état i
    L=[i]
    while L:
        j=L.pop(0)
        if (j,'€') in T:
            for k in T[(j,'€')]:
                if not k in Cl:
                    Cl.add(k)
                    L.append(k)
    return (Cl)

def déterminise(aut):
    (etats,alpha,T,init,accept)=aut
    #On calcule une bonne fois toute les clôtures
    Cl={i:cloture(aut,i) for i in etats}
    print("Clôtures :")
    print(Cl)
    #On fait hériter le caractère acceptant aux états 
    #possédant un état acceptant dans leur clôture
    Ac=set(accept)
    for e in etats:
        if Cl[e].intersection(accept)!=set() and not e in Ac:
            print(e,"hérite du caractère acceptant")
            Ac.add(e)
    etatsD={1}
    k=1
    TD = {}
    initD={1}
    acceptD=set()
    if init.intersection(Ac)!=set():
                        acceptD.add(1)
    L=[init] # La liste des états qu'il reste à traiter
    LM=[init]# La liste des états de l'AFD mémorisés 
    while L:
        et=L.pop(0)
        for c in alpha:
            et2=set()
            for i in et:
                for e in Cl[i]:#On calcule les transitions étendues à toute la clôture
                    if (e,c) in T:
                        et2=et2.union(T[(e,c)])

            if et2!=set():
                if  (et2 not in LM):
                    k+=1
                    etatsD.add(k)
                    LM.append(et2) 
                    L.append(et2)
                i=LM.index(et)+1
                j=LM.index(et2)+1
                TD[(i,c)]=j
                if et2.intersection(Ac)!=set():
                        acceptD.add(j)
    print("Liste des états :")
    print(LM)
    return (etatsD,alpha,TD,initD,acceptD)

def cloture(aut,i):
    (etats,al,T,init,Ac)=aut

    Cl={i} # La clôture de l'état i
    L=[i]
    while L:
        j=L.pop(0)
        if (j,'€') in T:
            for k in T[(j,'€')]:
                if not k in Cl:
                    Cl.add(k)
                    L.append(k)
    return (Cl)


def lireNDe(aut,m):
    (etats,al,transs,init,Ac)=aut
    
    Cl={i:cloture(aut,i) for i in etats}
    tete=init
    passage=[init]
    lettreIndex=0
    t={i:transs[i] for i in transs if transs[i]!=set()}
    for lettre in m:
        tete2=set()
        for k in tete:
            if(Cl[k]!=set()):
                for j in Cl[k]:
                    if(j!=k and (j,lettre) in transs):
                        tete2=tete2.union(t[(j,lettre)])
            if((k,lettre) in t):
                tete2=tete2.union(t[(k,lettre)])
        tete=tete2
        passage.append(tete)
    return (True,passage)

def analyseMot(motEntrer):
    global Automate,temporisateur,motAnalyser,nextEtatEnsemble,sectionSortDuMot,sortDuMot,sectionDessein,positionx,postionSave,pere
    (Etat,alphabet,tt,initiaux,acceptant)=Automate
    lettreEnListe=[]
    rayon=50
    y=50
    dist=50
    # if(AFN):
    #     messagebox.showinfo("En Attente","La lecture d'un mot par un AFD n'est pas encore prise en compte")
    #     return False
    
    if(motEntrer==motAnalyser and motEntrer!=""):
        lettreEnListe=[k for k in motEntrer]
        #Dessein
        if(temporisateur>=len(lettreEnListe)):
            #donner le sort final du mot
            sectionSortDuMot.pack()
            #print(nextEtat)
            for nextEtat in nextEtatEnsemble:
                if(nextEtat in acceptant):
                    
                    sortDuMot.config(bg="green")
                    sortDuMot["text"]="MOT ACCEPTER"
                    sortDuMot.pack()
                    return True
            
            sortDuMot.config(bg="red")
            sortDuMot["text"]="MOT REFUSER"
            sortDuMot.pack()
            return False

        for nextEtat in nextEtatEnsemble:
            y=50
            while((positionx+dist,y,positionx+dist+rayon,y+rayon) in postionSave.values()):
                y+=52
            for k in pere[nextEtat]:
                sectionDessein.create_line(positionx,postionSave[k][1]+23,positionx+dist,y+23,arrow=LAST)
            sectionDessein.create_oval(positionx+dist,y,positionx+dist+rayon,y+rayon)
            postionSave[nextEtat]=(positionx+dist,y,positionx+dist+rayon,y+rayon)
            pere[nextEtat]=set()
            #print(nextEtat)
            if(nextEtat in acceptant):
                sectionDessein.create_oval(positionx+dist+(5),y+(5),positionx+dist+(rayon-5),y+(rayon-5))
            sectionDessein.create_text(dist+positionx+(rayon//2),y+23,text=f"{nextEtat}",font=("Lato",14,"bold"))

    elif(motEntrer!=""):
        #premiere analyse
        postionSave=dict()
        pere=dict()
        temporisateur=0
        motAnalyser=motEntrer
        nextEtatEnsemble=list(initiaux)  #For next ETAT
        for k in motEntrer:
            if(k not in alphabet):
                messagebox.showerror("Invalide","Le mot entrer contient des elements n'ont mentionner dans l'alphabet ")
                return False
            lettreEnListe.append(k)
        #Gestion Dessein
        sectionDessein.pack()
        
        for nextEtat in nextEtatEnsemble:
            sectionDessein.create_line(positionx,y+23,positionx+dist,y+23,arrow=LAST)
            sectionDessein.create_oval(positionx+dist,y,positionx+dist+rayon,y+rayon)
            postionSave[nextEtat]=(positionx+dist,y,positionx+dist+rayon,y+rayon)
            if(nextEtat in acceptant):
                sectionDessein.create_oval(30+(5),y+(5),30+(rayon-5),y+(rayon-5))
            sectionDessein.create_text(positionx+dist+(rayon//2),y+23,text=f"{nextEtat}",font=("Lato",14,"bold"))
            y+=52

    lettre=lettreEnListe[temporisateur]
    nextEtatEnsembleTempo=set()
    for nextEtat in nextEtatEnsemble:
        if((nextEtat,lettre) in tt):
            nextEtatEnsembleTempo = nextEtatEnsembleTempo | tt[(nextEtat,lettre)]
            for i in tt[(nextEtat,lettre)]:
                if(i not in pere):
                    pere[i]=set()
                pere[i].add(nextEtat)
        else:
            messagebox.showwarning("Incomplet",'Automate INCOMPLET')
    nextEtatEnsemble=nextEtatEnsembleTempo
    temporisateur+=1
    positionx=positionx+dist+rayon        