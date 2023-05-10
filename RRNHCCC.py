import numpy as np
import sympy as sp
from numpy import *
from sympy import *
from collections import Counter
from sympy.parsing.sympy_parser import parse_expr
import string
import re

def es_numero_real(cadena):
    try:
        numero = float(cadena)
        return True
    except ValueError:
        return False

def hallarRaices(coeficientes):
  # aquí se voltean los coeficientes( el primero queda positiva y el resto queda negativo)
  coeficientes = voltear(coeficientes)
  n = len(coeficientes) - 1
  ecuacion = ""
#----------------------------------------------------------------- codigo d chat gpt
  for i, coeficiente in enumerate(coeficientes):
      if coeficiente != 0:
          ecuacion += f"{coeficiente}r^{n-i}"
          if i != n:
              ecuacion += " + "
  raices = np.roots(coeficientes)
  multiplicidad = Counter(np.round(r, 5) for r in raices)

  raic = []
  multiplid = []
  for raiz, mult in multiplicidad.items():
    raic.append(raiz)
    multiplid.append(mult)
#---------------------------------------------------------------------
  return raic, multiplid #devuelve dos listas

#voltea la lista para que los valores desde f(n-1) estén con su signo contrario y así poder hacer la ecuacion caracteristica
def voltear(lista):
    for i in range(1,len(lista)):
      lista[i]= -1*lista[i]
    return lista

def funcionHomogenea(coeficientes):
  n = sp.Symbol("n")
  raices, multiplicidad =  hallarRaices(coeficientes)
  fh = []
  for j in range (len(raices)):
    for i in range(0, multiplicidad[j]):  
      fh.append((n**(i))*raices[j]**n ) #cada posición del vector es un b_i 
  return fh #solucion  de la homogenea asociada

def RRLHCCC(coeficientes, casos_base):
  n = symbols("n")
  fn= funcionHomogenea(coeficientes)# esta es la sum(b*r**n)
  #crear el sistema de ecuaciones
  ecuaciones = []# listas de listas(Matriz)
  for i in range (len(casos_base)):
    aux =[]
    [aux.append(float(b.subs(n,i).evalf())) for b in fn]
    ecuaciones.append(aux)
  
  # se resuvleve el sistema de ecuaciones, volver esto una función
  A = np.array(ecuaciones)
  B = np.array(casos_base)
  x = np.linalg.solve(A,B)# lista con los valores de las incognitas b_i
  
  #funcion final 
  fN =  sum([x[i] * fn[i] for i in range(len(coeficientes)-1)])
  #se multiplican las incognitas por lo que ya había en el vector fn[i]
  print(f"f(n)= {fN}")
  return fN # HAY QUE SIMPLIFICARLO

def funcionParticular(coeficientes, pt, R):
  #definir las variable ssimbolcias, solo permite hasta un polinomio de grado 5
  A= sp.Symbol("A")
  B= sp.Symbol("B")
  C= sp.Symbol("C")
  D= sp.Symbol("D")
  E = sp.Symbol("E")
  F = sp.Symbol("F")
  a = [A,B,C,D,E,F]
  n = sp.Symbol('n')
 # la funcion debe estar despejada y el primer coeficeinte debe ser 1
  homogenea =[]
  homogenea [:]= coeficientes [1:]
  # Pedimos al usuario que ingrese un polinomio
  #pt = (input("Ingresar g(n) de la forma Pt(n)R**n, \n Ingrese Pt(n): ")) 
  #R = (int(input("Ingrese la R del R**n: ")))# es una constante la entrada entonces que entre como # si aqui ponto un float no corre no sé pq
  coeGen =[]
  # hallar el grado del polinimio ingresado
  if(pt.count("n")==0):
    grado = 0
    pt = sympify(pt)
  else:
    grado = (degree(Poly(pt), gen=n))
  generales =0
  for i in range(grado + 1):
    generales  = generales+((a[i] * n ** (grado - i))*(R**n)) # hacer el polinomio general
    coeGen.append(a[i]) # guardar en una lista las variables simbolicas a utilizar

  coeGen[:] = [x for i, x in enumerate(coeGen) if i == coeGen.index(x)]  # asegurarse que los elementos no estén repetidos       
  # reemplazar fp en f(n)
  f =0
  for i in range(1,len(homogenea)+1):
    f=f+(homogenea[i-1]*generales.subs(n,n-i))
  f = simplify(f+ sympify(pt)) # simplificar la expresion 
  coeficientes = (f.as_poly()).coeffs(); # coeficiente de la f(n) reemplazada fp
  matrix = ([coeGen[i]-coeficientes[i] for i in range(len(coeGen))]) #restar fn = fp para hallar los coeficientes de las constantes
  soluciones = []
  #resolver sistema de ecuaciones
  soluciones  = list(linsolve(matrix, tuple(coeGen)))
  # reemplazar los valores con 
  for i in range( len(soluciones[0])):
    f = f.subs([(coeGen[i],soluciones[0][i])])
  return f


