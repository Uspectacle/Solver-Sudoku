##
##



"""========\\  Résolution d'un SUDOKU  \\========"""


##
##





# Ce doccument Python contient toute les fonctions permetant de résoudre un Sudoku.

# Il se décompose en 6 parties :
# - La présentation des fonctions de base qui seront utilisées
# - L'initialisation, c'est à dire l'explication de la méthode global et les fonctions d'ordre générale sur le Sudoku
# - Les fonctions de résolution triviales
# - Les 3 méthodes à employer pour résoudre des Sudoku plus complexe
# - La fonction de résolution générale de Sudoku
# - Un exemple de Sudoku complexe et sa résolution





import copy # On aura besoin de copy.deepcopy, pop et append



















##


"""Les fonctions de base"""

##





# Voici les fonctions peu complexe et utilisé régulierement par la suite.





### On commence avec les definitions des ensembles du sudoku :

# Liste décrivant la i+1-eme ligne

def ligne(M0,i):
    M=copy.deepcopy(M0)
    return([M[i][k] for k in range(9)])



# Liste décrivant la i+1-eme colone

def colone(M0,i):
    M=copy.deepcopy(M0)
    return([M[k][i] for k in range(9)])



# Assigne à un emplacement, l'indice de l'un des neufs carré 3x3 auquel il appartient tel que le sudoku décrive : [[0,1,2],[3,4,5],[6,7,8]]

