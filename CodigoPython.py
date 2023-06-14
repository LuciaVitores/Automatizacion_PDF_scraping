#!/usr/bin/env python
# coding: utf-8

# # Código para la automatización de la extracción de datos. 
# #### Alumna: Lucía Vítores López

# ## ÍNDICE:
# 1. [Importaciones](#1)
# 
# 
# 
# 2. [Desarrollo código](#2)
# 
#     2.1. [Definición de funciones](#2.1.)
#     
#     2.2. [Importación de ficheros Excel](#2.2)
#     
#     2.3. [Definición de algunas variables](#2.3)
#     
#     2.4. [Diagnóstico](#2.3.1)
#     
#     2.5. [NHC](#2.3.2)
#     
#     2.6. [Biopsia](#2.3.3)
#     
#     2.7. [Biopsia sólida](#2.3.4)
#     
#     2.8. [Fecha](#2.3.5)
#     
#     2.9. [Definimos el resto de las variables](#2.4)
#     
#     2.10. [Ensayos clínicos y tratamientos disponibles](#2.4.1)
#     
#     2.11. [Número de chip y de paciente](#2.4.2)
#     
#     2.12. [Mutaciones y derivados](#2.4.3)
#     
#     2.13. [Mutaciones totales](#2.4.3.1)
#     
#     2.14. [Genes patogénicos](#2.4.3.2)
#     
#     2.15. [Variables de interés](#2.5)
#     
#     
#     
# 3. [Creación de DataFrame](#3)
# 
# 
# 4. [Exportación](#4)

# ## 1. Importaciones. <a id = "1"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# Hacemos las importaciones necesarias para que funcione el código.
# 
# Cada una de las bibliotecas estará correctamente explicada en la memoria disponible en GitHub. 

# In[1]:


import fitz 
import re
import pandas as pd
import os
import numpy as np


# ## 2. Desarrollo código. <a id = "2"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[2]:


CarpetaEntrada = "INPUT"
CarpetaDatos = "DATOS"
CarpetaInformes = "INFORMES"
CarpetaSalida = "OUTPUT"
CarpetaResultados = "RESULTADOS"
PathBase = os.getcwd()


# ## 2.1. Definición de funciones. <a id = "2.1."></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# Para la función `LeerFicherosPDF` se crea una lista vacía llamada **ficheros** y otra llamada **subcarpetas** que almacena las subcarpetas encontradas dentro de la ruta determinada por **os.walk(ruta)**. 
# 
# Se ordenan con **sorted()** usando el argumento **key** para hacerlo de forma numérica, sin tener en cuenta los valores no numéricos del nombre de cada carpeta. 
# 
# 
# Se itera sobre las subcarpetas ordenadas y se lee cada archivo PDF dentro de ellas, agregándolos a la lista ficheros junto con su ruta completa.
# 
# La función devuelve la lista ficheros que contiene las rutas de todos los archivos PDF encontrados en las subcarpetas ordenadas.

# In[ ]:


'''def LeerFicherosPDF(ruta):
    ficheros = []

    for raiz, directorios, archivos in os.walk(ruta):
        for archivo in archivos:
            if archivo.endswith('.pdf'):
                ficheros.append(os.path.join(raiz,archivo))

    return ficheros
'''


# In[25]:


def LeerFicherosPDF(ruta):
    ficheros = []
    subcarpetas = []

    for raiz, directorios, archivos in os.walk(ruta):
        # Obtener las subcarpetas y ordenarlas por nombre de forma numérica
        subcarpetas = sorted(directorios, key=lambda x: int(re.sub('\D', '', x)))

        for subcarpeta in subcarpetas:
            subcarpeta_ruta = os.path.normpath(os.path.join(raiz, subcarpeta))
            for archivo in os.listdir(subcarpeta_ruta):
                if archivo.endswith('.pdf'):
                    ficheros.append(os.path.normpath(os.path.join(subcarpeta_ruta, archivo)))
                    
    for archivo in os.listdir(ruta):
        if archivo.endswith('.pdf'):
            ficheros.append(os.path.normpath(os.path.join(ruta, archivo)))

    return ficheros


