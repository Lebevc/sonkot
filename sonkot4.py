# -*- coding=utf-8 -*-
#---------------------------------------------------
# Sončni kot cos(theta) poljubno orientirane ploskve
#
# predelava "sonkot-2.py" na eno samo funkcijo
#
# povzeto po    http://www.powerfromthesun.net/Book/chapter03/chapter03.html
#               http://www.powerfromthesun.net/Book/chapter04/chapter04.html
#---------------------------------------------------------------------------
# Dnevnik:
# 13.12.2016    pričetek iz nič, nomenklatura povzeta po izvirniku (==štala)
#               VSE PRAV, samo malo nastlano počez
# 14.12.2016    zajem iz ene same funkcije. Štetje 'jd' in 'ure leta' od "0"
# 15.12.2016    popravil fellerje - VSE PRAV: +-1% napake glede na 'SOLPOS'
#---------------------------------------------------------------------------
import numpy as np
#---------------------------------------------------------------------------

"""Kličemo eno samo funkcijo z nujnimi parametri, ven prileti cos(theta) na
poljubno orientirano ploskev. porežemo negativne kosinuse. Štetje dni/ur z 0.
G.širina in G.višina v decimalnih stopinjah. Vzhod ima negativne vrednosti.
nagib ploskve [0..pi], zasuk ploskve [0..2*pi], jdura [0..87640]"""

def kosinus(nagib, zasuk, jdura, gsir, gdol):
# izvorni greh
    gsir = np.deg2rad(gsir)             
# sezonski odklon sonca od smeri 'jug'    
    eot0 = np.deg2rad(360*(jdura//24)/365.242)
    eot = 0.258*np.cos(eot0)-7.416*np.sin(eot0)-3.648*np.cos(2*eot0)-9.228*np.sin(2*eot0)
# krajevni sončni čas 'Ts'
    ts0 = (15+gdol)/15.0
    ts = jdura % 24 + eot/60 - ts0
# urni kot sonca
    omega = np.deg2rad(15*(ts-12))
# parameter 3.7 v izračunih 
    delta0 = np.deg2rad(0.98563*(jdura//24-172))
    delta = np.arcsin(0.39795*np.cos(delta0))
# višina sonca ob določenem dnevu in uri 3.17
    alfa0 = np.sin(delta)*np.sin(gsir) + np.cos(delta)*np.cos(omega)*np.cos(gsir)
    alfa = np.arcsin(alfa0)
# odmik sonca od smeri 'jug' 3.19
    azimut0 = np.sin(delta)*np.cos(gsir) - np.cos(delta)*np.cos(omega)*np.sin(gsir)
    azimut = np.arccos(azimut0/np.cos(alfa))
    if np.sin(omega)>0:
        azimut = 2*np.pi - azimut 
# kosinus 'theta' vpadlega žarka na ploskev (4.1)
    kosinus0 = np.sin(alfa)*np.cos(nagib)+np.cos(alfa)*np.sin(nagib)*np.cos(zasuk-azimut)
# popravek ko je sonce pod obzorjem    
    obzorje = (kosinus0 <= 0) or (alfa<=0)
    if obzorje:
        kosinus0 = 1e-3
        
    return kosinus0    

#=============================================================================
# demo podatki za kontrolo - vse kar potrebujemo

nagib = np.deg2rad(90)              # navpična plošča
zasuk = np.deg2rad(180)             # obrnjeno na jug
sirina = (46 + 29/60)               # geografska širina SG
dolzina = -(15+7/60)                # geografska dolžina SG

for i in range(240,264):
    kot = kosinus(nagib, zasuk, i, sirina, dolzina)
    print(i-240, kot)
