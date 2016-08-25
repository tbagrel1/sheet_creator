# -*- coding:utf-8 -*

############### SHEET CREATOR X ###############

# Titre :    SheetCreatorX - Version Windows

# Auteur :   Thomas BAGREL
# Adresse :  tomsb07@gmail.com

# Version :  1.2.1 Beta
# Langue : Français

# Afichage : Interface graphique (GUI) avec "tkinter"

# Corps du programme : Module "__main__.py"

# Prérequis : Google Chrome, LaTeX Distribution (pour PDFLaTeX), Editeur LaTeX

# Documentation :
"""
Ce petit programme est destiné à créer des feuilles de mots pour les
classes de maternelle de façon simple et automatisée.\nIl génère un
fichier .tex (LaTeX), qui est ensuite compilé, pour donner un .pdf.
Un dossier est créé pour chaque mot de référence entré.\nBonne
utilisation !\nPour plus d'informations, lancer le programme et acceder
à l'aide ou consulter le fichier "Aide.pdf"
"""

##### Début du programme #####

  #### 1. Préambule ####

	### 1.1. Import des modules ###
		# Module "random" pour choisir aléatoirement les mots ... #
from random import *
		# Module "tkinter" pour créer l'interface graphique #
from tkinter import *
		# Module "os" pour les commandes système #
import os

	### 1.2. Création des classes et des fonctions ###

	  ## 1.2.1. Création des classes ##

		# Classe "Err" pour afficher un message d'erreur graphique (Toplevel) #
class Err(Toplevel):
	# Corps de la classe
	def __init__(self, Master=None):
		Toplevel.__init__(self, Master)
		# Création de la fenêtre graphique
		TxtBoxErr = Label(self, text="Une erreur est survenue lors de la\
 génération\n Ceci est sûrement du à une erreur de saisie.\nVeuillez cliquer\
 sur \'OK\', et vérifier votre saisie.\nSi ça ne fonctionne pas, relancez\
 le logiciel ou vérifiez les prérequis logiciels.\nMerci !")
		TxtBoxErr.grid(row=0, column=0, sticky=W+E+N+S)
		BoutonFermer = Button(self, text="  Ok  ",\
 command=self.fermer)
		BoutonFermer.grid(row=1, column=0, sticky=W+E+N+S)
		# Bind des touches pour valider et femer la fenêtre
		self.bind("<Return>", self.fermer)
		self.bind("<Escape>", self.fermer)
	# Fonction de fermeture de la classe
	def fermer(self, *event):
		self.quit()

		# Fonction "Erreur" qui crée une fenêtre de la classe "Err" #
def Erreur():
	# Création de la fenêtre de la classe "Err"
	FenetreErreur = Err()
	FenetreErreur.title("Erreur !")
	FenetreErreur.protocol("WM_DELETE_WINDOW", FenetreErreur.quit)
	# Mise au premier plan de la fenêtre
	FenetreErreur.grab_set()
	FenetreErreur.focus_set()
	# Boucle et fermeture de la fenêtre
	FenetreErreur.mainloop()
	FenetreErreur.destroy()

		# Fonction "Generer" qui lance la création du document final