# La función `LeerDocumento` lee el contenido de un documento usando la libreria **PyMuPDF** (fitz). 
# 
# Con **fitz.open()** abre el documento denominado **nombreFichero** e inicializa la variable **text** como cadena vacía.
# 
# El bucle for nos permite recorrer cada página del documento y obtener el texto que lo forma. 
# 
# Finalmente, la función devuelve el texto dividido con el separador \n.

# In[9]:


def LeerDocumento(nombreFichero):
    with fitz.open(nombreFichero) as doc:
        text=""
        for page in doc:
            text = text + page.get_text()
    return text.split('\n')


# La función `BuscarValor` nos permite buscar una palabra determinada en el texto de cada fichero. 
# 
# Busca la palabra definida en la cadena **textoBuscar** en la lista de cadenas **lines**, para ello usamos la biblioteca **re**. Se recorren las posiciones en busca de los valores definidos en **textoBuscar** y en caso de encontrar, la nueva variable **valores** almacenará un valor 1, en caso de que no esté almacena un 0. 
# 
# Con el bucle for recorremos cada uno de los elementos almacenados en **valores** y se usa la técnica slicing [:] para extraer la subcadena que hay tras la última vez que aparece la palabra, almacenando los resultados en la nueva variable **Encontrados**. Strip permite eliminar los espacios en blanco.

# In[10]:


def BuscarValor(textoBuscar, lines):
    Encontrados = []

    valores = [1 if re.search(textoBuscar, line) else 0 for line in lines]
    valores = [i for i, s in enumerate(valores)  if s==1 in valores]

    posiciones = len(textoBuscar)
    
    for i in valores:
        Encontrados.append(lines[i][lines[i].rfind(textoBuscar)+posiciones:].strip())

    return Encontrados


# Esta función `GenerarImagen` es un extra que sirve para crear imágenes partiendo de los documentos. De cada hoja del fichero PDF se obtiene una imagen con su contenido.
# 
# En caso de querer usarla solo hay que descomentar (eliminar ''')

# In[ ]:


''' def GenerarImagen(ruta, fichero):
    i = 0   
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    with fitz.open(os.path.join(ruta,fichero)) as doc:
        for page in doc:
            i+=1
            val = f"image_{i+1}.png"
            pix = page.get_pixmap(matrix=mat)
            pix.save(os.path.join(ruta,fichero + "_" + val)) '''


# ## 2.2. Importación de ficheros Excel. <a id = "2.2"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[4]:


# Importamos el fichero que almacena los nombres del diagnóstico y su número correspondiente.
# La ruta corresponde al lugar donde se encuentra el fichero Diagnostico.xlsx
fichero = os.path.normpath(os.path.join(PathBase, CarpetaEntrada, CarpetaDatos, "Diagnostico.xlsx"))

diagnostico = pd.read_excel("INPUT/DATOS/Diagnostico.xlsx")
#print(diagnostico)

#Creo un diccionario con los valores del fichero importado. 
diagnosticos_dic = dict(zip(diagnostico["DIAGNÓSTICO"], diagnostico["NÚMERO DIAGNÓSTICO"]))

# En cada iteración, almacena el diagnóstico y si valos correspondiente, almacenándolo en valor, lo que nos permite imprimir el diccionario en filas separadas. 
for diagnostico in diagnosticos_dic:
    valor = diagnosticos_dic.get(diagnostico)
    print(diagnostico, valor)


# In[5]:


# Importamos el fichero Excel con la información tanto de los genes como de su número correspondiente. 
# La ruta corresponde a la posición donde se encuentra almacenado el fichero Genes.xlsx
fichero = os.path.normpath(os.path.join(PathBase, CarpetaEntrada, CarpetaDatos, "Genes.xlsx"))

genes = pd.read_excel(fichero)
#print(genes)

# Creamos una variable que contenga solo los nombres de los genes.
mutaciones = genes["GEN"].unique()
#print(mutaciones)

#Creo un diccionario con los valores del fichero.
mutaciones_dic = dict(zip(genes["GEN"], genes["Número gen"]))
mutaciones_dic

# Usamos items() para recorrer los elementos del diccionario, devolviendo el gen con su respectivo valor.
# Es otra forma de recorrer el diccionario para obtener su contenido.
for gen, valor in mutaciones_dic.items():
    print(gen, valor)