def icarre(i,j):
    return(3*(i//3)+j//3)



# Liste décrivant du i+1-eme carré

def carre(M0,i):
    M=copy.deepcopy(M0)
    return([M[k+3*(i//3)][j+3*(i%3)] for k in range(3) for j in range(3)])





### On continue avec les fonctions sur les listes, simples mais adaptés au contexte :

# Retire tout les éléments n d'une liste L0

def retirer(L0,n):
    L=copy.deepcopy(L0)
    L2=[]
    for k in range(len(L)):
        if L[k]!=n:
            L2.append(L[k])  # la nouvelle liste prend tout les elements de L0 qui ne sont pas n
    return(L2)



# Répond si il est vrai que l'élément 'n' est dans la liste L0

def presence(L0,n):
    L=copy.deepcopy(L0)
    s=False
    for k in range(len(L)):
        if L[k]==n:
            s=True
    return(s)



# Répond si n est bien un des neuf nombres possibles et non pas une liste

def nombre(n):
    return(presence([1,2,3,4,5,6,7,8,9],n))  



# Liste des positions dans L0, des listes qui contiennent tout les éléments de la liste N0

def contient(L0,N0):
    L=copy.deepcopy(L0)
    N=copy.deepcopy(N0)
    S=[]
    for k in range(len(L)):
        if nombre(L[k])==False:
            S.append(k)    # on suppose que L[k] contient N puis tente de le réfuter
            for n in range(len(N)):
                if presence(L[k],N[n])==False:
                    S=retirer(S,k) # refuté
    return(S)



# Répond si il est vrai que la liste L0 contient des nombres en double

def doublon(L0):
    L=copy.deepcopy(L0)
    s=False
    for k in range(len(L)-1):
        for i in range(k+1,len(L)):
            if nombre(L[i])==True:
                if L[k]==L[i]:
                    s=True
    return(s)





### On fabrique la liste P(E) pour un ensemble E, c'est à dire l'ensemble des ensembles inclus dans E (un ensemble)

def combinaisons(L0):
    L=copy.deepcopy(L0)
    n=len(L)+1
    P=[[]]*(n**(n-1)) # on créé une liste de tout les combinaisons possibles...
    if n!=1 and n<8:
        for k in range(n**(n-1)):
            for i in range(1,n):  # ...des entiers naturels de 1 à n
                for j in range(n):
                    if (k//(n**j))%n==i:
                        P[k]=P[k]+[i]
        k=1
        while k<len(P):  # on retire les éléments 'false', c'est à dire si...
            s=True
            if len(P[k])>1:
                for i in range(1,len(P[k])):
                    if P[k][i-1]>=P[k][i]:  # ... l'élément n'est pas ordoné (strictement croissant)
                        s=False
            if s==True:
                for j in range(k):
                    if P[j]==P[k]:   # ... l'élément est déjà dans la liste
                        s=False
            if s==False:
                P.pop(k)
                k=k-1  # on retire l'élément 'false'
            k=k+1
        if len(P)!=1:
            for k in range(1,len(P)):
                for i in range(len(P[k])):
                    P[k][i]=L[P[k][i]-1]  # On remplace les valeurs muettes par les éléments de la liste
    if n>=8:  # Trop compliqué pour Python
        P=[]
    return(P)



# Fonction inutile, mais amusante: calculer les puissances de 2 de façon beaucoup trop complexe

def deux_puissance(n):  # Pour n un entier naturel inferieur à 7 car l'ordinateur ne peux calculer au dela
    L=[k for k in range(n)]
    P=combinaisons(L)
    return(len(P))



















##


""" Initialisation """

##





# M est le sudoku dans les fonctions, c'est une matrice 9 par 9 ne contenant que des chiffres et des listes de chiffres. Il est initalement remplie avec des 0 pour signifier que la case est vide.





### : écrir une liste de toutes les possibilités pour chaque case vide 

def Remplissage(M0):
    M=copy.deepcopy(M0)
    for i in range (9):
        for j in range (9):
            if M[i][j]==0:
                M[i][j]=[1,2,3,4,5,6,7,8,9]
    return(M)





# L'objectif du programme est donc de developper des strategies qui permettent de retirer des nombres de ces listes afin de ne conserver que les nombres encore validable. Quand une liste ne contient plus qu'un seul nombre, on écrira definitivement ce nombre sur la case. Le programme se terminera quand toutes les cases auront un unique nombre et que le sudoku sera cohérent.





### L'Etat dit si il est vrai que le Sudoku est fini

def Etat(M0):
    M=copy.deepcopy(M0)
    s=True                                    #  On suppose que le sudoku est fini et on tente de le refuter ...
    for i in range(9):
        for j in range(9):
            if presence(ligne(M,i),j)==False:
                s=False                       # ... par non présence des neuf chiffres dans chaque ensemble
            if presence(colone(M,i),j)==False:
                s=False
            if presence(carre(M,i),j)==False:
                s=False
    return(s)





### Présentation du sudoku ligne par ligne


def Presentation(M0):
    for k in range(len(M0)):
        print(M0[k])



















##


""" Retirer les possibilités trivialement fausses """

##





# Au Sudoku, la grille se sépart en 3 types d'ensemble, les 9 colonnes, les 9 lignes et les 9 carrés.
# Dans chaque ensemble, il y a 9 cases.

# La règle de base du jeu est d'écrire les chiffres 1, 2, 3, 4, 5, 6, 7, 8 et 9 dans chaque ensemble. 
# S'il y a autant de cases que d'éléménts differents à y écrire et que chaque case ne peut contenir qu'un seul nombre alors :
# Un même nombre ne peut être présent plus d'une fois dans un ensemble.

# Autrement dit, l'on va retirer des possibilités d'une case tout les nombres qui sont déjà écrits dans les ensembles incluant la case.





### Répond si un nombre n est déjà present dans le voisinage de la case i,j

def impossible(M0,n,i,j):
    M=copy.deepcopy(M0)
    s=False
    if presence(ligne(M,i),n)==True:
        s=True
    if presence(colone(M,j),n)==True:
        s=True
    if presence(carre(M,icarre(i,j)),n)==True:
        s=True
    return(s)





### Retire toutes les possibilités impossibles d'une case i,j du sudoku M0 et valide les seules possibilités restantes

def Vidange(M0,i,j):
    M=copy.deepcopy(M0)
    for n in range(1,10):
        if impossible(M,n,i,j)==True:
            M[i][j]=retirer(M[i][j],n) # n n'est pas possible
    if len(M[i][j])==1:
        M[i][j]=M[i][j][0] # validation de la seul possibilité restante
    return(M[i][j])





### Applique la fonction précedente à toute les cases qui contiennent des possibilités

def Vidange_total(M0):
    M=copy.deepcopy(M0)
    for i in range(9):
        for j in range(9):
            if nombre(M[i][j])==False:
                M[i][j]=Vidange(M,i,j)
    return(M)





### On applique ce que l'on sait déjà à un module de résolution incomplet, mais suffisant pour un sudoku simple

def Resolution_partielle(M0):
    M=copy.deepcopy(M0)
    M=Remplissage(M)
    M1=copy.deepcopy(Vidange_total(M))
    while M1!=M:
        M=copy.deepcopy(M1) 
        M1=Vidange_total(M) # Vidange chaque case jusqu'à l'idempotence (la fonction Vidange_total devienne inefficace)
    return(M)



















##


""" Stratégie 1 : n possibilités pour n cases """

##





# Une première statégie, pratique dans certains cas est la suivante.

# Prenons un ensemble qui peut représenter une ligne, une colonne ou même un carré:
# L=[[7, 8, 9], 1, 2, 5, [3, 4, 9], [3, 4, 7, 9], 6, [8, 9], [8, 9]]

# On remarque que 3 et 4 ne sont possibles que dans 2 cases, la 5ième et la 6ième.
# Soit 3 est dans la 5ième, et donc 4 est dans la 6ième.
# Soit 3 est dans la 6ième, et donc 4 est dans la 5ième.
# Dans tout les cas, 3 et 4 occuperont ces 2 cases. 
# Il est ainsi impossible que 7, 8 ou 9 ne soit écrit dans ces cases.
# L doit donc être réecrit :
# L=[[7,8,9], 1, 2, 5, [3, 4], [3, 4], 6, [8, 9], [8, 9]]

# Cette remarque est généralisable à n nombres qui ne sont possible que dans n cases.
# Ainsi en reprenant l'exemple :
# L=[[7, 8, 9], 1, 2, 5, [3, 4, 9], [3, 4, 7, 9], 6, [8, 9], [8, 9]]
# On aurait aussi pu voir que 3, 4 et 7 se partagent les 1ière, 5ième et 6ième cases et ainsi, L s'écrivait :
# L=[[7], 1, 2, 5, [3, 4], [3, 4, 7], 6, [8, 9], [8, 9]]

# L'objectif de la Stratégie 1 est de trouver les couples de n possibilités qui se partagent n cases et d'en déduire l'impossibilité pour les autres nombres d'être dans ces n cases.





### On cherhce la liste des nombres pas encore validé dans une liste L0

def possible(L0):
    L=copy.deepcopy(L0)
    S=[1,2,3,4,5,6,7,8,9]
    for k in range(9):
        if nombre(L[k])==True:    # on retire les nombres validés
            S=copy.deepcopy(retirer(S,L[k]))
    return(S)





### Si n Possibilités (liste nP) se partagent n Cases (liste nC), alors auccun autre nombre ne peut occuper ces cases

def Application(L0,nP,nC):
    L=copy.deepcopy(L0)
    n=len(nP)
    L2=copy.deepcopy(L)
    for i in range(n):
        k=nC[i]
        for j in range(len(L[k])):
            if presence(nP,L[k][j])==False: # un autre nombre
                L2[k]=retirer(L2[k],L[k][j])
    return(L2)





### Recherche de n possibilités se partageant n cases et application de la statégie 1 sur un ensemble

def Laplace(L0):
    L=copy.deepcopy(L0)
    L2=copy.deepcopy(L)
    p=possible(L)
    if len(p)<7: # Limitation technique
        P=combinaisons(p)
        for k in range(len(P)):
            if len(P[k])!=0 and len(P[k])<len(p):
                nP=P[k]   # on teste une combinaison de possibilité de cardinal n
                n=len(nP)
                nC=[]  # les cases qu'elles se partagent
                for i in range(n):
                    I=contient(L,[nP[i]]) # liste des cases de l'ensemble où le nombre nP[i] est une possibilité
                    for j in range(len(I)):
                        if presence(nC,I[j])==False:
                            nC.append(I[j]) # les cases que se partagent les n possibilités
                if len(nC)==n :   # condition de la stratégie 1
                    L2=Application(L2,nP,nC)
    return(L2)



















##


""" Stratégie 2 : n cases pour n possibilités """

##





# Cette deuxième statégie, est similaire si ce n'est identique à la première.

# Prenons un ensemble qui peut représenter une ligne, une colonne ou même un carré:
# L=[[7, 8, 9], 1, 2, 5, [3, 4, 9], [3, 4, 7, 9], 6, [8, 9], [8, 9]]

# On remarque que les deux dernières cases ne contiènent que 8 et 9 comme possibilité.
# Si 8 ou 9 est ecrit dans l'une 7 premières cases, alors l'une des deux dernières cases sera l'ensemble vide.
# Par l'absurde, on a trouve que 8 et 9 ne sont impossibles dans les 7 premières cases.
# L doit donc être réecrit :
# L=[[7], 1, 2, 5, [3, 4], [3, 4, 7], 6, [8, 9], [8, 9]]

# Cette remarque est généralisable à n case qui ne se partagent que n possibilités.

# L'objectif de la Stratégie 2 est de trouver les couples de n cases qui se partagent n possibilités et d'en déduire l'impossibilité pour ces nombres d'être dans les autres cases.





### On cherhce la liste des cases pas encore validé dans une liste L0

def leslistes(L0):
    L=copy.deepcopy(L0)
    L2=[]
    for k in range(len(L)):
        if nombre(L[k])==False:
            L2.append(k)
    return(L2)





### Si n Cases (liste nC) se partagent n Possibilités (liste nP), alors auccun autre case ne peut contenir ces nombres

def Separation(L0,nP,nC):
    L=copy.deepcopy(L0)
    n=len(nC)
    L2=copy.deepcopy(L)
    for k in range(9):
        if presence(nC,k)==False and nombre(L[k])==False: # une autre case
            for i in range(len(L[k])):
                for j in range(n):
                    if presence(L[k],nP[j])==True:
                        L2[k]=retirer(L2[k],nP[j])
    return(L2)





### Recherche de n cases se partageant n possibilité et application de la statégie 2 sur un ensemble

def Cloture(L0):
    L=copy.deepcopy(L0)
    L2=copy.deepcopy(L)
    c=leslistes(L)
    if len(c)<7: # Limitation technique
        C=combinaisons(c)
        for k in range(len(C)):
            if len(C[k])!=0 and len(C[k])<len(c):
                nC=C[k]   # on teste une combinaison de case de cardinal n
                n=len(nC)
                nP=[]  # les possibilités qu'elles se partagent
                for i in range(n):
                    I=L[nC[i]] # liste des possibilité de la case [nC[i]]
                    for j in range(len(I)):
                        if presence(nP,I[j])==False:
                            nP.append(I[j])
                if len(nP)==n:    # condition de la stratégie 2
                    L2=Separation(L2,nP,nC)
    return(L2)



















##


""" Stratégie 3 : Restriction d'une ligne/colonne à un carré et inversement """

##





# Cette troisième statégie est souvant utile.
# Simplement, si toutes possibilités d'un nombre sur une ligne ( ou colonne ) sont contenue dans un même carré, alors, le nombre n'est pas possible dans les autres cases du carré.
# De même si les possibilités d'un nombre sur un carré sont concentrés sur une seul ligne (ou une seul colonne) alors, le nombre n'est pas possible dans les autres cases de la ligne ( ou de la colonne ).





### On cherche dans un ensemble tout les nombres qui ne sont possible que dans un même tière de l'ensemble

def Concentration(L0):
    L=copy.deepcopy(L0)
    S=[]
    P=possible(L)
    for i in range(len(P)):
        I=contient(L,[P[i]])  # liste des cases de L0 où P[i] est une possibilité
        s=True
        if len(I)>1:
            for k in range(1,len(I)):
                if I[k-1]//3!=I[k]//3:  # Ces cases sont concentrées dans un tiere de L0 
                    s=False
            if s==True:
                S.append([P[i],I[k]//3]) # Liste des nombres interressants pour la stratégie 3 accompagné du tière de L0 où ce nombre est concenté
    return(S)





### On applique la stratégie 3 à une ligne pour limiter les possibilités d'un carré

def Ligne_Carre(M0):
    M=copy.deepcopy(M0)
    for i in range(9): # la ligne que l'on étudit
        C=Concentration(ligne(M,i)) # les nombres et le tiere de ligne où ils sont concentrés
        for k in range(len(C)):
            for j in range(3):
                if i%3!=j:   # les autres lignes qui partagent les même carré que la ligne i
                    for n in range(3):
                        I=3*(i//3)+j  
                        J=3*C[k][1]+n  # les colonnes du carré que l'on limite
                        if nombre(M[I][J])==False:
                            M[I][J]=retirer(M[I][J],C[k][0])
    return(M)





### On applique la stratégie 3 à une colonne pour limiter les possibilités d'un carré

def Colonne_Carre(M0):
    M=copy.deepcopy(M0)
    for j in range(9): # la colonne que l'on étudit
        C=Concentration(colone(M,j)) # les nombres et le tiere de colonne où ils sont concentrés
        for k in range(len(C)):
            for i in range(3):
                if j%3!=i:  # les autres colonne qui partagent les même carré que la colonne j
                    for n in range(3):
                        I=3*C[k][1]+n
                        J=3*(j//3)+i
                        if nombre(M[I][J])==False:
                            M[I][J]=retirer(M[I][J],C[k][0])
    return(M)





### On applique la stratégie 3 à un carré pour limiter les possibilités d'une ligne

def Carre_Ligne(M0):
    M=copy.deepcopy(M0)
    for ic in range(9): # le carre que l'on étudit
        C=Concentration(carre(M,ic)) # les nombres et la ligne du carré où ils sont concentrés
        for k in range(len(C)):
            I=3*(ic//3)+C[k][1] # la ligne qui contient le nombre concentré
            for j in range(9):
                if j//3!=ic%3: # les colonnes qui ne coupent pas le carré
                    if nombre(M[I][j])==False:
                        M[I][j]=retirer(M[I][j],C[k][0])
    return(M)





### Cas particulier des carrés aux colonnes

# On recommence la fonction concentration pour la faire sortir les colones et non les lignes (avec L0 décrivant un carré) où des nombres sont concentrés

def Concentration_spe(L0):
    L=copy.deepcopy(L0)
    S=[]
    P=possible(L)
    for i in range(len(P)):
        I=contient(L,[P[i]])
        s=True
        if len(I)>1:
            for k in range(1,len(I)):
                if I[k-1]%3!=I[k]%3:
                    s=False
            if s==True:
                S.append([P[i],I[k]%3])
    return(S)    



# On applique la stratégie 3 à un carré pour limiter les possibilités d'une colonnes

def Carre_Colonne(M0):
    M=copy.deepcopy(M0)
    for ic in range(9): # le carre que l'on étudit
        C=Concentration_spe(carre(M,ic)) # les nombres et la colonne du carré où ils sont concentrés
        for k in range(len(C)):
            J=3*(ic%3)+C[k][1]  # la colonne qui contient le nombre concentré
            for i in range(9):
                if i//3!=ic//3:  # les lignes qui ne coupent pas le carré
                    if nombre(M[i][J])==False:
                        M[i][J]=retirer(M[i][J],C[k][0])
    return(M)   



















##


""" La Résolution """

##





### On applique ce que l'on sait des méthodes triviales. C'est incomplet, mais suffisant pour un sudoku simple

def Resolution_partielle(M0):
    M=copy.deepcopy(M0)
    M=Remplissage(M)
    M1=copy.deepcopy(Vidange_total(M))
    while M1!=M:
        M=copy.deepcopy(M1) 
        M1=Vidange_total(M) # Vidange chaque case jusqu'à l'idempotence (la fonction Vidange_total devienne inefficace)
    return(M)





### On applique toutes les facettes de la stratégie 3 au sudoku en même temps

def Canon_Ball(M0):
    M=copy.deepcopy(M0)
    M=Ligne_Carre(M)
    M=Colonne_Carre(M)
    M=Carre_Ligne(M)
    M=Carre_Colonne(M)
    return(M)





### On complette un peu notre module de résolution avec la stratégie 3

def Resolution_Canon(M0):
    M=copy.deepcopy(M0)
    M1=Resolution_partielle(M)
    if Etat(M1)==False:
        M=Canon_Ball(M1)
        while M1!=M and Etat(M)==False:
            M1=Resolution_partielle(M)
            M=Canon_Ball(M1)
    return(M)





### On rassemble les stratégies 1 et 2 et les applique à tout les ensembles du sudoku

def Full_Monty(M0):
    M=copy.deepcopy(M0)
    for i in range(9):
        L=Laplace(ligne(M,i)) # Stratégie 1 appliqué aux lignes
        L2=Cloture(L)   # Stratégie 2 appliqué aux lignes
        for j in range(9):
            M[i][j]=L2[j]
    for j in range(9):
        C=Laplace(colone(M,j))
        C2=Cloture(C)   # aux colonnes
        for i in range(9):
            if nombre(C[i])==True:
                M[i][j]=C2[i]
            else :
                M[i][j]=copy.deepcopy(C[i])
    for ic in range(9):
        C3x3=Laplace(carre(M,ic))
        C3x3_2=Cloture(C3x3)  # aux carrés
        for k in range(9):
            I=3*(ic//3)+(k//3)
            J=3*(ic%3)+(k%3)
            M[I][J]=C3x3_2[k]
    return(M)





### On compile tout ce que l'on a dans une seule fonction de résolution

def SUDOKU(M0):
    M=copy.deepcopy(M0)
    M1=Resolution_Canon(M)
    if Etat(M1)==False:
        M=Full_Monty(M1)
        while M1!=M and Etat(M)==False:
            M1=Resolution_Canon(M)
            M=Full_Monty(M1)
    return(M)



















##


""" Exemple """

##





### On rentre le sudoku à la main (pour le moment) sous forme de liste de liste

S=[[8,0,3,0,4,0,0,0,5],[0,0,0,0,0,1,3,0,6],[0,0,0,7,3,0,0,0,0],[0,6,7,0,0,0,0,0,0],[3,0,0,0,0,0,0,0,2],[0,0,0,0,0,0,4,5,0],[0,0,0,0,2,7,0,0,0],[4,0,9,1,0,0,0,0,0],[5,0,0,0,6,0,7,0,4]]



Presentation(S)

# [8, 0, 3, 0, 4, 0, 0, 0, 5]
# [0, 0, 0, 0, 0, 1, 3, 0, 6]
# [0, 0, 0, 7, 3, 0, 0, 0, 0]
# [0, 6, 7, 0, 0, 0, 0, 0, 0]
# [3, 0, 0, 0, 0, 0, 0, 0, 2]
# [0, 0, 0, 0, 0, 0, 4, 5, 0]
# [0, 0, 0, 0, 2, 7, 0, 0, 0]
# [4, 0, 9, 1, 0, 0, 0, 0, 0]
# [5, 0, 0, 0, 6, 0, 7, 0, 4]





###  On teste la résolution

Presentation(SUDOKU(S))

# [8, 1, 3, 6, 4, 2, 9, 7, 5]
# [7, 2, 4, 5, 9, 1, 3, 8, 6]
# [9, 5, 6, 7, 3, 8, 2, 4, 1]
# [1, 6, 7, 2, 5, 4, 8, 3, 9]
# [3, 4, 5, 8, 7, 9, 1, 6, 2]
# [2, 9, 8, 3, 1, 6, 4, 5, 7]
# [6, 3, 1, 4, 2, 7, 5, 9, 8]
# [4, 7, 9, 1, 8, 5, 6, 2, 3]
# [5, 8, 2, 9, 6, 3, 7, 1, 4]


# Résolut en 13 minutes par le programme contre 35 minutes à la main



















# Le programme n'est pas encore parfait:

# Le temps de résolution est trop grand.
# Il n'est pas sûre que le module peut résoudre tout les sudoku.
# Seul les sudoku de taille 9 contenant les chiffres de 1 à 9 sont résoluble.
# Il faut rentrer le sudoku à la main.
# L'affichage du résultat n'est pas un sudoku.
# Des erreurs ont pu se glisser entre les lignes.
# Les combinaisons sont limités aux ensembles de moins de 8 éléments.
# Le systhème d'hypothèse n'as pas été mit en place.
# Certain passages sont difficilement comprehansible.
# l'outil copy n'a pas de remplacent 'fait main' qui ne ralenti pas trop.

# Toute fois les résultats sont là.
# Le programme vas plus vite que l'homme en particulier sur les sudoku simples.
# La programmation a necessité de nombreuses et longue periodes de reflexion.
# Plusieurs théorèmes ont du etre démontré, ne serai-ce que pour les combinaisons.
# Les notions d'idempotence, de théorie des graphs, de dénombrement, de division euclidienne, de matrice...

# Cette exercice m'as prit 2 mois de travail (à faible fréquence).
# Merci de m'avoir lut.