def RRLNOHCCC(coeficientes,casos_base,pt,R):
  n = symbols("n")
  fp = funcionParticular(coeficientes,pt,R)
  fn= funcionHomogenea(coeficientes)# esta es la sum(b*r**n)
  fn.append(fp)
  #crear el sistema de ecuaciones
  ecuaciones = []# listas de listas(Matriz)
  for i in range (len(casos_base)):
    aux =[]
    [aux.append(float(b.subs(n,i).evalf())) for b in fn]
    ecuaciones.append(aux)
  
  # se resuvleve el sistema de ecuaciones
  #el ultimo valor de ecuaciones restarlo con cb ya que e suna constante 
  cb=[casos_base[j]-ecuaciones[j][-1] for j in range(len(casos_base))]

  # eliminar los dos ultimos valores de ecuaciones en cada una de las listas ya que osn constantes y se restaron antes a cb
  for i in range(len(ecuaciones)):
    ecuaciones[i].pop(-1)
  ec = np.array(ecuaciones)
  cb = np.array(cb)
  x = np.linalg.solve(ec,cb)# lista con los valores de las incognitas b_i
  
  #funcion final 
  fN =  sum([x[i] * fn[i] for i in range(len(coeficientes)-1)])
  #se multiplican las incognitas por lo que ya había en el vector fn[i]
  fN = fN+fp
  print(f"f(n)= {fN}")

  return fN #display(Math(sp.latex("funcion no recurrente está dada por  f(n)= ")+ sp.latex(fN)))# HAY QUE SIMPLIFICARLO

def RRNOHCCCK1 (coeficientes,casos_base,pt,R):
  n = symbols("n")
  i = symbols("i")
  #gn = pt+"("+str(R)+")"+"**n" # reescrieiendo el pt+r
  gn = str(f"{pt}+({R})**n")
  #gn = input("ingrese le g(n) ->")
  gn = sympify(gn)

 
  #aplicar formula dada en clase 
  c = coeficientes[1]# coeficientes de f(n-1)
  sumatoria = sp.Sum(c**i*gn.subs(n,n-i).evalf(), (i,0,n-1)).doit() 
  f = c**n*casos_base[0]+sumatoria
  #print(f"f(n)= {f}")
  return (f"f(n)= {f}")

  #---------------------INICIO----------------

  #---------------------INICIO, CODIGO PRINCIPAL---------------------------------------------
def mainRRNHCCC(grado,coeficientes,casos_base,opcion,pt,R):
  '''
  coeficientes = []

  #coeficientes = [1,4,-4] #para probar para jacobstal
  #grado =2 #int(input("ingrese el grado de la funcion de recurrencia -> ")  
    
  grado = int(input("Ingresa el grado de la relacion de recurrencia -> "))
  for i in range(grado+1):
    #pass
    coeficientes.append(int(input(f"agregre el coeficiente de f(n {-i} ) -> ")))
  print(coeficientes)

  casos_base = []
  for i in range(grado):
    #pass
    casos_base.append(int(input(f"agregre el casi base f({i}) -> ")))
    
  #casos_base = [1,3]
  print(casos_base)
  
  opcion = int(input("es la relacion de recurrencia homogenea? 1.Sí 0.No ->")) #aquí hay que hacer botones
  #opcion = 0
  '''
  if ( opcion  == 1):
    return RRLHCCC(coeficientes, casos_base) #es homogenea nada mas entonces resolver RRLHCCC
  elif(grado==1):
    return RRNOHCCCK1 (coeficientes,casos_base,pt,R)
    #es no homogenea de grado = 1 hay que hacer c^nf(0)sumatoria de i=0 hasta n-1 c^2g(n-i)
    
  else:
    return RRLNOHCCC(coeficientes,casos_base, pt,R)
    #resolver el RRLNOHCCC


if __name__ == "__main__":
  
  print(mainRRNHCCC())