# ## 2.3. Definición de algunas variables. <a id = "2.3"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[28]:


rutaEntrada = os.path.normpath(os.path.join(PathBase, CarpetaEntrada, CarpetaInformes))


# In[29]:


#Se inicializan las variables como listas vacías.
fecha_Data = []
NHC_Data = [] 
Nbiopsia_Data = [] 
texto_Data = []
#Los resultados de la función LeerFicherosPDF se almacenan en ficheros.

ficheros = LeerFicherosPDF(rutaEntrada)

for ficheroPDF in ficheros:
    #os.path.normpath() normaliza la ruta resultante eliminando cualquier redundancia en la ruta y asegura que esté en un formato estandarizado.
    #os.path.join() une la ruta Ruta y el nombre del archivo ficheroPDF en una ruta completa. 
    lines = LeerDocumento(os.path.normpath(os.path.join(rutaEntrada,ficheroPDF)))

    #print(lines)
    #Aplicamos la función BuscarValor para almacenar distintas palabras dentro de distintas variables
    NHC_Data.append(BuscarValor("NHC:", lines))
    Nbiopsia_Data.append(BuscarValor("biopsia:", lines))
    fecha_Data.append(BuscarValor("Fecha:", lines))
    texto_Data.append(BuscarValor("de la muestra:", lines))
    #GenerarImagen(Ruta, ficheroPDF)
print(NHC_Data)
print(Nbiopsia_Data)
print(fecha_Data)
print(texto_Data)


# ## 2.3.1. Diagnóstico. <a id = "2.3.1"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[30]:


# Definimos las variables que vamos a usar. 
textoDiag = []
numeroDiag = []

# Recorremos los resultados alamacenados en la variable texto_Data para crear una variable sin repeticiones donde almacene los resultados. 
# Texto_Data almacena los resultados obtenidos en la funcion BuscarValor. Lo que queremos es crear una variable que almacene solo una vez cada uno de los resultados obtenidos en las listas. 
for i in texto_Data:
    sinduplicados = list(set(i))
    textoDiag.append([x for x in i if x in sinduplicados][0])
print(textoDiag)
    
# Teniendo importado ya el fichero de los diagnósticos, puedo usar este para recorrer la variable anterior textoDiag y en caso de que coincida
# con algún elemento del diccionario, nos devuelve su valor en una nueva variable llamada numeroDiag.
for diagnostico in textoDiag:
    valor = diagnosticos_dic.get(diagnostico)
    numeroDiag.append(valor)
    print(numeroDiag)


# ## 2.3.2 NHC. <a id = "2.3.2"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[31]:


# Definimos una nueva variable. 
NHC = []

#Recorremos cada uno de los elementos de NHC_Data para crear una variable nueva que almacene únicamente uno de los resultados de cada fichero.
for i in NHC_Data:
    sinduplicadosNHC = list(set(i))
    NHC.append([x for x in i if x in sinduplicadosNHC][0])
print(NHC)


# ## 2.3.3 Biopsia. <a id = "2.3.3"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[32]:


lista_resultante =  []
elementos_vistos = set()

# Recorremos los valores de Nbiopsia_Data para crear una variable sin duplicados y así asegurarnos de que solo existe una copia del total de resultados obtenidos. 
for sublist in Nbiopsia_Data:
    sublist_sin_duplicados = []
    for elemento in sublist:
        if elemento not in elementos_vistos:
            sublist_sin_duplicados.append(elemento)
            elementos_vistos.add(elemento)
    lista_resultante.append(sublist_sin_duplicados)

print(lista_resultante)

NB_values = [elemento for sublist in lista_resultante for elemento in sublist]
print(NB_values)


# In[33]:


# Nos interesa saber el valor del tercer elemento de cada uno de los valore de biopsia, ya que van a determinar sin son biopsia, citología o punción. 
biopsia = [x[2] for x in NB_values]
biopsia


# ## 2.3.4 Biopsia sólida. <a id = "2.3.4"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[34]:


# Para cada una de las posibles letras que pueden aparecer en esa posición, se le ha asignado un número
#B de biopsia = 1
#C de citología = 3
#P de punción = 2
B = "1"
C = "3"
P = "2"
Biopsia_solida = []

