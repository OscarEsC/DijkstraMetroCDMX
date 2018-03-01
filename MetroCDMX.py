import random
try:
	from tkinter import * #Python 3
	from tkinter import messagebox
except:
	from Tkinter import * #Python 2.7
	import tkMessageBox as messagebox

class Estacion:
	def __init__(self,  i,  l):
		self.id = i 
		self.visitado = False
		self.nivel = -1 #raiz
		self.vecinos = []
		self.costo = float("inf") 
		self.antecesor = -1

		if len(l)>1:
			self.transborde = True
		else:
			self.transborde = False
		self.linea = l

	def agregarVecino(self,  v):
		if v[0] not in self.vecinos: 
			self.vecinos.append(v)	

class RedMetro(object):
	def __init__(self):
		self.estaciones = {}
	
	def agregarEstacion(self,  v,  l):
		if v not in self.estaciones:
			vert = Estacion(v,  l) #instancia de clase vertice y la asigna a vert
			self.estaciones[v] = vert #la llave es v
	
	def agregarArista(self,  a,  b,  p):
		if a not in self.estaciones:
			messagebox.showwarning("Estacion no valida", "La estacion "+a+" no existe")
		elif b not in self.estaciones:
			messagebox.showwarning("Estacion no valida", "La estacion "+b+" no existe")
		else:
			self.estaciones[a].agregarVecino([b, p]) 
			self.estaciones[b].agregarVecino([a, p])

	def leerRedMetro(self, rutaE,  rutaA):
		try:
			e = open(rutaE,'r')
			a = open(rutaA, 'r')
			l = e.readlines()			#lista de lineas,  cada linea es una estacion

			for estacion in l:
				if estacion != "\n":
					aux = estacion.split('|')
					aux[1] = aux[1].replace("\n", '')
					
					stationLines = aux[1][1:len(aux[1])-1].split(",")
					self.agregarEstacion(aux[0], stationLines)

			l = a.readlines()
			for aristas in l:
				if aristas != "\n":
					aux = aristas.replace('\n', '')
					aux = aux.split('|')
					self.agregarArista(aux[0], aux[1], float(aux[2]))
			e.close()
			a.close()

		except IOError:
			messagebox.showerror("File error", "No se encontro el archivo")

	def resetEstaciones(self):
		for x in self.canv.find_withtag("black"):
			tags = self.canv.gettags(x)
			self.canv.itemconfig(x, fill=tags[0])

		self.canv.dtag("black", "black")

		for v in self.estaciones:
			self.estaciones[v].visitado = False
			self.estaciones[v].nivel = -1
			self.estaciones[v].antecesor = -1
			self.estaciones[v].costo = float("inf")

	def agregarAdy(self, eroot, estv): #recibe la estacion a la que se le cambian los vecinos y los nuevos vecinos
		if eroot not in self.estaciones:
			messagebox.showwarning("Estacion no valida", "La estacion "+eroot+" no existe")
		elif estv[0] not in self.estaciones:
			messagebox.showwarning("Estacion no valida", "La estacion "+estv[0]+" no existe")
		else:
			val=False
			for x in self.estaciones[eroot].vecinos:
				if x[0] == estv[0]:
					val = True
			if val==True:
				messagebox.showwarning("Estacion no valida", "La estacion "+estv[0]+" ya esta conectada con"+eroot[0])
			else:
				self.agregarArista(eroot,estv[0],int(estv[1]))
				t1 = self.canv.find_withtag(eroot)
				t2 = self.canv.find_withtag(estv[0])
				color = 0
				for tag in t1:
					if self.canv.type(tag) == "oval":
						c_root= self.canv.coords(tag) #Obtenemos las coordenadas de la estacion raiz
						break
				for tag1 in t2:
					if self.canv.type(tag1) == "oval":
						c_vec= self.canv.coords(tag1) #obtenemos coordenas de la estacion vecina
						break	
				for tag2 in t1:
					if self.canv.type(tag2) == "line":
						color = self.canv.gettags(tag2)
						break
				if color == 0:
					for tag2 in t2:
						if self.canv.type(tag2) == "line":
							color = self.canv.gettags(tag2)
							break
					if color == 0:
						color = ["pink"]
				
				self.canv.create_line(c_root[0],c_root[1],c_vec[0],c_vec[1],width=7, fill= color[0],capstyle=ROUND, tags=tuple([color[0],eroot,estv[0]]))
				self.canv.dtag(self.canv.create_oval(self.canv.coords(tag),outline='white',fill='white',tag=(self.canv.gettags(tag)[0],'')),'')
				self.canv.dtag(self.canv.create_oval(self.canv.coords(tag1),outline='white',fill='white',tag=(self.canv.gettags(tag1)[0],'')),'')

	def eliminarAdy(self, eroot, estv):##recibe las estaciones entre las que se le elimina arista
		if eroot in self.estaciones and estv in self.estaciones:
			prueba = False
			for ve in self.estaciones[eroot].vecinos:
				if ve[0] == estv:
					prueba = True
					self.estaciones[eroot].vecinos.remove(ve)
					break
				
			if prueba==True: # si estan directamente conectadas
				for er in self.estaciones[estv].vecinos:
					if er[0]== eroot:
						self.estaciones[estv].vecinos.remove(er)
						break

				for tag in self.canv.find_withtag(eroot):
					if self.canv.type(tag) == "line":
						aris = self.canv.gettags(tag)
						if eroot in aris and estv in aris:
							self.canv.delete(tag) #eliminamos el que tiene como tag aris
							break
			else:
				messagebox.showwarning("Estacion no valida", "Estas estaciones no estan directamente conectadas")
		else:
			messagebox.showwarning("Estacion no valida", "Ingresaste una estacion que no existe o la ingresaste incorrectamente.")

	def agregar(self,id,vecin):
		if vecin[1] == '':
			ltag = self.canv.gettags(vecin[0][0])
			for x in self.canv.find_withtag(vecin[0][0]):
				if self.canv.type(x) == "oval":
					coordX = self.canv.coords(x)
					break
			self.agregarEstacion(id,self.estaciones[vecin[0][0]].linea[0]) #linea asociada a id
			self.agregarArista(id,vecin[0][0],int(vecin[0][1])) #le mando la nueva estacion, su vecino y el peso entre estas
			a=random.randrange(-40,40,10)
			b=random.randrange(-40,40,10)
			self.canv.create_line(coordX[0],coordX[1],coordX[0]+a,coordX[1]+b, width=7, fill=ltag[0], capstyle=ROUND, tags=tuple([ltag[0],vecin[0][0],id]))

			self.canv.dtag(self.canv.create_oval(coordX[0]+a,coordX[1]+b,coordX[0]+a+4,coordX[1]+b+4, outline='white',  fill='white', tag = (id,'')),'')
			self.canv.dtag(self.canv.create_text(coordX[0]+a,coordX[1]+b, text=id, font=("Arial",  8),width=80, fill="dark gray", activefill="black", tag=(id,'')),'')
			self.canv.dtag(self.canv.create_oval(coordX,outline = 'white', fill='white', tag=(vecin[0][0],'')),'')
			self.canv.delete(x)

		else:
			for x in self.canv.find_withtag(vecin[0][0]):
					if self.canv.type(x) == "oval":
						coordX = self.canv.coords(x)
						break
			for y in self.canv.find_withtag(vecin[1][0]):
				if self.canv.type(y) == "oval":
					coordY = self.canv.coords(y)
					break
			ambas = 0
			for i in self.canv.find_withtag(vecin[0][0]):
				if i in self.canv.find_withtag(vecin[1][0]): #el valor de la arista que conecta a est_ant con est_post
					ambas = i
					break;
			
			if (ambas != 0): #probamos si estas directamente conectadas, por si la nueva estacion estara entre dos estaciones contiguas
				ltag = self.canv.gettags(ambas) #obtenemos el tag con est_ant,est_post,color
				self.agregarEstacion(id,self.estaciones[ltag[1]].linea[0]) #linea asociada a id
				self.agregarArista(id,vecin[0][0],int(vecin[0][1])) #le mando la nueva estacion , una vieja y el peso entre estas
				self.agregarArista(id,vecin[1][0],int(vecin[1][1]))
				self.eliminarAdy(vecin[0][0],vecin[1][0])
				
				self.canv.create_line(coordX[0],coordX[1],(coordX[0]+coordY[0])//2,(coordX[1]+coordY[1])//2, width=7, fill=ltag[0], capstyle=ROUND, tags=tuple([ltag[0],vecin[0][0],id]))
				self.canv.create_line((coordX[0]+coordY[0])//2,(coordX[1]+coordY[1])//2,coordY[0],coordY[1], width=7, fill=ltag[0], capstyle=ROUND, tags=tuple([ltag[0],id,vecin[1][0]]))
			else:
				t1 = self.canv.gettags(vecin[0][0])
				t2 = self.canv.gettags(vecin[1][0])
				
				self.agregarEstacion(id,[self.estaciones[vecin[0][0]].linea[0],self.estaciones[vecin[1][0]].linea[0]]) #lineas a las que pertenece id
				self.agregarArista(id,vecin[0][0],int(vecin[0][1])) #vecino y peso
				self.agregarArista(id,vecin[1][0],int(vecin[1][1]))
				
				if len(t1) == 1 and len(t2) ==3: #si la primer estacion es ovalo a ambas lineas les pone el color de la segunda estacion
					self.canv.create_line(coordX[2],coordX[3],(coordY[2]+coordX[2])//2,(coordX[3]+coordY[3])//2, width=7, fill=t2[0], capstyle=ROUND, tags=tuple([t1[0],vecin[0][0],id]))
					self.canv.create_line((coordY[2]+coordX[2])//2,(coordX[3]+coordY[3])//2,coordY[2],coordY[3], width=7, fill=t2[0], capstyle=ROUND, tags=tuple([t2[0],id,vecin[1][0]]))	

				elif len(vecin[0][0]) == 3 and len(t2) == 1:#si la segunda es ovalo, a las lineas les pone el color de la primera estacion
					self.canv.create_line(coordX[2],coordX[3],(coordY[2]+coordX[2])//2,(coordX[3]+coordY[3])//2, width=7, fill=t1[0], capstyle=ROUND, tags=tuple([t1[0],vecin[0][0],id]))
					self.canv.create_line((coordY[2]+coordX[2])//2,(coordX[3]+coordY[3])//2,coordY[2],coordY[3], width=7, fill=t1[0], capstyle=ROUND, tags=tuple([t2[0],id,vecin[1][0]]))
				
				else:#si ambas son ovalos les pone color dorado
					self.canv.create_line(coordX[2],coordX[3],(coordY[2]+coordX[2])//2,(coordX[3]+coordY[3])//2, width=7, fill="gold2", capstyle=ROUND, tags=tuple([t1[0],vecin[0][0],id]))
					self.canv.create_line((coordY[2]+coordX[2])//2,(coordX[3]+coordY[3])//2,coordY[2],coordY[3], width=7, fill="gold2", capstyle=ROUND, tags=tuple([t2[0],id,vecin[1][0]]))
			self.canv.dtag(self.canv.create_oval((coordX[0]+coordY[0])//2,(coordX[1]+coordY[1])//2,(coordX[0]+coordY[0])//2+4,(coordX[1]+coordY[1])//2+4, outline='white',  fill='white', tag = (id,'')),'')
			self.canv.dtag(self.canv.create_text((coordX[0]+coordY[0])//2,(coordX[1]+coordY[1])//2, text=id, font=("Arial",  8),width=80, fill="dark gray", activefill="black", tag=(id,'')),'')
			self.canv.dtag(self.canv.create_oval(coordX,outline = 'white', fill='white', tag=(vecin[0][0],'')),'')
			self.canv.dtag(self.canv.create_oval(coordY,outline = 'white', fill='white', tag=(vecin[1][0],'')),'')
			self.canv.delete(x)
			self.canv.delete(y)

	def modNombreEstacion(self, estacion, nombre):
		if estacion in self.estaciones:
			self.agregarEstacion(nombre, self.estaciones[estacion].linea)
			for vecino in self.estaciones[estacion].vecinos: #iteramos sobre los vecinos de la estacion
				self.agregarArista(vecino[0],nombre,vecino[1])
			self.eliminar(estacion)

			for tag in self.canv.find_withtag(estacion):
				if self.canv.type(tag) == "text":
					self.canv.dtag(self.canv.create_text(self.canv.coords(tag), text = nombre, font = ("Arial",  8),width=80, fill = "dark grey", activefill = "black", tag = (nombre,'')),'')#Obtenemos las coordenadas del texto
					self.canv.delete(tag)
					break
			self.canv.addtag_withtag(nombre,estacion)
			self.canv.dtag(estacion)

		else:
			messagebox.showwarning("Estacion no valida", "La estacion "+estacion+" no existe")

	def modificarTiempo(self, estacion1, estacion2, nuevoTiempo):
		if estacion1 not in self.estaciones:
			messagebox.showwarning("Estacion no valida", "La estacion "+estacion1+" no existe")
		elif estacion2 not in self.estaciones:
			messagebox.showwarning("Estacion no valida", "La estacion "+estacion2+" no existe")
		elif nuevoTiempo.isdigit() == False:
			messagebox.showwarning("Tiempo invalido", "Se esperaba un numero entero, se obtuvo: "+nuevoTiempo)
		else:
			prueba = False
			for vecino in self.estaciones[estacion1].vecinos:
				if vecino[0] == estacion2:
					prueba = True
					break
			if prueba == True:
				for vec in self.estaciones[estacion2].vecinos:
					if vec[0] == estacion1:
						vec[1] = nuevoTiempo
						vecino[1] = nuevoTiempo
						messagebox.showinfo("Operacion realizada", "Se ha cambiado el tiempo de traslado")
						break
			else:
				messagebox.showwarning("Estaciones no validas", "Las estaciones no estan conectadas")

	def eliminar (self, e):
		for vecino in self.estaciones[e].vecinos:
			for vecDeVec in self.estaciones[vecino[0]].vecinos:
				if vecDeVec[0]==e:
					self.estaciones[vecino[0]].vecinos.remove(vecDeVec)
					break
		del self.estaciones[e]

	def minheap(self,  l,  i):#l contiene el nombre de las estaciones
		if(2*i+1 <= len(l)-1):
			if(float(self.estaciones[l[2*i]].costo) < float(self.estaciones[l[2*i+1]].costo)):
				min = 2*i 
			else:
				min = 2*i+1
				if(self.estaciones[l[i]].costo > self.estaciones[l[min]].costo):
					aux = l[i]
					l[i] = l[min]
					l[min] = aux
					self.minheap(l, min)

		elif(2*i <= len(l)-1):
			if(float(self.estaciones[l[i]].costo) > float(self.estaciones[l[2*i]].costo)):
				aux = l[i]
				l[i] = l[2*i]
				l[2*i] = aux
				self.minheap(l, 2*i)
		return l

	def caminoMasCortoEstaciones(self,  estacion1, estacion2):
		if estacion2 in self.estaciones and estacion1 in self.estaciones:
			self.resetEstaciones()
			cola = [] #lista donde iremos agregando los nodos que van a ser visitados
			cola.append(estacion2) #Agregamos el nodo raiz del BFS

			self.estaciones[estacion2].visitado = True
			self.estaciones[estacion2].nivel = 0 #Le asigamos el nivel 0 ya que es el nodo raiz

			while (len(cola) > 0 and estacion1 not in cola):
				actual = cola[0]
				cola = cola[1:] #Quitamos el elemento actual de la cola porque ya fue visitado

				for estacion in  self.estaciones[actual].vecinos: #Revisamos sus vecinos para ver si no han sido visitados
					if (self.estaciones[estacion[0]].visitado == False): #Estacion es una lista [estacion,  lineas]
						cola.append(estacion[0]) #Agregamos a la lista los estacioninos que no han sido visitados
						self.estaciones[estacion[0]].visitado = True
						self.estaciones[estacion[0]].nivel = self.estaciones[actual].nivel+1 #Su nivel es el del nodo padre(actual) +1

			if (self.estaciones[estacion1].nivel==-1 or self.estaciones[estacion2].nivel==-1): #Si la grafica es disconexa
				messagebox.showerror("No existe camino", "No hay manera de llegar de "+estacion1+" a "+estacion2)
			else:
				camino = [] #Lista que guarda los nodos por los que hay que pasar para llegar al destino
				nivel = self.estaciones[estacion1].nivel #Empezamos en el nivel del nodo inicial
				camino.append(estacion1) #Agreamos el nodo inicial para que se guarde al inicio de la lista

				while nivel != 0: #Mientras no lleguemos al nivel del nodo raiz de la grafica que es el nodo destino
					for x in self.estaciones[estacion1].vecinos: #Verificamos los vecinos del nodo actual
						if self.estaciones[x[0]].nivel == nivel-1: #Si un vecino tiene nievel-1 entonces es nodo padre
							camino.append(x[0]) #Lo agregamos a la lista
							nivel = self.estaciones[x[0]].nivel #Bajamos de nivel al nivel del nodo padre
							estacion1 = x[0] #cambiamos de nodo actual al nodo padre
							break; #rompemos el ciclo para que no siga iterando

				for x in range(0, len(camino), 1):
					i = self.canv.find_withtag(camino[x])
					try:
						j = self.canv.find_withtag(camino[x+1])
					except:
						j = self.canv.find_withtag(camino[x-1])
					for w in i:
						if w in j:
							self.canv.itemconfig(w, fill="black")
							self.canv.addtag_withtag("black", w)
				return camino
		else:
			messagebox.showwarning("Estacion no valida", "La estacion no existe o la ingresaste incorrectamente")
			return None

	def camino(self,  r,  c):
		if(r != -1):
			self.camino(self.estaciones[r].antecesor, c)
			c.append(r)
		return c

	def tomarTransbordo(self, prim, seg):
		cont = 0;
		l1 = self.estaciones[self.estaciones[prim].antecesor].linea #estacion anterior
		l2 = self.estaciones[seg].linea #est siguiente

		for lin in l1:
			if lin in l2:
				cont +=1
		return cont

	def dijkstra(self, a, b):
		if a not in self.estaciones or b not in self.estaciones:	
			messagebox.showwarning("Estacion no valida", "La estacion no existe o la ingresaste incorrectamente")
		else:
			self.resetEstaciones()
			lista = [] #estaciones que se van a evaluar
			self.estaciones[a].costo = 0  #a[0]

			for v in self.estaciones[a].vecinos:  #a[0]
				self.estaciones[v[0]].costo = int(v[1])
				self.estaciones[v[0]].antecesor = a
				lista.append(v[0])

			while(len(lista) > 0):
				minimo = self.minheap(lista, 0) #obtenemos la estacion con el costo minimo
				m = minimo[0] #m es un string
				for vec in self.estaciones[m].vecinos:
					if self.estaciones[m].transborde == False: #La estacion no tiene transbordo

						if self.estaciones[m].costo + int(vec[1]) < self.estaciones[vec[0]].costo:
							self.estaciones[vec[0]].costo = self.estaciones[m].costo + int(vec[1])
							self.estaciones[vec[0]].antecesor = m # m es el nombre de la estacion que le antecede en menor costo

							if self.estaciones[vec[0]].visitado == False:
								lista.append(vec[0])
					else:
						if self.tomarTransbordo(m, vec[0]) == 0: # Si tiene que tomar el transbordo,  la estacion siguiente y anterior no tienen en comun

							if self.estaciones[m].costo + int(vec[1])+5 < self.estaciones[vec[0]].costo:
								self.estaciones[vec[0]].costo = 5+self.estaciones[m].costo + int(vec[1])
								self.estaciones[vec[0]].antecesor = m

								if self.estaciones[vec[0]].visitado == False:
									lista.append(vec[0])
						else: # si tienen estaciones en común no se hace transbordo
							if self.estaciones[m].costo + int(vec[1]) < self.estaciones[vec[0]].costo:
								self.estaciones[vec[0]].costo = self.estaciones[m].costo + int(vec[1])
								self.estaciones[vec[0]].antecesor = m

								if self.estaciones[vec[0]].visitado == False:
									lista.append(vec[0])
				lista.remove(m)
				self.estaciones[m].visitado = True #Para que no se vuelva a agregar a lista
			
			c = []
			if (self.estaciones[b].visitado == True):
				c = self.camino(b, c)
				for x in range(0, len(c), 1):
					i = self.canv.find_withtag(c[x])
					try:
						j = self.canv.find_withtag(c[x+1])
					except:
						j = self.canv.find_withtag(c[x-1])
					for w in i:
						if w in j:
							self.canv.itemconfig(w, fill="black")
							self.canv.addtag_withtag("black", w)
				c.append(self.estaciones[b].costo)
				return c
			else:
				messagebox.showerror("No existe camino", "No hay manera de llegar de "+a+" a "+b)
				return None
	
class RedDelMetro(RedMetro):
	def __init__(self,est,aris,ovl,ln,tx):
		RedMetro.__init__(self)

		self.leerRedMetro(est, aris)

		self.ventana = Tk()
		self.ventana.config(bg = "black")#color del Fondo de la self.ventana
		self.ventana.geometry("%dx%d+%d+%d" % (self.ventana.winfo_screenwidth()-15, self.ventana.winfo_screenheight()-80, -0, 0))#Dimensiones de la ventana
		self.ventana.title("Red del metro de la Ciudad de México") #Con los metodos winfo_screenwidth() y winfo_screenheight() obtenemos el tamaño de la pantalla
		self.ventana.resizable(width = False,  height = False)

		self.canv = Canvas(self.ventana,  width = 20+2*self.ventana.winfo_screenwidth()/3,  height = 150,  bg = 'dark grey',  cursor = "arrow", relief = RIDGE, bd = 4)#Creamos un canvas para dibujar las lineas
		self.crearLineas(ovl,ln,tx)
		self.canv.pack(side = LEFT, fill = Y)

		self.frame = Frame(self.ventana, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7,  height = 150)
		self.frame.pack(side = RIGHT, fill = Y, padx = 5, pady = 5)

		self.frame2 = Frame(self.frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7,  height = 5)
		self.frame2.grid(row = 0, column = 0, columnspan = 3)	

		self.etiqueta = Label(self.frame, text = "Red del metro de la Ciudad de Mexico", bg = "#3399FF", font =("Helvetica", 16))
		self.etiqueta.grid(row = 1, column = 0, columnspan = 3, sticky= W+E)
		self.etiqueta2 = Label(self.frame, text = "Elige alguna de las siguientes opciones", bg = "#3399FF", font =("Georgia", 12), width = 30)
		self.etiqueta2.grid(row = 2, column = 0, columnspan = 3, sticky = W+E)

		self.boton = Button(self.frame, text = "Camino corto estacion", command = self.menuCaminoCorto)#,  anchor=E)
		self.boton.grid(row = 3, column = 0, sticky = W+E)
		self.boton1 = Button(self.frame, text = "Camino menor tiempo", command = self.menuCaminoTiempo)#,  anchor=E)
		self.boton1.grid(row = 3, column = 1, sticky = W+E)
		self.boton2 = Button(self.frame, text = "Eliminar estacion",  command = self.menuEliminarEstaciones)#,  anchor=E)
		self.boton2.grid(row = 3, column = 2,  sticky = W+E)
		self.boton3 = Button(self.frame, text = "Agregar estacion", command = self.menuAgregarE)
		self.boton3.grid(row = 4,column = 0,sticky = W+E)
		self.boton4 = Button(self.frame,text= "Modificar atributos",command = self.menuModAtributos)
		self.boton4.grid(row = 4, column = 1,sticky = W+E)
		self.boton5 = Button(self.frame, text = "Salir", command = self.guardarRed)
		self.boton5.grid(row = 5,column = 1,sticky = W+E)
		self.boton6 = Button(self.frame,text="Cargar otra red",command = self.cargarRedNueva)
		self.boton6.grid(row = 4, column = 2,sticky = W+E)

		self.ventana.mainloop()  

	def menuCaminoCorto(self):
		self.resetEstaciones()
		frameauxiliar = Frame(self.frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7)
		frameauxiliar.grid(row=6,column=0,columnspan=3,sticky=N+S)
		Frame(frameauxiliar,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-10,  height = 5).grid(row = 0, column = 0, columnspan = 3)	
		#estos frames son para que no se encimen los objetos
		Message(frameauxiliar, text = "Estacion de inicio", width = 100, bg = "#3399FF").grid(row = 1, column = 0)
		estacion1 = Entry(frameauxiliar, takefocus = True, width = 40)
		estacion1.grid(row = 1, column = 1, columnspan = 2)

		Message(frameauxiliar, text = "Estacion de destino", width = 120, bg = "#3399FF").grid(row = 2, column = 0)
		estacion2 = Entry(frameauxiliar, takefocus = True, width = 40)
		estacion2.grid(row = 2, column = 1, columnspan = 2)

		Button(frameauxiliar, text = "Buscar camino mas corto en distancia", command = lambda:self.impresionCaminoCorto(estacion1.get().upper(), estacion2.get().upper(),frameauxiliar)).grid(row = 3, column = 1)

	def menuCaminoTiempo(self):
		self.resetEstaciones()
		frameauxiliar = Frame(self.frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7)
		frameauxiliar.grid(row=6,column=0,columnspan=3,sticky=N+S)
		Frame(frameauxiliar,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-10,  height = 5).grid(row = 0, column = 0, columnspan = 3)
		Message(frameauxiliar, text = "Estacion de inicio", width = 100, bg = "#3399FF").grid(row = 1, column = 0)
		estacion1 = Entry(frameauxiliar, takefocus = True, width = 40)
		estacion1.grid(row = 1, column = 1, columnspan = 2)

		Message(frameauxiliar, text = "Estacion de destino", width = 120, bg = "#3399FF").grid(row = 2, column = 0)
		estacion2 = Entry(frameauxiliar, takefocus = True, width = 40)
		estacion2.grid(row = 2, column = 1, columnspan = 2)

		Button(frameauxiliar, text = "Buscar camino mas corto en tiempo", command = lambda:self.impresionCaminoTiempo(estacion1.get().upper(), estacion2.get().upper(),frameauxiliar)).grid(row = 3, column = 1)

	def menuEliminarEstaciones(self):
		self.resetEstaciones()
		frameauxiliar = Frame(self.frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7)
		frameauxiliar.grid(row=6,column=0,columnspan=3,sticky=N+S)
		Frame(frameauxiliar,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-10,  height = 5).grid(row = 0, column = 0, columnspan = 3)
		Message(frameauxiliar,  text = "Estacion a eliminar:",  width = 100,  bg = "#3399FF").grid(row = 1,  column = 0)
		estacion1 = Entry(frameauxiliar,  takefocus = True,  width = 40)
		estacion1.grid(row = 1,  column = 1,  columnspan = 2)

		Button(frameauxiliar,  text = "Eliminar",  command = lambda:self.eliminarE(estacion1.get().upper() )).grid(row = 2,  column = 1)

	def eliminarE(self, e):
		if e in self.estaciones:
			self.eliminar(e)
			self.canv.delete(e)
		else:
			messagebox.showwarning("Estacion no valida", "La estacion no existe o la ingresaste incorrectamente")

	def menuAgregarE(self):
		self.resetEstaciones()
		frameauxiliar = Frame(self.frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7)
		frameauxiliar.grid(row=6,column=0,columnspan=3,sticky=N+S)
		Frame(frameauxiliar,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-10,  height = 5).grid(row = 0, column = 0, columnspan = 3)
		Message(frameauxiliar,text = "Nombre de la nueva estacion", width = 100,bg = "#3399FF").grid(row = 1,column = 0)
		n_esta = Entry(frameauxiliar, takefocus = True,width = 40)
		n_esta.grid(row = 1,column = 1,columnspan = 2)

		Message(frameauxiliar,text = "Nombre de la estacion vecina 1", width = 100,bg = "#3399FF").grid(row = 2,column = 0)
		esta_vec1 = Entry(frameauxiliar, takefocus = True,width = 40)
		esta_vec1.grid(row = 2,column = 1,columnspan = 2)
		Message(frameauxiliar,text = "Tiempo de viaje", width=100,bg = "#3399FF").grid(row=3,column=0)
		viaje1 = Entry(frameauxiliar, takefocus = True,width = 40)
		viaje1.grid(row = 3,column = 1,columnspan = 2)

		Message(frameauxiliar,text = "Nombre de la estacion vecina 2", width=100,bg = "#3399FF").grid(row=4,column=0)
		esta_vec2 = Entry(frameauxiliar, takefocus = True,width = 40)
		esta_vec2.grid(row = 4,column = 1,columnspan = 2)
		Message(frameauxiliar,text = "Tiempo de viaje", width = 100,bg = "#3399FF").grid(row = 5,column = 0)
		viaje2 = Entry(frameauxiliar, takefocus = True,width = 40)
		viaje2.grid(row = 5,column = 1,columnspan = 2)
		Message(frameauxiliar,text = "*Si solo tiene una adyacencia deja los demas espacios en blanco", width=200,bg = "#3399FF").grid(row=6,column=1,sticky=W+S)
		Button(frameauxiliar,text = "Agregar",command = lambda: self.agregarE([n_esta.get().upper(),[esta_vec1.get().upper(),viaje1.get()],[esta_vec2.get().upper(),viaje2.get()]])).grid(row = 7,column=1)

	def agregarE(self,vec_a):
		if (vec_a[1][1].isdigit() == True and vec_a[1][0] in self.estaciones):
			if vec_a[2][0] == '':
				if vec_a[0] not in self.estaciones:
					self.agregar(vec_a[0], [vec_a[1],''])
				else:
					messagebox.showwarning("Estacion no valida", "La estacion ya existe en la Red")

			elif vec_a[2][1].isdigit() == True and vec_a[2][0] in self.estaciones:
				if vec_a[0] not in self.estaciones:
					self.agregar(vec_a[0], [vec_a[1],vec_a[2]])
				else:
					messagebox.showwarning("Estacion no valida", "La estacion ya existe en la Red")
		else:
			messagebox.showwarning("Estacion no valida", "Las estaciones vecinas no existen o ingresaste incorrectamente algun dato")

	def menuModAtributos(self):
		frameauxiliar = Frame(self.frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7)
		frameauxiliar.grid(row=6,column=0,columnspan=3,sticky=N+S)
		Frame(frameauxiliar,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-10,  height = 5).grid(row = 0, column = 0, columnspan = 2)
		
		Button(frameauxiliar,text = "Agregar adyacencia",command = self.menuagregarAdy).grid(row = 1, column = 0, sticky = W+E)
		Button(frameauxiliar,text = "Eliminar adyacencia",command = self.menuEliminarAdy).grid(row = 1, column = 1, sticky = W+E)
		Button(frameauxiliar,text = "Cambiar nombre",command = self.menuCambiarNombre).grid(row = 2, column = 0,sticky = W+E)
		Button(frameauxiliar,text = "Cambiar tiempo de traslado",command = self.menuCambiarTiempo).grid(row = 2,column = 1,sticky = W+E)

	def menuCambiarNombre(self):
		frameauxiliar = Frame(self.frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7)
		frameauxiliar.grid(row=6,column=0,columnspan=3,sticky=N+S)
		Frame(frameauxiliar,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-10,  height = 5).grid(row = 0, column = 0, columnspan = 3)
		
		Message(frameauxiliar,  text = "Estacion a modificar:",  width = 100,  bg = "#3399FF").grid(row = 1,  column = 0)
		estacion1 = Entry(frameauxiliar,  takefocus = True,  width = 40)
		estacion1.grid(row = 1,  column = 1,  columnspan = 2)
		
		Message(frameauxiliar,  text = "Nuevo nombre:",  width = 100,  bg = "#3399FF").grid(row = 2,  column = 0)
		estacion2 = Entry(frameauxiliar,  takefocus = True,  width = 40)
		estacion2.grid(row = 2,  column = 1,  columnspan = 2)
		
		Button(frameauxiliar,text = "Modificar nombre",command = lambda:self.modNombreEstacion(estacion1.get().upper(),estacion2.get().upper())).grid(row = 3, column = 1,sticky = W+E)

	def menuCambiarTiempo(self):
		frameauxiliar = Frame(self.frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7)
		frameauxiliar.grid(row=6,column=0,columnspan=3,sticky=N+S)
		Frame(frameauxiliar,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-10,  height = 5).grid(row = 0, column = 0, columnspan = 3)

		Message(frameauxiliar,  text = "Estacion 1:",  width = 100,  bg = "#3399FF").grid(row = 1,  column = 0)
		estacion1 = Entry(frameauxiliar,  takefocus = True,  width = 40)
		estacion1.grid(row = 1,  column = 1,  columnspan = 2)

		Message(frameauxiliar,  text = "Estacion 2:",  width = 100,  bg = "#3399FF").grid(row = 2,  column = 0)
		estacion2 = Entry(frameauxiliar,  takefocus = True,  width = 40)
		estacion2.grid(row = 2,  column = 1,  columnspan = 2)

		Message(frameauxiliar,  text = "Nuevo tiempo de traslado:",  width = 100,  bg = "#3399FF").grid(row = 3,  column = 0)
		tiempo = Entry(frameauxiliar,  takefocus = True,  width = 40)
		tiempo.grid(row = 3,  column = 1,  columnspan = 2)

		Button(frameauxiliar,text = "Modificar tiempo de traslado",command = lambda:self.modificarTiempo(estacion1.get().upper(),estacion2.get().upper(),tiempo.get())).grid(row = 4, column = 1,sticky = W+E)

	def menuagregarAdy(self):
		frameauxiliar = Frame(self.frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7)
		frameauxiliar.grid(row=6,column=0,columnspan=3,sticky=N+S)
		Frame(frameauxiliar,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-10,  height = 5).grid(row = 0, column = 0, columnspan = 3)

		Message(frameauxiliar,text="Nombre de la estacion",width=100,bg= "#3399FF").grid(row=1, column=0)
		est = Entry(frameauxiliar, takefocus = True,width = 40)
		est.grid(row = 1,column = 1,columnspan = 2)
		Message(frameauxiliar,text = "Nombre de la nueva estacion vecina ", width = 100,bg = "#3399FF").grid(row = 2,column = 0)
		esta_vec = Entry(frameauxiliar, takefocus = True,width = 40)
		esta_vec.grid(row = 2,column = 1,columnspan = 2)
		Message(frameauxiliar,text = "Tiempo de viaje", width=100,bg = "#3399FF").grid(row=3,column=0)
		viaje = Entry(frameauxiliar, takefocus = True,width = 40)
		viaje.grid(row = 3,column = 1,columnspan = 2)
		Button(frameauxiliar,text = "Aceptar",command = lambda: self.agregarAdy(est.get().upper(),[esta_vec.get().upper(),viaje.get()])).grid(row = 4,column=1)

	def menuEliminarAdy(self):
		frameauxiliar = Frame(self.frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7)
		frameauxiliar.grid(row=6,column=0,columnspan=3,sticky=N+S)
		Frame(frameauxiliar,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-10,  height = 5).grid(row = 0, column = 0, columnspan = 3)

		Message(frameauxiliar,text="Nombre de la estacion",width=100,bg= "#3399FF").grid(row=1, column=0)
		est = Entry(frameauxiliar, takefocus = True,width = 40)
		est.grid(row = 1,column = 1,columnspan = 2)
		Message(frameauxiliar,text = "Nombre de la estacion vecina a borrar", width = 100,bg = "#3399FF").grid(row = 2,column = 0)
		esta_vec = Entry(frameauxiliar, takefocus = True,width = 40)
		esta_vec.grid(row = 2,column = 1,columnspan = 2)
		Button(frameauxiliar,text = "Aceptar",command = lambda: self.eliminarAdy(est.get().upper(),esta_vec.get().upper())).grid(row = 3,column=1)

	def impresionCaminoCorto(self, est1, est2,frame):
		frameaux = Frame(frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7-25)
		frameaux.grid(row=4,column=0,columnspan=3,sticky=N+S)
		Frame(frameaux,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-25,  height = 5).grid(row = 0, column = 0, columnspan = 3)
		c = self.caminoMasCortoEstaciones(est1, est2)

		scrollbar = Scrollbar(frameaux)
		scrollbar.grid(row = 1, column = 0,sticky=N+S)
		if c != None:
			e = Listbox(frameaux, yscrollcommand=scrollbar.set)
			e.insert(END, "Tienes que ir por:")
			for est in c:
				e.insert(END, est)
		else:
			e = Listbox(frameaux, yscrollcommand=scrollbar.set)
			e.insert(END,  "No hay camino")
			#e.insert(END, "camino")
		e.grid(row = 1, column = 0,columnspan=3)
		scrollbar.config(command=e.yview)

	def impresionCaminoTiempo(self, est1,  est2,frame):
		frameaux = Frame(frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7-25)
		frameaux.grid(row=4,column=0,columnspan=3,sticky=N+S)
		Frame(frameaux,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-25,  height = 5).grid(row = 0, column = 0, columnspan = 3)
		c = self.dijkstra(est1, est2)

		scrollbar = Scrollbar(frameaux)
		scrollbar.grid(row = 1, column = 0,sticky=N+S)
		if c != None:
			e = Listbox(frameaux, yscrollcommand=scrollbar.set)

			costo = c[len(c)-1]
			c = c[:len(c)-1]
			e.insert(END, "Tienes que ir por:")

			for est in c:
				e.insert(END, est)
			e.insert(END, "\nTiempo estimado:")
			e.insert(END, str(costo)+" minutos")
		else:
			e = Listbox(frameaux, yscrollcommand=scrollbar.set)
			e.insert(END,  "No hay camino")
			#e.insert(END, "camino")
		e.grid(row = 1, column = 0,columnspan=3)
		scrollbar.config(command=e.yview)

	def cargarRedNueva(self):

		frameauxiliar = Frame(self.frame, bg = '#3399FF', bd = 4,  width = 2*self.ventana.winfo_screenwidth()/7)
		frameauxiliar.grid(row=6,column=0,columnspan=3,sticky=N+S)
		Frame(frameauxiliar,bg = '#3399FF',  width = 2*self.ventana.winfo_screenwidth()/7-10,  height = 5).grid(row = 0, column = 0, columnspan = 3)

		Message(frameauxiliar,text="Nombre del archivo que contiene los ovalos:",width=100,bg= "#3399FF").grid(row=1, column=0)
		ovl = Entry(frameauxiliar, takefocus = True,width = 40)
		ovl.grid(row = 1,column = 1,columnspan = 2)
		Message(frameauxiliar,text = "Nombre del archivo que contiene las lineas de aristas:", width = 100,bg = "#3399FF").grid(row = 2,column = 0)
		ln = Entry(frameauxiliar, takefocus = True,width = 40)
		ln.grid(row = 2,column = 1,columnspan = 2)
		Message(frameauxiliar,text="Nombre del archivo que contiene los textos:",width = 100,bg = "#3399FF").grid(row = 3, column = 0)
		tex = Entry(frameauxiliar, takefocus = True,width = 40)
		tex.grid(row = 3, column = 1, columnspan = 2)
		Message(frameauxiliar,text="Nombre del archivo que contiene las estaciones:",width = 100,bg = "#3399FF").grid(row = 4, column = 0)
		esta = Entry(frameauxiliar, takefocus = True,width = 40)
		esta.grid(row = 4, column = 1, columnspan = 2)
		Message(frameauxiliar,text="Nombre del archivo que contiene las aristas:",width = 100,bg = "#3399FF").grid(row = 5, column = 0)
		arist = Entry(frameauxiliar, takefocus = True,width = 40)
		arist.grid(row = 5, column = 1, columnspan = 2)
		Button(frameauxiliar,text = "Aceptar",command = lambda: self.cargarR(ovl.get(),ln.get(),tex.get(),esta.get(),arist.get())).grid(row = 6,column=1)

	def cargarR(self,ovl,ln,text,esta,arist):
		red2 = RedDelMetro(esta,arist,ovl,ln,text)

	def crearLineas(self,ovl,ln,tex):
		try:
			lineas = open(ln, 'r')
			ovalos = open(ovl,'r')
			textos = open(tex,'r')
			l = lineas.readlines()
			o = ovalos.readlines()
			t = textos.readlines()

			for reng in l:
				if reng != "\n":
					aux = reng.split('|')
					aux2 = aux[1].split(',')
					aux2[2]=aux2[2].replace('\n','')
					self.canv.create_line(aux[0].split(','), width = 7, fill = aux2[0], capstyle = ROUND, tags = tuple(aux2))
			for reng in o:
				if reng != "\n":
					aux = reng.split('|')
					self.canv.dtag(self.canv.create_oval(aux[0].split(','),  outline = 'white',  fill = 'white', tag=tuple(aux[1].split('\n'))),'')
			for reng in t:
				if reng != "\n":
					aux = reng.split('|')
					self.canv.dtag(self.canv.create_text(aux[0].split(','), text = aux[1], font = ("Arial",  8),width=80 , fill = "dark grey", activefill = "black", tag = aux[1].split('\n')),'')

			self.canv.pack(side = LEFT, fill = Y)
			lineas.close()
			ovalos.close()
			textos.close()

		except IOError:
			messagebox.showerror("Archivo no encontrado", "No se encontro archivo de configuracion de la red")
			self.ventana.destroy()

	def guardarRed(self):
		if messagebox.askyesno("Guardar red","Quieres guardar la configuracion?"):
			try:
				est = open("est1.txt",'w+')
				arist = open("aris1.txt", 'w+')
				lin = open("lineas2.txt",'w+')
				oval = open("ovalos2.txt",'w+')
				text = open("textos2.txt",'w+')
				self.resetEstaciones()

				for estacion in self.estaciones:
					est.write(estacion+'|[')
					for x in self.estaciones[estacion].linea:
						est.write(x)
						if x != self.estaciones[estacion].linea[len(self.estaciones[estacion].linea)-1]:
							est.write(',')
					est.write(']\n')
					for vecino in self.estaciones[estacion].vecinos:
						if self.estaciones[vecino[0]].visitado == False:
							arist.write(estacion+'|'+vecino[0]+'|'+str(int(vecino[1]))+'\n')
					self.estaciones[estacion].visitado = True

				for elemento in self.canv.find_all():
					tags = list(self.canv.gettags(elemento))
					coord = self.canv.coords(elemento)
					if self.canv.type(elemento) == "line":
						i=0
						for c in coord:
							lin.write(str(int(c)))
							if i<3:
								lin.write(',')
							i+=1
						lin.write('|')
						for t in tags:
							lin.write(t)
							if t != tags[len(tags)-1]:
								lin.write(',')
						lin.write('\n')
					elif self.canv.type(elemento) == "oval":
						i=0
						for c in coord:
							oval.write(str(int(c)))
							if i<3:
								oval.write(',')
							i+=1
						oval.write('|'+tags[0]+'\n')
					elif self.canv.type(elemento) == "text":
						i=0
						for c in coord:
							text.write(str(int(c)))
							if i==0:
								text.write(',')
							i+=1
						text.write('|'+tags[0]+'\n')

				lin.close()
				oval.close()
				text.close()
				arist.close()
				est.close()
				self.ventana.destroy()
			except IOError:
				messagebox.showerror("Archivo no encontrado", "No se encontro archivo de configuracion de la red, no se guardo la configuracion")

		else:
			self.ventana.destroy()

#----------main---------------------------------------------
class main:
	df = RedDelMetro("estaciones.txt","aristas.txt","ovalos.txt","lineas.txt","textos.txt")