def Generer():
	# Récupération du mot de référence saisi par l'utilisateur
	MotRefBrut = MotRefStringVar.get()
	MotRefBrut.strip()
	# Vérification de la validité du mot de référence et correction
	MotRefValid = True
	MotRef = ""
	ListeErrMotRef = []
	for i in range(len(MotRefBrut)):
		car = MotRefBrut[i]
		if car == "&" or car == "~" or car == "\"" or car == "#" or\
 car == "\'" or car == "{"or car == "(" or car == "[" or car == "-" or\
 car == "|" or car == "`" or car == "_" or car == "\\" or car == "^" or\
 car == "@" or car == ")" or car == "]" or car == "=" or car == "+" or\
 car == "}" or car == "²" or car == "<" or car == ">" or car == "," or\
 car == "?" or car == "." or car == ";" or car == ":" or car == "/" or\
 car == "!" or car == "§" or car == "¨" or car == "$" or car == "£" or\
 car == "ø" or car == "%" or car == "µ" or car == "*":
			if MotRefValid == True:
				MessageEtat("Erreur : R invalide")
				MotRefValid = False
		else:
			MotRef = MotRef + car
	# Vérification de la longueur minimale du mot de référence
	if len(MotRef) < 3:
		MessageEtat("Erreur : R trop court")
		MotRefStringVar.set("cochon")
		MotRef = MotRefStringVar.get()

	# Récupération du nombre de ligne saisi par l'utilisateur
	NombreLignesBrut = NombreLignesStringVar.get()
	# Vérification de la validité du nombre de ligne
	try:
		NombreLignes = int(NombreLignesBrut)
	except:
		MessageEtat("Erreur : NBL invalide")
		NombreLignesStringVar.set("5")
		NombreLignesBrut = NombreLignesStringVar.get()
		NombreLignes = int(NombreLignesBrut)

	# Récupération des choix d'écriture (checkbuttons)
	Capitale = CapitaleIntVar.get()
	Script = ScriptIntVar.get()
	Cursive = CursiveIntVar.get()
	# Calcul de la longueur estimée du fichier final par rapport a une page
	TotalEcriture = Capitale+Script+Cursive
	if TotalEcriture*NombreLignes > 15:
		MessageEtat("Attention : PP possible")

	# Récupération du nombre de mot de référence par ligne
	NombreMotRefBrut = NombreMotRefStringVar.get()
	# Vérification de la validité du nombre de mot de référence par ligne
	try:
		NombreMotRef = int(NombreMotRefBrut)
		if NombreMotRef < 1 or NombreMotRef > 5:
			MessageEtat("Erreur : NBR invalide")
			NombreMotRefStringVar.set("1")
			NombreMotRefBrut = NombreMotRefStringVar.get()
			NombreMotRef = int(NombreMotRefBrut)
	except:
		MessageEtat("Erreur : NBR invalide")
		NombreMotRefStringVar.set("1")
		NombreMotRefBrut = NombreMotRefStringVar.get()
		NombreMotRef = int(NombreMotRefBrut)
	if NombreMotRef > 3:
		MessageEtat("Attention : NBR élevé")

	# Récupération de la probabilité de présence du mot de référence
	ProbaMotRefBrut = ProbaMotRefStringVar.get()
	# Vérification de la validité de la probabilité de présence
	try:
		ProbaMotRef = int(ProbaMotRefBrut)
		if ProbaMotRef < 0 or ProbaMotRef > 100:
			MessageEtat("Erreur : PR invalide")
			ProbaMotRefStringVar.set("80")
			ProbaMotRefBrut = ProbaMotRefStringVar.get()
			ProbaMotRef = int(ProbaMotRefBrut)
	except:
		MessageEtat("Erreur : PR invalide")
		ProbaMotRefStringVar.set("80")
		ProbaMotRefBrut = ProbaMotRefStringVar.get()
		ProbaMotRef = int(ProbaMotRefBrut)
	if ProbaMotRef < 50:
		MessageEtat("Attention : PR basse")
	CalculerProbaMotsDivers()
	# En cas de mode avancé :
	if ModeAvanceeBool is True:
		# Récupération de la liste de mots choisie
		NomListeMots = ListeMotsStringVar.get()
		# Vérification de l'existence de la liste de mots choisie
		if NomListeMots != "ListeMots.txt" and NomListeMots !=\
 "DicoMots.txt" and NomListeMots != "PersoMots.txt":
			MessageEtat("Erreur : LM invalide")
			ListeMotsStringVar.set("ListeMots.txt")
		NomListeMots = ListeMotsStringVar.get()
	else:
		NomListeMots = "ListeMots.txt"

	# Ouverture des fichiers :
	# Ouverture de la liste de mots de référence
	ListeRef = open(NomListeMots, "r", encoding="iso-8859-1")
	# Création d'un dossier au nom du mot de référence s'il n'existe pas
	os.chdir("Fichiers Créés")
	CommandeCreaDossier = "mkdir "+MotRef
	os.system(CommandeCreaDossier)
	# On change le CWD pour le dossier venant d'être créé
	os.chdir(MotRef)
	# Création des noms des fichiers à créé
	NomListeTProche = "ListeTProche_"+MotRef+".txt"
	NomListeProche = "ListeProche_"+MotRef+".txt"
	# Création des fichiers de mots proches et très proches
	ListeTProche = open(NomListeTProche, "w", encoding="iso-8859-1")
	ListeProche = open(NomListeProche, "w", encoding="iso-8859-1")
	# Lecture de la liste de référence
	MotsListeRef = ListeRef.readlines()
	ToggleTProcheIntVar103 = CheckTProcheIntVar103.get()
	ToggleTProcheIntVar102 = CheckTProcheIntVar102.get()
	ToggleTProcheIntVar14 = CheckTProcheIntVar14.get()
	ToggleTProcheIntVar13 = CheckTProcheIntVar13.get()
	ToggleTProcheIntVar31 = CheckTProcheIntVar31.get()
	ToggleProcheIntVar102 = CheckProcheIntVar102.get()
	ToggleProcheIntVar13 = CheckProcheIntVar13.get()
	ToggleProcheIntVar12 = CheckProcheIntVar12.get()
	ToggleProcheIntVar31 = CheckProcheIntVar31.get()
	ToggleProcheIntVar21 = CheckProcheIntVar21.get()
	# Création des listes de mots :
	# Pour chaque mot de la liste de référence :
	for i in range (len(MotsListeRef)):
		# Récupération du mot seul (sans \n)
		MotBrut = MotsListeRef[i]
		Mot = MotBrut[:-1]
		ValidMotTProche = False
		# Pour la liste de mots très proches :
		# Si le paramètre début/fin 3 lettres est choisi pour très proche :
		if ToggleTProcheIntVar103 == 1 and len(Mot) >=3:
			# On prend le début du mot étudié et la fin du mot étudié et on les
			# compare au mot de référence
			if Mot[:3] == MotRef[:3] or Mot[-3:] == MotRef[-3:]:
				ValidMotTProche = True
		# Si le paramètre début/fin 2 lettres est choisi pour très proche :
		if ToggleTProcheIntVar102 == 1 and len(Mot) >=2 and ValidMotTProche\
 == False:
			# On prend le début du mot étudié et la fin du mot étudié et on les
			# compare au mot de référence
			if Mot[:2] == MotRef[:2] or Mot[-2:] == MotRef[-2:]:
				ValidMotTProche = True
		# Si le paramètre 1x4 est choisi pour très proche :
		if ToggleTProcheIntVar14 == 1 and len(Mot) >= 4 and ValidMotTProche ==\
 False:
			# On prend des séquences de 4 lettres sur le mot étudié
			for j in range (len(Mot)-4):
				ChaineAComparer = Mot[j:(j+4)]
				# Et on les compare à toutes les séquences de 4 lettres du mot
				# de référence
				for k in range (len(MotRef)-4):
					ChaineRef = MotRef[k:(k+4)]
					# Si il y a correspondance, on retient le mot
					if ChaineRef == ChaineAComparer:
						ValidMotTProche = True
		# Si le paramètre 1x3 est choisi pour très proche :
		if ToggleTProcheIntVar13 == 1 and len(Mot) >= 3 and ValidMotTProche ==\
 False:
			# On prend des séquences de 3 lettres sur le mot étudié
			for j in range (len(Mot)-3):
				ChaineAComparer = Mot[j:(j+3)]
				# Et on les compare à toutes les séquences de 3 lettres du mot
				# de référence
				for k in range (len(MotRef)-3):
					ChaineRef = MotRef[k:(k+3)]
					# Si il y a correspondance, on retient le mot
					if ChaineRef == ChaineAComparer:
						ValidMotTProche = True
		# Si le paramètre 3x1 est choisi pour très proche :
		if ToggleTProcheIntVar31 == 1 and ValidMotTProche == False:
			ListeCopieMotRef = []
			CaraAComparer = ""
			CaraRef = ""
			CaraCommun = 0
			# On crée la liste de caractères du mot étudié
			for o in range (len(MotRef)-1):
				ListeCopieMotRef.append(MotRef[o])
			# Pour chaque lettre du mot étudié :
			for j in range (len(Mot)-1):
				CaraAComparer = Mot[j]
				# On la compare à toutes les lettres du mot de référence
				for k in range (len(ListeCopieMotRef)-1):
					CaraRef = ListeCopieMotRef[k]
					# Si il y a correspondance, on augmente la variable de
					# caractère commun et on supprime le caractère de la liste
					# pour éviter une double indentification (faussée)
					if CaraAComparer == CaraRef:
						CaraCommun = CaraCommun + 1
						ListeCopieMotRef[k] = ""
						break
			# Si il y a 3 caractères commun au minimum, on retient le mot
			if CaraCommun >= 3:
				ValidMotTProche = True
		ValidMotProche = False
		if ValidMotTProche == False:
			# Pour la liste de mots proches :
			# Si le paramètre début/fin 2 lettres est choisi pour proche :
			if ToggleProcheIntVar102 == 1 and len(Mot) >=2:
				# On prend le début du mot étudié et la fin du mot étudié et on
				# les compare au mot de référence
				if Mot[:2] == MotRef[:2] or Mot[-2:] == MotRef[-2:]:
					ValidMotProche = True
			# Si le paramètre 1x3 est choisi pour proche :
			if ToggleProcheIntVar13 == 1 and len(Mot) >= 3 and ValidMotProche \