# Cada vez que encuentre una de las tres letras, almacenará su número correspondiente definido arriba en la nueva variable Biopsia_solida
for i in biopsia:
    if i == "B":
        Biopsia_solida.append(B)
        print("1")
    elif i == "P":
        Biopsia_solida.append(P)
        print("2")
    else:
        Biopsia_solida.append(C)
        print("3")
        
print(Biopsia_solida)


# ## 2.3.5.Fecha. <a id = "2.3.5"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[35]:


# Como con fechas nos pasa lo mismo (que aparecen repetidas veces el mismo resultado y solo nos intersa una vez). Creamos una nueva variable para almacenar solo un resultado cada vez.
fechas = []
for i in fecha_Data:
    sinduplicados = list(set(i))
    fechas.append([x for x in i if x in sinduplicados][0])

print(fechas)


# ## 2.4. Definimos el resto de las variables. <a id = "2.4"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# ## 2.4.1. Ensayos clínicos y tratamientos disponibles. <a id = "2.4.1"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# A la hora de obtener el número de ensayos clínicos y tratamientos disponibles, lo hacemos de la misma forma. Como vemos, el número de ensayos/tratamientos se encuentra justo delante de la palabra. 
# 
# Aprovechamos ese método para crear un patrón que usando expresiones regulares, nos pueda devolver dicho valor. Para ello especificamos con r"(\d+)\s* que nos interesa la cadena de texto que contenga cualquier número de 0-9 ambos incluidos y que se encuentre justo antes de la palabra definida posteriormente (Ensayos clínicos y tratamientos disponibles). 
# Tras determinar las variables de interés que vamos a usar, recorremos el texto de cada uno de los ficheros para buscar el patrón usando el método **re.search()**. Una vez encontrado, se convierte en entero (int()) para poder ser almacenado en la variable ensayos/tratamientos y usando group(1) para obtener solo el número. 
# Añadimos con append los valores almacenados en ensayos/tratamientos a la variable definida arriba ensayos_finales/tratamientos_finales. 
# 
# Posteriormente se ha desarrollado una función que nos permite modificar los valores. En caso de no haber obtenido ningún número de ensayos/tratamientos, añadimos un 0 a la nueva variable. En caso de haber obtenido uno o más resultados, añadimos un 1. De esta forma estamos binarizando los resultados.

# In[36]:


#Definimos el patrón de búsqueda
patron = r"(\d+)\s* Ensayos clínicos"
ficheros = LeerFicherosPDF(rutaEntrada)
#También las variables como lsitas vacías
lista_ensayos = []
ensayos_finales = []

for ficheroPDF in ficheros:
    lines = LeerDocumento(os.path.normpath(os.path.join(rutaEntrada,ficheroPDF)))
    
    ensayos = 0
    #Recorremos lines
    for line in lines:
        resultado = re.search(patron, line)
        #Cuando aparece el resultado, añadimos el entero a la variable 
        if resultado:
            ensayos = int(resultado.group(1))
            
    #Añadimos lista_ensayos a ensayos
    lista_ensayos.append(ensayos)   
    
    #print(ficheroPDF + " -> Ensayos: " + str(ensayos))
print(lista_ensayos) 

#Binarizamos la variable
for i in lista_ensayos:
    if i == 0:
        ensayos_finales.append(0)
    else:
        ensayos_finales.append(1)
        
print(ensayos_finales)


# In[37]:


patron2 = r"(\d+)\s* Tratamientos disponibles"
ficheros = LeerFicherosPDF(rutaEntrada)

lista_tratamientos = []
tratamientos_finales = []

for ficheroPDF in ficheros:
    lines = LeerDocumento(os.path.normpath(os.path.join(rutaEntrada, ficheroPDF)))
    tratamientos = 0
    
    for line in lines:
        resultado = re.search(patron2, line)
        if resultado:
            tratamientos = int(resultado.group(1))
    
    lista_tratamientos.append(tratamientos)
    #print(ficheroPDF + " -> Tratamientos: " + str(tratamientos))
    
print(lista_tratamientos)

#Binarizamos la variable
for i in lista_tratamientos:
    if i == 0:
        tratamientos_finales.append(0)
    else:
        tratamientos_finales.append(1)
print(tratamientos_finales)


