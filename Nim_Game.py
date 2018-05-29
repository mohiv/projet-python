#!/usr/bin/python3


from random import *

#lire le score a partir du fichier score.txt
def read_scores():
	d = {}
	
	try :
		f = open("score.txt", "r")
		for i in f :
				name, best, last, _ = i.split(';')
				d[ name ] = [ float(best), float(last) ]
		f.close()

	except :
		f = open("score.txt", "w")
		f.close()

	return d
#sauvgarder le score dans le fichier score.txt
def write_scores(winner, prev, s, J):
	n = sum( i*10**i for i in range(s+1) )

	win = J[winner]
	if win in prev :
		prev[win][1] = n
		
		if n < prev[win][0] :
			prev[win][0] = n

	else :
		prev[win] = (n, n)

	loser = (winner+1)%2
	lose = J[loser]
	if lose in prev:
		prev[lose][1] = float('inf')
	
	else :
		prev[lose] = (float('inf'), float('inf'))

	try :
		f = open("score.txt", "a")
		for J in prev.items() :
			l ="{"+winner+";"+prev[win][0]+";"+prev[win][1]+"};\n"
			f.write(l)
			
	except :
		f = open("score.txt", "w")
		
		for i in prev.items() :
			l = "{"+str(i[0])+"};{"+str(i[1][0])+"};{"+str(i[1][0])+"}\n"
			f.write(l)
		f.close()

	return prev
#fonction qui affiche le score final
def print_scores(prev):
	l = sorted( prev.items(), key=lambda x: x[1][0] )

	print('Meilleurs Scores :')
	for i in range( min(10, len(l)) ) :
		name, best = l[i]
		print( name, ':', best[0] )
#fonction qui affiche l'état de jeu a chaque étape
def afficher(tableau):
	l = max( tableau.values() )
	
	for i in tableau :
		val = tableau[i]
		print( i, '|', val*'*', (l-val)*' ','|', val )

#le main de jeu nim
def Nim():

	a = input( 'Jouer 1 :' )
	b = input( 'Jouer 2 :' )

	J = { 0:a, 1:b }
	i = randrange(0, 2)

	precedant = read_scores()

	tas =  { i : randrange(5, 24) for i in range(1, randrange(4, 9) ) }
	afficher( tas )
	
	tour = 0

	while True :
		c = input( '%s entrer votre coups : '%J[i%2]  )
		
		t, p = c.split('-')
		t, p = eval(t), eval(p)
		
		if min(t, p) < 0 or t > len(tas) :
			print('veillez entrer un coups valide')
			continue
		if p > tas[t] :
			print('veillez entrer un coups valide')
			continue
		 
		tas[t] -= p
		if(tas[t]<1) :
			break 
		tour += 1
		i += 1
		
		afficher(tas)

	gagnant = (sum( tas.values() )+i)%2
	
	d = write_scores(gagnant, precedant, tour, J)
	print_scores(d)

	x = input ("Voulez-vous commencer une nouvelle partie ? [oui/non] : ")
	if x == 'oui' :
		Nim()

Nim()