== False:
				# On prend des séquences de 3 lettres sur le mot étudié
				for j in range (len(Mot)-3):
					ChaineAComparer = Mot[j:(j+3)]
					# Et on les compare à toutes les séquences de 3 lettres du
					# mot de référence
					for k in range (len(MotRef)-3):
						ChaineRef = MotRef[k:(k+3)]
						# Si il y a correspondance, on retient le mot
						if ChaineRef == ChaineAComparer:
							ValidMotProche = True
			# Si le paramètre 1x2 est choisi pour proche :
			if ToggleProcheIntVar12 == 1 and len(Mot) >= 2 and ValidMotProche\
 == False:
				# On prend des séquences de 2 lettres sur le mot étudié
				for j in range (len(Mot)-2):
					ChaineAComparer = Mot[j:(j+2)]
					# Et on les compare à toutes les séquences de 2 lettres du
					# mot de référence
					for k in range (len(MotRef)-2):
						ChaineRef = MotRef[k:(k+2)]
						# Si il y a correspondance, on retient le mot
						if ChaineRef == ChaineAComparer:
							ValidMotProche = True
			# Si le paramètre 3x1 est choisi pour très proche :
			if ToggleProcheIntVar31 == 1 and ValidMotProche == False:
				ListeCopieMotRef = []
				CaraAComparer = ""
				CaraRef = ""
				CaraCommun = 0
				# On crée la liste de caractères du mot étudié
				for o in range (len(MotRef)-1):
					ListeCopieMotRef.append(MotRef[o])
				# Pour chaque lettre du mot étudié :
				for j in range (len(Mot)-1):
					CaraAComparer = Mot[j]
					# On la compare à toutes les lettres du mot de référence
					for k in range (len(ListeCopieMotRef)-1):
						CaraRef = ListeCopieMotRef[k]
						# Si il y a correspondance, on augmente la variable de
						# caractère commun et on supprime le caractère de la
						# liste pour éviter une double indentification (faussée)
						if CaraAComparer == CaraRef:
							CaraCommun = CaraCommun + 1
							ListeCopieMotRef[k] = ""
							break
				# Si il y a 3 caractères commun au minimum, on retient le mot
				if CaraCommun >= 3:
					ValidMotProche = True
			# Si le paramètre 2x1 est choisi pour très proche :
			if ToggleProcheIntVar21 == 1 and ValidMotProche == False:
				ListeCopieMotRef = []
				CaraAComparer = ""
				CaraRef = ""
				CaraCommun = 0
				# On crée la liste de caractères du mot étudié
				for o in range (len(MotRef)-1):
					ListeCopieMotRef.append(MotRef[o])
				# Pour chaque lettre du mot étudié :
				for j in range (len(Mot)-1):
					CaraAComparer = Mot[j]
					# On la compare à toutes les lettres du mot de référence
					for k in range (len(ListeCopieMotRef)-1):
						CaraRef = ListeCopieMotRef[k]
						# Si il y a correspondance, on augmente la variable de
						# caractère commun et on supprime le caractère de la
						# liste pour éviter une double indentification (faussée)
						if CaraAComparer == CaraRef:
							CaraCommun = CaraCommun + 1
							ListeCopieMotRef[k] = ""
							break
				# Si il y a 2 caractères commun au minimum, on retient le mot
				if CaraCommun >= 2:
					ValidMotProche = True
		# Si le mot n'est pas le même que le mot de référence, ou si le mot ne
		# comporte pas plus de 8 lettres :
		if len(Mot)>8 or Mot==MotRef:
			pass
		else:
			# Si le mot a été retenue pour la liste très proche ou pour les deux
			# listes, on l'inscrit seulement dans la liste très proche (afin
			# d'éviter des doublons quasi-inévitables)
			if ValidMotTProche == True:
				ListeTProche.write(MotBrut)
			# Sinon, si il n'a pas été retenu pour la liste très proche, on
			# vérifie si il a été retenu pour la liste proche, et dans ce cas,
			# on l'inscrit
			elif ValidMotProche == True:
				ListeProche.write(MotBrut)
	# On ferme tous les fichiers
	ListeRef.close()
	ListeTProche.close()
	ListeProche.close()

	# Création du fichier .tex à compiler :
	# Ouverture des listes crées précédemment, ici en lecture ("r")
	ListeTProche = open(NomListeTProche, "r", encoding="iso-8859-1")
	ListeProche = open(NomListeProche, "r", encoding="iso-8859-1")
	NomListeMots = "../../"+NomListeMots
	# Ouverture de la liste de mots de référence, servant pour les mots divers
	ListeRef = open(NomListeMots, "r", encoding="iso-8859-1")
	# Création de listes avec le contenu des 3 listes précédentes
	ContenuListeRef = ListeRef.readlines()
	ContenuListeTProche = ListeTProche.readlines()
	ContenuListeProche = ListeProche.readlines()
	# Affichage d'un message donnant le nombre de mots trouvés pour chaque liste
	MessageEtat("Nombre Mots : "+str((len(ContenuListeTProche)))\
+","+str((len(ContenuListeProche)))+","+str((len(ContenuListeRef))))
	MessageEtat("  ...  ")
	MessageEtat("  ...  ")
	global EtatBox3Vierge
	global EtatBox2Vierge
	EtatBox3Vierge = True
	EtatBox2Vierge = True
	# Ouverture du fichier .tex à compiler
	NomFichierTex = "FichierLaTeX_"+MotRef+".tex"
	FichierTex = open(NomFichierTex, "w", encoding="iso-8859-1")

	# Remplissage du fichier .tex à compiler :
	# Ecriture du préambule du fichier .tex
	FichierTex.write("\\documentclass[a4paper, 11pt,oneside, fleqn]{article}\
\n\n% Import des packages\n\\usepackage[latin1]{inputenc}\n\\usepackage[T1]\
{fontenc}\n\\usepackage[frenchb]{babel}\n\\usepackage{tabulary}\n\\usepackage\
[top=2cm, bottom=2cm, left=2cm, right=1cm]{geometry}\n\\usepackage{setspace}\
\n\\usepackage{hyperref}\n\\usepackage{frcursive}\n\\usepackage{collcell}\n\
\\usepackage{bookman}\n\n% Debut du document\n\\begin{document}\n\n% Creation\
des nouvelles commandes\n\\newcommand{\\x}{\\times}\n\\newcolumntype{h}\
{>{\\Large\\bfseries\\arraybackslash}C}\n\\newcolumntype{g}{>{\\large\\\
collectcell\\MakeUppercase}h<{\\endcollectcell}}\n\\newcolumntype{i}{>{\\Large\
\\cursive}h}\n\\renewcommand{\\arraystretch}{1.5}\n\n% Parametres du document\
\n\\sloppy\n\\pagestyle{empty}\n\\begin{onehalfspace}\n\n% Corps du document\
\n\n    % En-tete :\n\\sffamily \\noindent \\Large Pr\\\'enom : \\fbox{\\begin\
{minipage}{9cm} \\vspace{1.2cm}\\hspace{9cm} \\end{minipage}} \\hspace{1.5cm}\
\\Large Date :\\vspace{2mm}\\\\\n\\begin{minipage}{12cm}\n\\begin{center}\n\
\\Large\\textbf{Langage \\\'ecrit - Le mot \\MakeUppercase{"+MotRef+"}}\n\
\\end{center}\n\\normalsize Nous avons d\\\'ecouvert puis appris \\`a m\
\\\'emoriser le mot\\\\\n\\MakeUppercase{"+MotRef+"}\\\\\nNous pouvons le\
 retrouver dans une liste de mots : \\end{minipage}\\\\\n\\vspace{0.25cm}\\\\\n\
 \n    % Tableaux : \n")
	# Si l'écriture capitale a été choisie :
	if Capitale == True:
		LignesCapitale = ""
		# Pour chaque ligne :
		for i in range (NombreLignes):
			Ligne = []
			# Ajout des mots de référence en fonction du nombre et de la
			# probabilité choisie
			for j in range (NombreMotRef):
				JetonMotRef = randint(1,100)
				if JetonMotRef >= (100-ProbaMotRef):
					Ligne.append((MotRef+"\n"))
			# Si la ligne n'est pas pleine :
			if len(Ligne) < 5:
				print(len(Ligne))
				# Pour chaque trou :
				for j in range (5-len(Ligne)):
					JetonAutres = randint(1,100)
					# Remplissage en fonction des probabilités choisies
					if JetonAutres <= ProbaTProche:
						JetonMot = randint(0, (len(ContenuListeTProche)-1))
						MotChoisi = ContenuListeTProche[JetonMot]
						Ligne.append(MotChoisi)
					elif JetonAutres > ProbaTProche and JetonAutres <=\
 (ProbaTProche + ProbaProche):
						JetonMot = randint(0, (len(ContenuListeProche)-1))
						MotChoisi = ContenuListeProche[JetonMot]
						Ligne.append(MotChoisi)
					elif JetonAutres > (ProbaTProche + ProbaProche):
						JetonMot = randint(0, (len(ContenuListeRef)-1))
						MotChoisi = ContenuListeRef[JetonMot]
						Ligne.append(MotChoisi)
			# On mélange la ligne
			shuffle(Ligne)
			ChaineAAjouter = ""
			# On formate la ligne au format d'une ligne de tableau LaTeX
			print(Ligne)
			for j in range (len(Ligne)):
				ChaineAAjouter = ChaineAAjouter + (Ligne[j])[:-1] + " & "
			ChaineAAjouter = ChaineAAjouter[:-2]
			ChaineAAjouter = ChaineAAjouter + "\\\\\n\\hline\n"
			print(ChaineAAjouter)
			LignesCapitale = LignesCapitale + ChaineAAjouter
			print(LignesCapitale)
		# On écrit dans le fichier .tex le tableau créé
		FichierTex.write("        % Capitale\n\\large\\noindent En capitale\
 :\n\\begin{center}\n{\\huge \\textbf{\\MakeUppercase{"+MotRef+"}}}\n\
\\vspace{0.25cm}\\\\\n\\begin{tabulary}{17cm}{|g|g|g|g|g|}\n\\hline\n"+\
LignesCapitale+"\\end{tabulary}\n\\end{center}\n\\vspace{0.5cm}\n\n")

	# Si l'écriture script a été choisie :
	if Script == True:
		LignesScript = ""
		# Pour chaque ligne :
		for i in range (NombreLignes):
			Ligne = []
			# Ajout des mots de référence en fonction du nombre et de la
			# probabilité choisie
			for j in range (NombreMotRef):
				JetonMotRef = randint(1,100)
				if JetonMotRef >= (100-ProbaMotRef):
					Ligne.append((MotRef+"\n"))
			# Si la ligne n'est pas pleine :
			if len(Ligne) < 5:
				# Pour chaque trou :
				for j in range (5-len(Ligne)):
					JetonAutres = randint(1,100)
					# Remplissage en fonction des probabilités choisies
					if JetonAutres <= ProbaTProche:
						JetonMot = randint(0, (len(ContenuListeTProche)-1))
						MotChoisi = ContenuListeTProche[JetonMot]
						Ligne.append(MotChoisi)
					elif JetonAutres > ProbaTProche and JetonAutres <=\
 (ProbaTProche + ProbaProche):
						JetonMot = randint(0, (len(ContenuListeProche)-1))
						MotChoisi = ContenuListeProche[JetonMot]
						Ligne.append(MotChoisi)
					elif JetonAutres > (ProbaTProche + ProbaProche):
						JetonMot = randint(0, (len(ContenuListeRef)-1))
						MotChoisi = ContenuListeRef[JetonMot]
						Ligne.append(MotChoisi)
			# On mélange la ligne
			shuffle(Ligne)
			ChaineAAjouter = ""
			# On formate la ligne au format d'une ligne de tableau LaTeX
			print(Ligne)
			for j in range (len(Ligne)):
				ChaineAAjouter = ChaineAAjouter + (Ligne[j])[:-1] + " & "
			ChaineAAjouter = ChaineAAjouter[:-2]
			ChaineAAjouter = ChaineAAjouter + "\\\\\n\\hline\n"
			print(ChaineAAjouter)
			LignesScript = LignesScript + ChaineAAjouter
			print(LignesScript)
		# On écrit dans le fichier .tex le tableau créé
		FichierTex.write("        % Script\n\\large\\noindent En script\
 :\n\\begin{center} {\\huge \\textbf{"+MotRef+"}}\n\\vspace{0.25cm}\\\\\
\n\\begin{tabulary}{17cm}{|h|h|h|h|h|}\n\\hline\n"+LignesScript+\
"\\end{tabulary}\n\\end{center}\n\\vspace{0.5cm}\n\n")

	# Si l'écriture script a été choisie :
	if Cursive == True:
		LignesCursive = ""
		# Pour chaque ligne :
		for i in range (NombreLignes):
			Ligne = []
			# Ajout des mots de référence en fonction du nombre et de la
			# probabilité choisie
			for j in range (NombreMotRef):
				JetonMotRef = randint(1,100)
				# Remplissage en fonction des probabilités choisies
				if JetonMotRef >= (100-ProbaMotRef):
					Ligne.append((MotRef+"\n"))
			# Si la ligne n'est pas pleine :
			if len(Ligne) < 5:
				# Pour chaque trou :
				for j in range (5-len(Ligne)):
					JetonAutres = randint(1,100)
					if JetonAutres <= ProbaTProche:
						JetonMot = randint(0, (len(ContenuListeTProche)-1))
						MotChoisi = ContenuListeTProche[JetonMot]
						Ligne.append(MotChoisi)
					elif JetonAutres > ProbaTProche and JetonAutres <=\
 (ProbaTProche + ProbaProche):
						JetonMot = randint(0, (len(ContenuListeProche)-1))
						MotChoisi = ContenuListeProche[JetonMot]
						Ligne.append(MotChoisi)
					elif JetonAutres > (ProbaTProche + ProbaProche):
						JetonMot = randint(0, (len(ContenuListeRef)-1))
						MotChoisi = ContenuListeRef[JetonMot]
						Ligne.append(MotChoisi)
			# On mélange la ligne
			shuffle(Ligne)
			ChaineAAjouter = ""
			# On formate la ligne au format d'une ligne de tableau LaTeX
			print(Ligne)
			for j in range (len(Ligne)):
				ChaineAAjouter = ChaineAAjouter + (Ligne[j])[:-1] + " & "
			ChaineAAjouter = ChaineAAjouter[:-2]
			ChaineAAjouter = ChaineAAjouter + "\\\\\n\\hline\n"
			print(ChaineAAjouter)
			LignesCursive = LignesCursive + ChaineAAjouter
			print(LignesCursive)
		# On écrit dans le fichier .tex le tableau créé
		FichierTex.write("        % Cursive\n\\large\\noindent En cursive\
 :\n\\begin{center}\n{\\huge \\textbf {{\\cursive "+MotRef+"}}}\n\
\\vspace{0.25cm}\\\\\n\\begin{tabulary}{17cm}{|i|i|i|i|i|}\n\\hline\n"+\
LignesCursive+"\\end{tabulary}\n\\end{center}\n\n")

	# Fin de l'écriture :
	# On écrit la fin du fichier .tex
	FichierTex.write("% Fin du document\n\\end{onehalfspace}\n\\end{document}\
\n")
	# On ferme le fichier .tex, et on affiche un message de confirmation
	FichierTex.close()
	MessageEtat("FTEX généré !")
	# On ferme les autres fichiers ouverts
	ListeRef.close()
	ListeTProche.close()
	ListeProche.close()

	# Compilation du fichier .tex :
	# On prépare des commandes de compilation et d'affichage
	Commande1 = "pdflatex "+NomFichierTex
	Commande2 = "pdflatex "+NomFichierTex
	Commande3 = "start chrome \""+os.getcwd()+"\\"+NomFichierTex[:-3]+"pdf\""
	# On compile le fichier .tex et on affiche le fichier .pdf
	try:
		os.system(Commande1)
		os.system(Commande2)
		os.system(Commande3)
		MessageEtat("FTEX compilé !")
	except:
		# En cas d'erreur, on affiche la fenêtre d'erreur
		Erreur()
	# On revient au répertoire de départ
	os.chdir("../../")

		# Fonction "ParDefaut" qui réinitialise les paramètres de l'interface #