# ## 2.4.2. Número de chip y de paciente. <a id = "2.4.2"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[38]:


#Iteramos sobre cada fichero de la variable ficheros
for ficheroPDF in ficheros:
    #os.path.isfile() para verificar si la ruta corresponde a un archivo existente
    #os.path.join() y os.path.normpath() crean una ruta junto con el nombre del archivo ficheroPDF y que sea formato PDF
    if os.path.isfile(os.path.normpath(os.path.join(rutaEntrada, ficheroPDF))) and ficheroPDF.endswith(".pdf"):
        print(ficheroPDF)


# In[39]:


numero_paciente = [] 

for ficheroPDF in ficheros:
    if os.path.isfile(os.path.normpath(os.path.join(rutaEntrada, ficheroPDF))) and ficheroPDF.endswith(".pdf"):
        #se separa la ruta del nombre del archivo siendo ruta1 la ruta y fichero1 el fichero
        ruta1, fichero1 = os.path.split(ficheroPDF)
        #Se divide el nombre del archivo en nombre y extensión. Con [0] obtenemos solo el nombre
        paciente = os.path.splitext(fichero1)[0]
        #Dentro del nombre, obtenemos el séptimo valor
        pacientes = paciente[7]
        #Agrega el número el paciente a la lista definida anteriormente
        numero_paciente.append(pacientes)
        print(numero_paciente)


# In[40]:


chip2 = []
for ficheroPDF in ficheros:
    if os.path.isfile(os.path.normpath(os.path.join(rutaEntrada, ficheroPDF))) and ficheroPDF.endswith(".pdf"):
        # Esta expresión regular nos permite obtener el valor numérico (una o más cifras numéricas) siempre que estén entre v y _ (en este caso v100_)
        patron = r"v(\d+)_"
        resultado = re.search(patron, ficheroPDF)
        # Si aparece, almacenamos el valor en numero_chip para posteriormente añadir los valores a una nueva variable chip2.
        if resultado:
            numero_chip = resultado.group(1)
            chip2.append(numero_chip)
print(chip2)


# ## 2.4.3. Mutaciones y derivados. <a id = "2.4.3"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# ## 2.4.3.1. Mutaciones totales. <a id = "2.4.3.1"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[41]:


ficheros = LeerFicherosPDF(rutaEntrada) 
max_mut = 0
genes_mut2 = {}
frecuencias_totales = []
patron_frecuencia = re.compile(r"\d{2}\.\d{2}")

for ficheroPDF in ficheros:
    nombreFichero = os.path.normpath(os.path.join(rutaEntrada, ficheroPDF))
    lines = LeerDocumento(nombreFichero)
    total_mut = 0
    encontrados2 = []
    lista_frec = []
    
    for mutacion in mutaciones:
        if mutacion in lines:
            posicion = lines.index(mutacion)
            if mutacion == "FGFR4": 
                # Comprobamos que la siguiente posición a la del gen no sea p.(P136L). Si lo es pasamos, si no lo es añadimos un 1 a la variable total, añadimos la mutación a la variable encontrados 2 e imprimimos el valor.
                if (posicion < len(lines)-1 and lines[posicion + 1] == "p.(P136L)"):
                    pass
                else:
                    total_mut += 1
                    encontrados2.append(mutacion)
                    #print(ficheroPDF + " - Existe: " + mutacion)
        
            else:
                #Asumimos que la variable benigno es False usando boleanos. 
                benigno = False
                # Recorremos todas las posiciones
                for a in range(posicion+1, posicion+10):
                    #Si aparece Benign en las líneas, la variable definida anteriormente como False para a ser True.
                    if "Benign" in lines[a]:
                        benigno = True
                # Como las benignas no interesan, nos quedamos con las que siguen teniendo valor False
                if benigno == False:
                    # Añadimos 1 a la variable total_mut y añadimos la mutación a encontrados2. Imprimimos las mutaciones con sus respectivos ficheros
                    total_mut += 1
                    encontrados2.append(mutacion)
                    print(nombreFichero + " - Existe: " + mutacion)
                if not benigno:
                    for i in lines[posicion:posicion+10]:
                        #Usamos el patron definido anteriormente para obtener el porcentaje alélico de cada gen
                        resultado = re.search(patron_frecuencia, i)
                        if resultado:
                            frec = resultado.group()
                            lista_frec.append(frec)
                            
                    

    genes_mut2[ficheroPDF.replace("\\","_")] = encontrados2
    if total_mut > max_mut:
        max_mut = total_mut
        
    frecuencias_totales.append(lista_frec)
    
    #print(f"{ficheroPDF} - Número total de mutaciones : {total_mut}")
    #print(f"{ficheroPDF} - Frecuencias: {lista_frec}")


