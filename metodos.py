import matplotlib.pyplot as plt

def dibujarEstrellas(txt: str):

  with open(txt, 'r') as f:
      x = []
      y = []
      for line in f:
          columnas = line.split()
          x.append(float(columnas[0])) 
          y.append(float(columnas[1])) 

  #graficando
  # Crear el gráfico de puntos
  plt.scatter(x, y, color = '#ADD8E6', s = 10)# S es para el grosor

  # Agregar títulos y etiquetas a los ejes
  plt.title('Gráfico de las estrellas')
  plt.xlabel('Coordenada x')
  plt.ylabel('Coordenada y')

  # Mostrar el gráfico
  
  return plt.savefig('estrellas.png')# guardar el grafico de las estrellas

def start():
  with open("constelaciones\stars.txt", 'r') as f:
        coordenadas_constelaciones = {}
        for line in f:
            nombre = ""
            nombreLista = []
            coordenadas = []
            columnas = line.split()

            if (len(columnas)>=7):# si es 6 es que la vaina esa tiene nombre
              # desde 7 palante meter todo en un str
              for i in range(6,len(columnas)):
                nombre = nombre+columnas[i]# meter todos los nombres en un solo str

              nombreLista =  tuple(nombre.strip().split(';'))# lo cambié por una lista
              coordenadas.append(float(columnas[0]))#x
              coordenadas.append(float(columnas[1])) #y
              coordenadas_constelaciones[(nombreLista)] = coordenadas 
  return coordenadas_constelaciones


def estrellas_constelacion(txt: str):
    
  with open(txt, "r") as f1:
    estrellas = []
    for line in f1:
      aux = []
      columnas = line.strip().split(',')
      for i in columnas:
        aux.append(i)
      estrellas.append(aux)# cada posición es uns lista con dos estrellas que van unidas por una linea 
  return estrellas



                  
#constelaciones = ["Cygnet.txt"]

#MAIN
def main( constelacion = None):
  coordenadas_constelaciones= start()
  if(constelacion):
     constelaciones = [constelacion]
  else:
     constelaciones = ["constelaciones/Boyero.txt","constelaciones/Casiopea.txt", "constelaciones/Cazo.txt",
                  "constelaciones/Cygnet.txt","constelaciones/Geminis.txt","constelaciones/Hydra.txt","constelaciones/OsaMayor.txt","constelaciones/OsaMenor.txt"]
  for c in constelaciones:
    estrellas  = estrellas_constelacion(c)
    for e in estrellas:# estrellas es una lista de listas
      #print("e", e)
      equis = []
      ye = []
      for x, y in coordenadas_constelaciones.items():# buscar las estrellas de las constelaciones en todas las estrellas que hay
        for z in x:# x es una lista de nombre
          if  e[0].replace(" ","") == z:# si coincide entonces meterla informacion en el dictionario 
              equis.append(y[0]) 
              ye.append(y[1])
          if  e[1].replace(" ","") == z:# si coincide entonces meterla informacion en el dictionario 
              equis.append(y[0]) 
              ye.append(y[1])
      plt.plot(equis,ye)

  dibujarEstrellas("constelaciones\stars.txt")
  return plt.savefig('estrellas_constelacion.png')# guardar el grafico de las estrellas



if __name__ == "__main__":
  
  dibujarEstrellas("constelaciones\stars.txt")