def ParDefaut():
	# Réinitialisation du mot de référence
	MotRefStringVar.set("cochon")
	# Réinitialisation des écritures choisies
	CapitaleIntVar.set(1)
	ScriptIntVar.set(0)
	CursiveIntVar.set(0)
	# Réinitialisation du nombre de ligne
	NombreLignesStringVar.set("5")
	# Réinitialisation du nombre de mots de référence
	NombreMotRefStringVar.set("1")
	# Réinitialisation de la probabilité d'apparition du mot de référence
	ProbaMotRefStringVar.set("80")
	# Réinitialisation des probabilités des autres mots
	ProbaMotsTProchesStringVar.set("40")
	ProbaMotsProchesStringVar.set("40")
	FEntryProbaMotsDivers.config(text="20")
	# Réinitialisation des définitions des mots proches et très proches
	CheckTProcheIntVar103.set(0)
	CheckTProcheIntVar102.set(0)
	CheckTProcheIntVar14.set(0)
	CheckTProcheIntVar13.set(1)
	CheckTProcheIntVar31.set(0)
	CheckProcheIntVar102.set(0)
	CheckProcheIntVar13.set(0)
	CheckProcheIntVar12.set(1)
	CheckProcheIntVar31.set(0)
	CheckProcheIntVar21.set(0)
	# Réinitialisation de la liste de mots de référence
	ListeMotsStringVar.set("ListeMots.txt")
	# Désactivation du mode avancé
	ModeAvanceeIntVar.set(0)
	ModeAvanceeToggle()

		# Fonction "CalculerProbaMotsDivers" qui calcule la probabilité
		# complémentaire des autres mots