# In[42]:


frecuencias_totales


# In[43]:


# Creamos una nueva variable para almacenar solo los genes (valores) de la variable genes_mut2, ya que almacenaba tanto el nombre del fichero como los genes de interés que se modificaban.
mut = list(genes_mut2.values())
mut


# In[44]:


# Creamos una nueva función para que almacene el número de mutaciones que hay en cada fichero, para ello aplicamos la función len sobre la variable mut.
num_mutaciones = [len(i) for i in mut]
print(num_mutaciones)


# In[45]:


# Como ya tenemos un diccionario con las mutaciones y sus números correspondientes, podemos usarlo. 
numero_iden = []
for i in mut:
    # Se busca en el diccionario el valor asociado al gen, devolviéndolo. En caso de no encontrar ninguno, se devuelve 0.
    valores = [mutaciones_dic.get(gen, 0) for gen in i]
    # Los números obtenidos se agregan a la variable numero_iden
    numero_iden.append(valores)

print(numero_iden)


# In[46]:


fusiones = []
for ficheroPDF in ficheros:
    lines = LeerDocumento(os.path.normpath(os.path.join(rutaEntrada,ficheroPDF)))
    variantes = []
    
    for linea in lines:
        for mutacion in mutaciones:
            # Nos interesa tener las fusiones de los genes. 
            # Definimos el patrón: cuaalquier letra (mayúsculas) o número que aparezca una o más veces seguida de - y cualquier valor que aparezca en la variable mutación.
            patronGen = re.compile(r"[A-Z0-9]{1,}-" + mutacion)
            # En caso de encontrar el patrón, se almacenan las fusiones en la variable resultados.
            resultado = re.search(patronGen, linea)
            if resultado:
                # En caso afirmativo, se crea una nueva expresión regular para obtener el ID de cada una de las fusiones.
                gen = resultado.group()
                patronVariante = re.compile(gen + "[.][A-Za-z0-9]{1,}[.][A-Za-z0-9]{1,}")
                resultadoVariante = re.search(patronVariante,linea)
                if resultadoVariante:
                    variante = resultadoVariante.group(0)
                    variantes.append(variante)
    fusiones.append(variantes)
    #print(ficheroPDF)
    #print(variantes)
                    
fusiones


# ## 2.4.3.2. Genes patogénicos. <a id = "2.4.3.2"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[47]:


for ficheroPDF in ficheros:
    nombreFichero = os.path.normpath(os.path.join(rutaEntrada, ficheroPDF))
    lines = LeerDocumento(nombreFichero)
    
    for mutacion in mutaciones:
        if mutacion in lines:
            posicion = lines.index(mutacion)

            for a in range(posicion+1, min(posicion+10, len(lines))):
                # En caso de que aparezca la palabra Pathogeni en el archivo,imprime el fichero, la mutación y Pathogenic.
                if "Pathogeni" in lines[a]:
                    print(nombreFichero + " - Existe: " + mutacion + " - Pathogenic")
                


# In[48]:


patron_frecuencia = re.compile(r"\d{2}\.\d{2}")
frecuenciasPato = []

for ficheroPDF in ficheros:
    nombreFichero = os.path.normpath(os.path.join(rutaEntrada, ficheroPDF))
    lines = LeerDocumento(nombreFichero)
    lista_frec = []
    
    for mutacion in mutaciones:
        if mutacion in lines:
            posicion = lines.index(mutacion)
            
            for a in range(posicion+1, min(posicion+10, len(lines))):
                if "Pathogeni" in lines[a]:
                    print(nombreFichero + "- Existe: " + mutacion + "- Pathogenic")
            
                    for i in lines[posicion:posicion+10]:
                        resultado = re.search(patron_frecuencia, i)
                        if resultado:
                            frec = resultado.group()
                            lista_frec.append(frec)
                            #frecuencias.append(frec)
    frecuenciasPato.append(lista_frec)
                            #print(f"   Frecuencia: {frec}")
        
    #print(f"{ficheroPDF} - Frecuencias: {lista_frec}")
    