def CalculerProbaMotsDivers():
	global ProbaTProche
	global ProbaProche
	# Récupération de la probabilité des mots très proches
	ProbaTProcheBrut = ProbaMotsTProchesStringVar.get()
	# Vérification de la validité de la probabilité des mots très proches
	try:
		ProbaTProche = int(ProbaTProcheBrut)
	except:
		MessageEtat("Erreur : PTP invalide")
		ProbaMotsTProchesStringVar.set("40")
		ProbaTProcheBrut = ProbaMotsTProchesStringVar.get()
		ProbaTProche = int(ProbaTProcheBrut)
	if ProbaTProche < 0 or ProbaTProche >= 100:
		MessageEtat("Erreur : PTP invalide")
		ProbaMotsTProchesStringVar.set("40")
		ProbaTProcheBrut = ProbaMotsTProchesStringVar.get()
		ProbaTProche = int(ProbaTProcheBrut)
	# Récupération de la probabilité des mots proches
	ProbaProcheBrut = ProbaMotsProchesStringVar.get()
	# Vérification de la validité de la probabilité des mots proches
	try:
		ProbaProche = int(ProbaProcheBrut)
	except:
		MessageEtat("Erreur : PP invalide")
		ProbaMotsProchesStringVar.set("40")
		ProbaProcheBrut = ProbaMotsProchesStringVar.get()
		ProbaProche = int(ProbaProcheBrut)
	if ProbaProche < 0 or ProbaProche >= 100:
		MessageEtat("Erreur : PP invalide")
		ProbaMotsProchesStringVar.set("40")
		ProbaProcheBrut = ProbaMotsProchesStringVar.get()
		ProbaProche = int(ProbaProcheBrut)
	# Vérification que la somme ne dépasse pas déjà 100
	if ProbaTProche + ProbaProche > 100:
		MessageEtat("Erreur : PTP & PP invalide")
		ProbaMotsTProchesStringVar.set("40")
		ProbaTProcheBrut = ProbaMotsTProchesStringVar.get()
		ProbaTProche = int(ProbaTProcheBrut)
		ProbaMotsProchesStringVar.set("40")
		ProbaProcheBrut = ProbaMotsProchesStringVar.get()
		ProbaProche = int(ProbaProcheBrut)
	# Calcul de la probabilité de mots divers et affichage
	ProbaDivers = 100 - (ProbaTProche + ProbaProche)
	FEntryProbaMotsDivers.config(text=ProbaDivers)

		# Fonction "Aide" qui affiche le .pdf d'aide #
def Aide():
	try:
		os.system("start chrome \""+os.getcwd()+"\\Aide.pdf\"")
	except:
		MessageEtat("Erreur : Aide")

		# Fonction "MessageEtat" qui fait transforme les "EtatBox"'s en panneau
		# d'information roulant
def MessageEtat(Message):
	global EtatBox1Vierge
	global EtatBox2Vierge
	global EtatBox3Vierge
	# Mécanisme qui permet d'afficher les messages en haut si le champ n'a
	# jamais été utilisé
	if EtatBox1Vierge is True and EtatBox2Vierge is True and\
 EtatBox3Vierge is True:
		EtatBox1StringVar.set(Message)
		EtatBox1Vierge = False
	elif EtatBox1Vierge is False and EtatBox2Vierge is True and\
 EtatBox3Vierge is True:
		EtatBox2StringVar.set(Message)
		EtatBox2Vierge = False
	elif EtatBox1Vierge is False and EtatBox2Vierge is False and\
 EtatBox3Vierge is True:
		EtatBox3StringVar.set(Message)
		EtatBox3Vierge = False
	# Si les champs ont déjà été utilisés, roulement simple des informations :
	else :
		Message2 = EtatBox2StringVar.get()
		Message3 = EtatBox3StringVar.get()
		# Le message 2 passe dans l'EtatBox1
		EtatBox1StringVar.set(Message2)
		# Le message 3 passe dans l'EtatBox2
		EtatBox2StringVar.set(Message3)
		# Le nouveau message passe dans l'EtatBox3
		EtatBox3StringVar.set(Message)
		# (Le message 1, le plus ancien, est supprimé)

		# Fonction "ModeAvanceeToggle" qui permet d'activer/désactiver le mode
		# avancé
def ModeAvanceeToggle():
	global ModeAvanceeBool
	# Si le mode avancé est désactivé lors du clic sur le checkbutton :
	if ModeAvanceeBool is False:
		# On active tous les champs
		LabelDefTProche.config(state=NORMAL)
		LabelCommunTProche.config(state=NORMAL)
		CheckTProche103.config(state=NORMAL)
		CheckTProche102.config(state=NORMAL)
		CheckTProche14.config(state=NORMAL)
		CheckTProche13.config(state=NORMAL)
		CheckTProche31.config(state=NORMAL)
		LabelDefProche.config(state=NORMAL)
		LabelCommunProche.config(state=NORMAL)
		CheckProche102.config(state=NORMAL)
		CheckProche13.config(state=NORMAL)
		CheckProche12.config(state=NORMAL)
		CheckProche31.config(state=NORMAL)
		CheckProche21.config(state=NORMAL)
		LabelListeMots.config(state=NORMAL)
		EntryListeMots.config(state=NORMAL)
		# Le mode avancé est alors activé
		ModeAvanceeBool = True
	# Si le mode avancé est activé lors du clic sur le checkbutton :
	elif ModeAvanceeBool is True:
		# On désactive tous les champs
		LabelDefTProche.config(state=DISABLED)
		LabelCommunTProche.config(state=DISABLED)
		CheckTProche103.config(state=DISABLED)
		CheckTProche102.config(state=DISABLED)
		CheckTProche14.config(state=DISABLED)
		CheckTProche13.config(state=DISABLED)
		CheckTProche31.config(state=DISABLED)
		LabelDefProche.config(state=DISABLED)
		LabelCommunProche.config(state=DISABLED)
		CheckProche102.config(state=DISABLED)
		CheckProche13.config(state=DISABLED)
		CheckProche12.config(state=DISABLED)
		CheckProche31.config(state=DISABLED)
		CheckProche21.config(state=DISABLED)
		LabelListeMots.config(state=DISABLED)
		EntryListeMots.config(state=DISABLED)
		# On réinitialise les variables du mode avancé
		CheckTProcheIntVar103.set(0)
		CheckTProcheIntVar102.set(0)
		CheckTProcheIntVar14.set(0)
		CheckTProcheIntVar13.set(1)
		CheckTProcheIntVar31.set(0)
		CheckProcheIntVar102.set(0)
		CheckProcheIntVar13.set(0)
		CheckProcheIntVar12.set(1)
		CheckProcheIntVar31.set(0)
		CheckProcheIntVar21.set(0)
		ListeMotsStringVar.set("ListeMots.txt")
		# Le mode avancé est alors désactivé
		ModeAvanceeBool = False

  #### 2. Corps du programme ####

	### 2.1. Création de la fenêtre master ###

# On crée une fenêtre "tkinter"
Master = Tk()
Master.title("Sheet Creator X")
Master.protocol("WM_DELETE_WINDOW", Master.quit)
# On bind les touches du clavier
Master.bind("<Return>", Generer)
Master.bind("<Escape>", ParDefaut)

	### 2.2. Création des différentes parties de l'interface ###

	  ## 2.2.1. Création de la fenêtre basique ##
FenetreBasique = Frame(Master, bd=1, padx=5, pady=5, relief=GROOVE,\
 takefocus=1, width=280)
FenetreBasique.grid(row=0, column=0, sticky=W+E+N+S)
# Création du séparateur de fenêtres
Separateur1 = Frame(Master, bd=1, relief=SUNKEN, width=3)
Separateur1.grid(row=0, column=1, sticky=W+E+N+S)

	  ## 2.2.2. Création de la fenêtre avancée ##
FenetreAvancee = Frame(Master, bd=1, padx=5, pady=5, relief=GROOVE,\
 width=280)
FenetreAvancee.grid(row=0, column=2, sticky=W+E+N+S)
# Création du séparateur de fenêtres
Separateur2 = Frame(Master, bd=1, relief=SUNKEN, width=560, height=3)
Separateur2.grid(row=1, column=0, sticky=W+E+N+S, columnspan=3)

	  ## 2.2.3. Création de la fenêtre contrôle ##
FenetreControle = Frame(Master, bd=1, padx=5, pady=5, relief=GROOVE,\
 width=280)
FenetreControle.grid(row=2, column=0, sticky=W+E+N+S)
# Création du séparateur de fenêtres
Separateur3 = Frame(Master, bd=1, relief=SUNKEN, width=3)
Separateur3.grid(row=2, column=1, sticky=W+E+N+S)

	  ## 2.2.4. Création de la fenêtre état ##
FenetreEtat = Frame(Master, bd=1, padx=5, pady=5, relief=GROOVE,\
 width=280)
FenetreEtat.grid(row=2, column=2, sticky=W+E+N+S)

	### 2.3. Remplissage des fenêtres ###

	  ## 2.3.1. Remplissage de la fenêtre basique ##

# Création d'un espace à centrer
Espace2 = Frame(FenetreBasique, relief=FLAT, bd=0, padx=0, pady=0, height=20)
Espace2.grid(row=0, column=0, columnspan=3, sticky=W+E+N+S)
# Création de la sous-fenêtre de saisie du mot de référence
SFenetreMotRef = Frame(FenetreBasique, relief=GROOVE, bd=1,\
 padx=5, pady=5, width=280)
SFenetreMotRef.grid(row=1, column=0, columnspan=3, sticky=W+E+N+S)
LabelMotRef = Label(SFenetreMotRef, text="  Mot de référence (Au moins\
 3 lettres) :  ")
LabelMotRef.grid(row=0, column=0, sticky=W+E+N+S)
MotRefStringVar = StringVar()
MotRefStringVar.set("cochon")
EntryMotRef = Entry(SFenetreMotRef, textvariable=MotRefStringVar,\
width = 33)
EntryMotRef.grid(row=1, column=0, sticky=W+E+N+S)
# Création du séparateur de sous-fenêtre
Separateur4 = Frame(FenetreBasique, bd=1, relief=SUNKEN, width=280,\
 height=3)
Separateur4.grid(row=2, column=0, sticky=W+E+N+S, columnspan=3)
# Création de la sous-fenêtre de choix des écritures
SFenetreEcrtitures = Frame(FenetreBasique, relief=GROOVE, bd=1,\
 padx=5, pady=5)
SFenetreEcrtitures.grid(row=3, column=0, sticky=W+E+N+S)
CapitaleIntVar = IntVar()
CapitaleIntVar.set(1)
CheckCapitale = Checkbutton(SFenetreEcrtitures, text="  Capitale  ",\
 variable=CapitaleIntVar)
CheckCapitale.grid(row=0, column=0, sticky=W+N+S)
ScriptIntVar = IntVar()
CheckScript = Checkbutton(SFenetreEcrtitures, text="  Script  ",\
 variable=ScriptIntVar)
CheckScript.grid(row=1, column=0, sticky=W+N+S)
CursiveIntVar=IntVar()
CheckCursive = Checkbutton(SFenetreEcrtitures, text="  Cursive  ",\
 variable=CursiveIntVar)
CheckCursive.grid(row=2, column=0, sticky=W+N+S)
# Création du séparateur de sous-fenêtre
Separateur5 = Frame(FenetreBasique, bd=1, relief=SUNKEN, width=3)
Separateur5.grid(row=3, column=1, sticky=W+E+N+S)
# Création de la fenêtre de saisie du nombre de lignes
SFenetreNombreLignes = Frame(FenetreBasique, relief=GROOVE, bd=1,\
 padx=5, pady=5)
SFenetreNombreLignes.grid(row=3, column=2, sticky=W+E+N+S)
LabelNombreLignes = Label(SFenetreNombreLignes,\
 text="  Nombre de lignes  \n  par écriture :  ")
LabelNombreLignes.grid(row=0, column=0, sticky=W+E+N+S)
NombreLignesStringVar = StringVar()
NombreLignesStringVar.set("5")
EntryNombreLignes = Entry(SFenetreNombreLignes,\
 textvariable=NombreLignesStringVar)
EntryNombreLignes.grid(row=1, column=0, sticky=W+E+N+S)
# Création du séparateur de sous-fenêtre
Separateur6 = Frame(FenetreBasique, bd=1, relief=SUNKEN, width=280,\
 height=3)
Separateur6.grid(row=4, column=0, sticky=W+E+N+S, columnspan=3)
# Création de la sous-fenêtre de paramètres de génération du mot de référence
LabelGenerationMotRef = Label(FenetreBasique,\
 text="  Génération du mot de référence :  ")
LabelGenerationMotRef.grid(row=5, column=0, sticky=W+E+N+S,\
 columnspan=3)
SFenetreProbaMotRef = Frame(FenetreBasique, relief=GROOVE, bd=1,\
 padx=5, pady=5)
SFenetreProbaMotRef.grid(row=6, column=0, sticky=W+E+N+S, columnspan=3)
LabelNombreMotRef = Label(SFenetreProbaMotRef, justify=LEFT,\
 text="  Nombre de mots de \n  référence\
 par ligne (1-5) : ")
LabelNombreMotRef.grid(row=0, column=0, sticky=W+N+S)
NombreMotRefStringVar = StringVar()
NombreMotRefStringVar.set("1")
EntryNombreMotRef = Entry(SFenetreProbaMotRef,\
 textvariable=NombreMotRefStringVar, width=4, justify=CENTER)
EntryNombreMotRef.grid(row=0, column=1, sticky=E+N+S)
LabelProbaMotRef = Label(SFenetreProbaMotRef, justify=LEFT,\
 text="  Probabilité d'apparition du mot de \n  référence sur les\
 lignes  (0-100 %) : ")
LabelProbaMotRef.grid(row=1, column=0, sticky=W+N+S)
ProbaMotRefStringVar = StringVar()
ProbaMotRefStringVar.set("80")
EntryProbaMotRef= Entry(SFenetreProbaMotRef,\
 textvariable=ProbaMotRefStringVar, width=4, justify=CENTER)
EntryProbaMotRef.grid(row=1, column=1, sticky=E+N+S)
# Création du séparateur de sous-fenêtre
Separateur7 = Frame(FenetreBasique, bd=1, relief=SUNKEN, width=280,\
 height=3)
Separateur7.grid(row=7, column=0, sticky=W+E+N+S, columnspan=3)
# Création de la sous-fenêtre de paramètre de génération des autres mots
LabelGenerationAutres = Label(FenetreBasique,\
 text="  Génération du reste de la grille :  ")
LabelGenerationAutres.grid(row=8, column=0, sticky=W+E+N+S,\
 columnspan=3)
SFenetreProbaAutres = Frame(FenetreBasique, relief=GROOVE, bd=1,\
 padx=5, pady=5)
SFenetreProbaAutres.grid(row=9, column=0, sticky=W+E+N+S, columnspan=3)
LabelInfoProbaAutres = Label(SFenetreProbaAutres, text=" Très proches\
 + Proches + Divers = 100 % ")
LabelInfoProbaAutres.grid(row=0, column=0, columnspan=2, sticky=W+E+N+S)
LabelProbaMotsTProches = Label(SFenetreProbaAutres, text="  Mots très\
 proches (0-100 %) :          ", justify=LEFT)
LabelProbaMotsTProches.grid(row=1, column=0, sticky=W+N+S)
ProbaMotsTProchesStringVar = StringVar()
ProbaMotsTProchesStringVar.set("40")
EntryProbaMotsTProches = Entry(SFenetreProbaAutres,\
 textvariable=ProbaMotsTProchesStringVar, justify=CENTER, width=4)
EntryProbaMotsTProches.grid(row=1, column=1, sticky=E+N+S)
LabelProbaMotsProches = Label(SFenetreProbaAutres, text="  Mots\
 proches (0-100 %) :                ", justify=LEFT)
LabelProbaMotsProches.grid(row=2, column=0, sticky=W+N+S)
ProbaMotsProchesStringVar = StringVar()
ProbaMotsProchesStringVar.set("40")
EntryProbaMotsProches = Entry(SFenetreProbaAutres,\
 textvariable=ProbaMotsProchesStringVar, justify=CENTER, width=4)
EntryProbaMotsProches.grid(row=2, column=1, sticky=E+N+S)
SSFenetreDivers = Frame(SFenetreProbaAutres)
SSFenetreDivers.grid(row=3, column=0, columnspan=2, sticky=W+E+N+S)
LabelProbaMotsDivers = Label(SSFenetreDivers, text="  Mots divers\
 (0-100 %) :    ", justify=LEFT)
LabelProbaMotsDivers.grid(row=0, column=0, sticky=W+N+S)
BoutonCalculerProbaMotsDivers = Button(SSFenetreDivers,\
 text="Calculer", padx=2, pady=1, command=CalculerProbaMotsDivers)
BoutonCalculerProbaMotsDivers.grid(row=0, column=1, sticky=W+E+N+S)
Espace1 = Label(SSFenetreDivers, text=" ")
Espace1.grid(row=0, column=2, sticky=W+E+N+S)
FEntryProbaMotsDivers= Label(SSFenetreDivers, text="20", width=4,\
 justify=CENTER, bd=1, relief=SUNKEN)
FEntryProbaMotsDivers.grid(row=0, column=3, sticky=E+N+S)

	  ## 2.3.2. Remplissage de la fenêtre avancée ##

# Création du bouton d'activation/désactivation du mode avancé
ModeAvanceeIntVar = IntVar()
CheckModeAvancee = Checkbutton(FenetreAvancee, text="                  \
Mode Avancé                     ",\
 variable=ModeAvanceeIntVar, command=ModeAvanceeToggle)
CheckModeAvancee.grid(row=0, column=0, sticky=W+E+N+S)
SFenetreAvancee = Frame(FenetreAvancee, relief=GROOVE, bd=1,\
 padx=5, pady=5, width=280, height=335)
SFenetreAvancee.grid(row=1, column=0, sticky=W+E+N+S)
# Création de la sous-sous-fenêtre de définition de mots très proches
LabelDefTProche = Label(SFenetreAvancee, text="  Définition de \"Mots\
 très proches\" :          ", justify=LEFT)
LabelDefTProche.grid(row=0, column=0, sticky=W+N+S)
SSFenetreDefTProche = Frame(SFenetreAvancee, relief=GROOVE, bd=1,\
 padx=5, pady=5, width=280)
SSFenetreDefTProche.grid(row=1, column=0, sticky=W+E+N+S)
LabelCommunTProche = Label(SSFenetreDefTProche, text="    En commun\
              ", justify=LEFT)
LabelCommunTProche.grid(row=0, column=0, sticky=W+E+N+S)

CheckTProcheIntVar103 = IntVar()
CheckTProcheIntVar103.set(0)
CheckTProcheIntVar102 = IntVar()
CheckTProcheIntVar102.set(0)
CheckTProcheIntVar14 = IntVar()
CheckTProcheIntVar14.set(0)
CheckTProcheIntVar13 = IntVar()
CheckTProcheIntVar13.set(1)
CheckTProcheIntVar31 = IntVar()
CheckTProcheIntVar31.set(0)

CheckTProche103 = Checkbutton(SSFenetreDefTProche,\
 text="Début ou Fin sur 3 Lettres", variable=CheckTProcheIntVar103)
CheckTProche103.grid(row=1, column=0, sticky=W+N+S)
CheckTProche102 = Checkbutton(SSFenetreDefTProche,\
 text="Début ou Fin sur 2 Lettres", variable=CheckTProcheIntVar102)