frecuenciasPato


# In[50]:


patogen = {}

for ficheroPDF in ficheros:
    lines = LeerDocumento(os.path.normpath(os.path.join(rutaEntrada,ficheroPDF)))
    genpato2 = []
    
    for mutacion in mutaciones:
        if mutacion in lines:
            posicion = lines.index(mutacion)
            
            for a in range(posicion+1, min(posicion+10, len(lines))):
                if "Pathogeni" in lines[a]:
                    genpato2.append(mutacion)
                    #print(ficheroPDF + " - Existe: " + mutacion + " - Pathogenic")
            
                    
    
    patogen[ficheroPDF] = genpato2
    
patogen


# In[51]:


# Creamos una lista con los valores que son patogénicos.
patologicos = list(patogen.values())
patologicos


# In[52]:


# Como en el caso anterior, a cada una de las mutaciones patogénicas le corresponde un valor numérico.
numero_iden_pato = []
for i in patologicos:
    valores = [mutaciones_dic.get(gen, 0) for gen in i]
    numero_iden_pato.append(valores)

numero_iden_pato


# In[53]:


# Contamos el número de mutaciones patogénicas hay en cada fichero.
num_mutacionesPato = [len(i) for i in numero_iden_pato]
print(num_mutacionesPato)


# ## 2.5. Variables de interés. <a id = "2.5"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[54]:


# Número de chip 
chip2


# In[55]:


# Número de paciente 
numero_paciente


# In[56]:


# NHC
NHC


# In[57]:


# Número de biopsia 
NB_values


# In[58]:


# Biopsia sólida 
Biopsia_solida


# In[59]:


# Fecha de informe
print(fecha_Data)
print("---------------------------------------------------------------------------------------------------------------------")
print(fechas)


# In[60]:


# Diagnóstico 
print(texto_Data)
print("------------------------------------------------------------------------------------------------------------------")
print(textoDiag)


# In[61]:


# Número de diagnóstico 
numeroDiag


# In[62]:


# Total del número de mutaciones
num_mutaciones


# In[63]:


# Número de mutaciones patogénicas
num_mutacionesPato


# In[64]:


# Mutaciones detectadas totales 
mut


# In[65]:


# Fusiones
fusiones


# In[66]:


# % de frecuencia alélica
frecuencias_totales


# In[67]:


# % frecuencias alélicas patológicas 
frecuenciasPato


# In[68]:


# Nº de la mutación específica detectada 
numero_iden


# In[69]:


# Ensayos clínicos 
print(lista_ensayos)
print("-----------------------------------------------------------------------------------------------------------------")
print(ensayos_finales)


# In[70]:


# Fármaco aprobado 
print(lista_tratamientos)
print("-----------------------------------------------------------------------------------------------------------------")
print(tratamientos_finales)


# ## 3. Creación de DataFrame. <a id = "3"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# Join y merge son dos formas distintas de unir datos en Python usando la biblioteca pandas. 
# Sin embargo, en este caso se ha usado JOIN porque nos garantiza que no se crearán filas ni columnas espurias al unir los PDF, esto se debe a que une los DF por índices en lugar de por columnas (este tipo de unión es característico de merge, por lo que es capaz de crear resultados espurios). 
# En merge si se producen resultados espurios, esto ocurre cuando los datos tienen valores duplicados o vacíos o si los nombres de las columnas no coinciden en ambas tablas. Solo une los valores coincidentes de aquellas columnas con mismo nombre, eliminando el resto de las filas.

# In[71]:


# PACIENTES
T1 = pd.DataFrame({'Número de chip': chip2, 'Número de paciente': numero_paciente, 'NHC': NHC, 
                    'Número de biopsia': NB_values, 'Biopsia sólida': Biopsia_solida, 'Fecha de informe': fechas})


# In[72]:


# DIAGNOSTICO
T2 = pd.DataFrame({'Número de chip': chip2,'Número de biopsia': NB_values,'Diagnóstico': textoDiag, 
                   'Número del diagnóstico': numeroDiag})