CheckTProche102.grid(row=2, column=0, sticky=W+N+S)
CheckTProche14 = Checkbutton(SSFenetreDefTProche,\
 text="1 x 4 Lettres successives", variable=CheckTProcheIntVar14)
CheckTProche14.grid(row=3, column=0, sticky=W+N+S)
CheckTProche13 = Checkbutton(SSFenetreDefTProche,\
 text="1 x 3 Lettres successives", variable=CheckTProcheIntVar13)
CheckTProche13.grid(row=4, column=0, sticky=W+N+S)
CheckTProche31 = Checkbutton(SSFenetreDefTProche,\
 text="3 x 1 Lettres indépendantes", variable=CheckTProcheIntVar31)
CheckTProche31.grid(row=5, column=0, sticky=W+N+S)
# Création du séparateur de sous-fenêtre
Separateur8 = Frame(SFenetreAvancee, bd=1, relief=SUNKEN, width=280,\
 height=3)
Separateur8.grid(row=2, column=0, sticky=W+E+N+S)
# Création de la sous-sous-fenêtre de définition de mots proches
LabelDefProche = Label(SFenetreAvancee, text="  Définition de \"Mots\
 proches\" :                ", justify=LEFT)
LabelDefProche.grid(row=3, column=0, sticky=W+N+S)
SSFenetreDefProche = Frame(SFenetreAvancee, relief=GROOVE, bd=1,\
 padx=5, pady=5, width=280)
SSFenetreDefProche.grid(row=4, column=0, sticky=W+E+N+S)
LabelCommunProche = Label(SSFenetreDefProche, text="    En commun\
              ", justify=LEFT)
LabelCommunProche.grid(row=0, column=0, sticky=W+E+N+S)

CheckProcheIntVar102 = IntVar()
CheckProcheIntVar102.set(0)
CheckProcheIntVar13 = IntVar()
CheckProcheIntVar13.set(0)
CheckProcheIntVar12 = IntVar()
CheckProcheIntVar12.set(1)
CheckProcheIntVar31 = IntVar()
CheckProcheIntVar31.set(0)
CheckProcheIntVar21 = IntVar()
CheckProcheIntVar21.set(0)

CheckProche102 = Checkbutton(SSFenetreDefProche,\
 text="Début ou Fin sur 2 Lettres", variable=CheckProcheIntVar102)
CheckProche102.grid(row=1, column=0, sticky=W+N+S)
CheckProche13 = Checkbutton(SSFenetreDefProche,\
 text="1 x 3 Lettres successives", variable=CheckProcheIntVar13)
CheckProche13.grid(row=2, column=0, sticky=W+N+S)
CheckProche12 = Checkbutton(SSFenetreDefProche,\
 text="1 x 2 Lettres successives", variable=CheckProcheIntVar12)
CheckProche12.grid(row=3, column=0, sticky=W+N+S)
CheckProche31 = Checkbutton(SSFenetreDefProche,\
 text="3 x 1 Lettres indépendantes", variable=CheckProcheIntVar31)
CheckProche31.grid(row=4, column=0, sticky=W+N+S)
CheckProche21 = Checkbutton(SSFenetreDefProche,\
 text="2 x 1 Lettres indépendantes", variable=CheckProcheIntVar21)
CheckProche21.grid(row=5, column=0, sticky=W+N+S)
# Création du séparateur de sous-fenêtre
Separateur9 = Frame(SFenetreAvancee, bd=1, relief=SUNKEN, width=280,\
 height=3)
Separateur9.grid(row=5, column=0, sticky=W+E+N+S)
# Création de la zone de choix/saisie de la liste de mots de référence
LabelListeMots = Label(SFenetreAvancee, text="  Liste de mots (.txt)\
 :  ")
LabelListeMots.grid(row=6, column=0, sticky=W+N+S)
ListeMotsStringVar = StringVar()
ListeMotsStringVar.set("ListeMots.txt")
EntryListeMots = Entry(SFenetreAvancee, textvariable=ListeMotsStringVar\
,width=30)
EntryListeMots.grid(row=7, column=0, sticky=W+E+N+S)
# Désactivation par défaut du mode avancé
ModeAvanceeBool = False
LabelDefTProche.config(state=DISABLED)
LabelCommunTProche.config(state=DISABLED)
CheckTProche103.config(state=DISABLED)
CheckTProche102.config(state=DISABLED)
CheckTProche14.config(state=DISABLED)
CheckTProche13.config(state=DISABLED)
CheckTProche31.config(state=DISABLED)
LabelDefProche.config(state=DISABLED)
LabelCommunProche.config(state=DISABLED)
CheckProche102.config(state=DISABLED)
CheckProche13.config(state=DISABLED)
CheckProche12.config(state=DISABLED)
CheckProche31.config(state=DISABLED)
CheckProche21.config(state=DISABLED)
LabelListeMots.config(state=DISABLED)
EntryListeMots.config(state=DISABLED)

	  ## 2.3.3. Remplissage de la fenêtre contrôle ##

# Création du bouton générer
BoutonGenerer = Button(FenetreControle, text = "  Générer  ",\
 command=Generer, width=14)
BoutonGenerer.grid(row=0, column=0, sticky=W+E+N+S)
# Création du bouton par défaut
BoutonParDefaut = Button(FenetreControle, text="  Par Défaut  ",\
 command=ParDefaut, width=14)
BoutonParDefaut.grid(row=0, column=1, sticky=W+E+N+S)
# Création du bouton aide
BoutonAide = Button(FenetreControle, text="  Aide  ",\
 command=Aide, width=14)
BoutonAide.grid(row=1, column=0, sticky=W+E+N+S)
# Création du bouton quitter
BoutonQuitter = Button(FenetreControle, text="  Quitter  ",\
 command=Master.quit, width=14)
BoutonQuitter.grid(row=1, column=1, sticky=W+E+N+S)

	  ## 2.3.4. Remplissage de la fenêtre état ##

LabelEtat = Label(FenetreEtat, text="  Etat :  ")
LabelEtat.grid(row=0, column=0, sticky=W+N+S)
# Création de l'EtatBox1
EtatBox1StringVar = StringVar()
EtatBox1StringVar.set("  Saisie des informations  ")
EtatBox1 = Label(FenetreEtat, textvariable=EtatBox1StringVar, width=26,\
 relief=GROOVE, bd=1)
EtatBox1.grid(row=0, column=1, sticky=W+E+N+S)
EtatBox1Vierge = True
# Création de l'EtatBox2
EtatBox2StringVar = StringVar()
EtatBox2StringVar.set("  ...  ")
EtatBox2 = Label(FenetreEtat, textvariable=EtatBox2StringVar, width=26,\
 relief=GROOVE, bd=1)
EtatBox2.grid(row=1, column=1, sticky=W+E+N+S)
EtatBox2Vierge = True
# Création de l'EtatBox3
EtatBox3StringVar = StringVar()
EtatBox3StringVar.set("  ...  ")
EtatBox3 = Label(FenetreEtat, textvariable=EtatBox3StringVar, width=26,\
 relief=GROOVE, bd=1)
EtatBox3.grid(row=2, column=1, sticky=W+E+N+S)
EtatBox3Vierge = True

  #### 3. Fermeture des fenêtres ####

# Bouclage de la fenêtre master
Master.mainloop()
# Destruction de la fenêtre master
Master.destroy()

##### Fin du programme #####