# In[73]:


# MUTACIONES
T3 = pd.DataFrame({'Número de chip': chip2, 'Número de biopsia': NB_values,'Mutaciones detectadas':mut, 
                   'Número de la mutación específica':numero_iden, 'Total del número de mutaciones': num_mutaciones, 
                   'Porcentaje de frecuencia alélica (ADN)': frecuencias_totales, 'Fusiones ID':fusiones})


# In[74]:


# PATOGENICAS
T4 = pd.DataFrame({'Número de chip': chip2, 'Número de biopsia': NB_values,
                'Genes patogénicos': patologicos, 'Número de la mutación específica':numero_iden_pato, 
                '% frecuencia alélica':frecuenciasPato, 'Total de mutaciones patogénicas': num_mutacionesPato})


# In[75]:


# INFORMACION
T5 = pd.DataFrame({'Número de chip': chip2, 'Número de biopsia': NB_values,'Ensayos clínicos': lista_ensayos,
                   'SI/NO ensayo':ensayos_finales, 'Fármaco aprobado': lista_tratamientos, 'SI/NO fármacos': tratamientos_finales})


# In[76]:


tabla_unida = T1.join(T2.set_index(["Número de chip", "Número de biopsia"]), on=["Número de chip", "Número de biopsia"])
tabla_unida


# In[86]:


tabla_unida2 = tabla_unida.join(T3.set_index(["Número de chip", "Número de biopsia"]), on=["Número de chip", "Número de biopsia"])
tabla_unida2


# In[87]:


tabla_final = tabla_unida2.join(T5.set_index(["Número de chip", "Número de biopsia"]), on=["Número de chip", "Número de biopsia"])
tabla_final


# In[79]:


tabla_unida3 = tabla_unida.join(T4.set_index(["Número de chip", "Número de biopsia"]), on=["Número de chip", "Número de biopsia"])
tabla_unida3


# In[80]:


tabla_final_pato = tabla_unida3.join(T5.set_index(["Número de chip", "Número de biopsia"]), on=["Número de chip", "Número de biopsia"])
tabla_final_pato


# ## 4. Exportación. <a id = "4"></a><a href="#index"><i class="fa fa-list-alt" aria-hidden="true"></i></a>

# In[90]:


rutaSalida = os.path.normpath(os.path.join(PathBase, CarpetaSalida))

if os.path.exists(rutaSalida) == False:
    os.makedirs(rutaSalida)
    
rutaResultados = os.path.normpath(os.path.join(rutaSalida, CarpetaResultados))

if os.path.exists(rutaResultados) == False:
    os.makedirs(rutaResultados)


# In[84]:


# Exportar el dataframe a un archivo Excel con índices
fichero = os.path.normpath(os.path.join(rutaSalida, "TablaPato.xlsx"))

tabla_final_pato.to_excel(fichero)


# In[88]:


# Exportar el dataframe a un archivo Excel con índices
fichero = os.path.normpath(os.path.join(rutaSalida, "TablaGeneral.xlsx"))

tabla_final.to_excel(fichero)


# In[91]:


# Divide el DataFrame en fragmentos de 80 líneas
fragmentos = np.array_split(tabla_final, len(tabla_final) // 80 + 1)

# Guarda cada fragmento en un archivo Excel separado
for i, fragmento in enumerate(fragmentos):
    nombre_archivo = f"tabla_final{i}.xlsx"
    ruta_archivo = os.path.normpath(os.path.join(rutaResultados, nombre_archivo))
    fragmento.to_excel(ruta_archivo, index=False)
    print(f"Archivo {nombre_archivo} guardado correctamente.")


# In[92]:


# Divide el DataFrame en fragmentos de 80 líneas
fragmentos = np.array_split(tabla_final_pato, len(tabla_final_pato) // 80 + 1)

# Guarda cada fragmento en un archivo Excel separado
for i, fragmento in enumerate(fragmentos):
    nombre_archivo = f"patogenicos_{i}.xlsx"
    ruta_archivo = os.path.join(rutaResultados, nombre_archivo)
    fragmento.to_excel(ruta_archivo, index=False)
    print(f"Archivo {nombre_archivo} guardado correctamente.")


# In[ ]:




