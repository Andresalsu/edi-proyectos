from PIL import Image
from os import listdir
from os.path import isfile, join
import os, unidecode, shutil, pytesseract, re, imagehash, cv2, numpy as np
from pdf2image import convert_from_path
from spellchecker import SpellChecker
from detectTables import buscarTablas

path = "/Users/andalval/Desktop/prueba datalicit/2. SENA DIRECCIÓN GENERAL Dirección Jurídica DG-LP-001-2019/"
archivos = [f for f in listdir(path) if isfile(join(path, f))]
spell = SpellChecker(language='es')
i=1
for x in archivos:
    ruta = path + x
    try:
        os.stat(path+"/Imagenes para analizar")
    except:
        os.mkdir(path+"/Imagenes para analizar")
    rutanueva=path+"/Imagenes para analizar"
    if ruta.endswith('.pdf') and "PLIEGO" in x or "Pliego" in x:
        pages = convert_from_path(ruta, dpi=200)
        for page in pages:
            filename = x.replace(' ','_') + "-" + str(i) + '.jpg'
            page.save(os.path.join(rutanueva,filename), 'JPEG')
            i=i+1

path = path+"Imagenes para analizar/"

def buscarCoincidencias(palabra=[], extension=0):
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
    ocurrencias=[]
    for x in archivos:
            ruta = path + x
            if ruta.endswith('.jpg') and "PLIEGO" in x or "Pliego" in x:
                im = Image.open(ruta)
                # Utilizamos el método "image_to_string"
                # Le pasamos como argumento la imagen abierta con Pillow
                try:
                    os.stat(path+"texto"+x+".txt")
                except:
                    texto = pytesseract.image_to_string(im)
                    texto=unidecode.unidecode(texto)
                    datafile = ''
                    with open(path+"texto"+x+".txt", "w") as text_file:
                        text_file.write(texto)
                with open(path+"texto"+x+".txt", "r") as text_file:
                    datafile = text_file.readlines()
                for i, line in enumerate(datafile):
                    for d in palabra:
                        if d in line:
                            for l in datafile[i:i+extension]:
                                ocurrencias.append(l.replace('\n',''))
    return ocurrencias
def buscarPresupuesto():
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra=["presupuesto oficial","suma de","PRESUPUESTO OFICIAL","Presupuesto oficial", "Presupuesto Oficial"]
    ocurrencias=buscarCoincidencias(palabra,4)
    results=''
    for j in ocurrencias:
        if '$' in j:
            presupuesto = re.findall(r'\d+\b', j)
            results = ''.join(presupuesto)
            return j

def buscarCodigo():
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra=["LICITACION PUBLICA", "PROCESO CONTRACTUAL", "Licitacion publica", "Proceso contractual"]
    ocurrencias=buscarCoincidencias(palabra,2)
    p=0
    results=''
    for u in ocurrencias:
        if '-' in u:
            results=ocurrencias[p]
        p += 1
    return results

def buscarObjeto():
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra=["OBJETO:","OBJETO","Objeto","Objeto:"]
    ocurrencias=buscarCoincidencias(palabra,9)
    results=''
    for j in ocurrencias:
        if 'CONTRATAR ' in j or 'Contratar 'in j:
            resultados=ocurrencias[ocurrencias.index(j):ocurrencias.index(j)+8]
            results=' '.join(resultados)
        elif 'PRESTAR ' in j or 'Prestar ' in j:
            resultados=ocurrencias[ocurrencias.index(j):ocurrencias.index(j)+8]
            results=' '.join(resultados)
    return results

def buscarPlazo():
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra=["plazo de ejecuci","Plazo de ejecuci"]
    ocurrencias=buscarCoincidencias(palabra,3)
    p=0
    results=''
    for j in ocurrencias:
        if 'sera' in j:
            fecha = ocurrencias[p:p+4]
            results = ''.join(fecha)
            return results
        p += 1

def buscarUNSPSC():
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra=["UNSPSC","CODIGO UNSPSC","SEGMENTO","Segmento","segmento"]
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
    ocurrencias=[]
    i=0
    # Abrimos la imagen
    for x in archivos:
        ruta = path + x
        if ruta.endswith('.jpg') and "PLIEGO" in x or "Pliego" in x:
            im = Image.open(ruta)
            # Utilizamos el método "image_to_string"
            # Le pasamos como argumento la imagen abierta con Pillow
            try:
                os.stat(path+"texto"+x+".txt")
            except:
                texto = pytesseract.image_to_string(im)
                texto=unidecode.unidecode(texto)
                datafile = ''
                with open(path+"texto"+x+".txt", "w") as text_file:
                    text_file.write(texto.encode().decode())
            with open(path+"texto"+x+".txt", "r") as text_file:
                datafile = text_file.readlines()
            for i, line in enumerate(datafile):
                for d in palabra:
                    if d in line:
                        encontrados=buscarTablas(ruta)
                        for u in encontrados:
                            texteando=pytesseract.image_to_string(u)
                            texteando=unidecode.unidecode(texteando)
                            if any(i.isdigit() for i in texteando):
                                os.rename(u,r'data/UNSPSC-'+str(i)+'.png')
                                ocurrencias.append('data/UNSPSC-'+str(i)+'.png')
                                i += 1
    dosocurrencias=[]
    for a in ocurrencias:
        for b in ocurrencias:
            try:
                if str(a) is not str(b) and os.path.exists(a) and os.path.exists(b):
                    an = cv2.imread(a)
                    bn = cv2.imread(b)
                    an = cv2.resize(an,(500,300))
                    bn = cv2.resize(bn,(500,300))
                    difference = cv2.subtract(an, bn)    
                    result = not np.any(difference)
                    if result is True:
                        ocurrencias.remove(b)
                        dosocurrencias.append(b)
            except OSError as e:
                print(e.strerror)
                continue
    for i in dosocurrencias:
        if (i in ocurrencias):
            dosocurrencias.remove(i)
    for i in dosocurrencias:
        if(os.path.exists(i)):
            os.remove(os.path.abspath(i))
    return ocurrencias

def buscarFinanciera():
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra=["CAPACIDAD FINANCIERA","Capacidad financiera", "Capacidad Financiera", "INDICADORES FINANCIEROS", "Indicadores financieros"]
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
    ocurrencias=[]
    # Abrimos la imagen
    for x in archivos:
        ruta = path + x
        if ruta.endswith('.jpg') and "PLIEGO" in x or "Pliego" in x:
            im = Image.open(ruta)
            # Utilizamos el método "image_to_string"
            # Le pasamos como argumento la imagen abierta con Pillow
            try:
                os.stat(path+"texto"+x+".txt")
            except:
                texto = pytesseract.image_to_string(im)
                texto=unidecode.unidecode(texto)
                datafile = ''
                with open(path+"texto"+x+".txt", "w") as text_file:
                    text_file.write(texto.encode().decode())
            with open(path+"texto"+x+".txt", "r") as text_file:
                datafile = text_file.readlines()
            for i, line in enumerate(datafile):
                for d in palabra:
                    if d in line:
                        encontrados=buscarTablas(ruta)
                        for u in encontrados:
                            texteando=pytesseract.image_to_string(u)
                            texteando=unidecode.unidecode(texteando)
                            if 'Endeudamiento' in texteando or 'ENDEUDAMIENTO' in texteando or 'endeudamiento' in texteando:
                                os.rename(u,r'data/Finaciero-'+str(i)+'.png')
                                ocurrencias.append('data/Financiero-'+str(i)+'.png')
                                i += 1
    dosocurrencias=[]
    for a in ocurrencias:
        for b in ocurrencias:
            try:
                if str(a) is not str(b) and os.path.exists(a) and os.path.exists(b):
                    an = cv2.imread(a)
                    bn = cv2.imread(b)
                    an = cv2.resize(an,(500,300))
                    bn = cv2.resize(bn,(500,300))
                    difference = cv2.subtract(an, bn)    
                    result = not np.any(difference)
                    if result is True:
                        ocurrencias.remove(b)
                        dosocurrencias.append(b)
            except OSError as e:
                print("Failed with:"+e.strerror)
                continue
    for i in dosocurrencias:
        if (i in ocurrencias):
            dosocurrencias.remove(i)
    for i in dosocurrencias:
        if(os.path.exists(i)):
            os.remove(os.path.abspath(i))
    if not ocurrencias:
        ocurrencias=buscarCoincidencias(palabra,10)
        p=0
        results=''
        for j in ocurrencias:
            busqueda=['INDICE DE LIQUIDEZ','Indice de liquidez','Indice de Liquidez','INDICE DE ENDEUDAMIENTO', 'Indice de endeudamiento',
            'Indice de Endeudamiento']
            if 'INDICE DE LIQUIDEZ' in j or 'Indice de liquidez' in j or 'Indice de Liquidez' in j:
                fecha = ocurrencias[p:p+10]
                results = fecha
                return results
            p += 1
    return ocurrencias

def buscarOrganizacional():
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra=["CAPACIDAD ORGANIZACIONAL","Capacidad organizacional", "Capacidad Organizacional", 'INDICADORES DE CAPACIDAD ORGANIZACIONAL', "Indicadores de capacidad organizacional"]
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
    ocurrencias=[]
    # Abrimos la imagen
    for x in archivos:
        ruta = path + x
        if ruta.endswith('.jpg') and "PLIEGO" in x or "Pliego" in x:
            im = Image.open(ruta)
            # Utilizamos el método "image_to_string"
            # Le pasamos como argumento la imagen abierta con Pillow
            try:
                os.stat(path+"texto"+x+".txt")
            except:
                texto = pytesseract.image_to_string(im)
                texto=unidecode.unidecode(texto)
                datafile = ''
                with open(path+"texto"+x+".txt", "w") as text_file:
                    text_file.write(texto.encode().decode())
            with open(path+"texto"+x+".txt", "r") as text_file:
                datafile = text_file.readlines()
            for i, line in enumerate(datafile):
                for d in palabra:
                    if d in line:
                        encontrados=buscarTablas(ruta)
                        for u in encontrados:
                            texteando=pytesseract.image_to_string(u)
                            texteando=unidecode.unidecode(texteando)
                            if "RENTABILIDAD " in texteando or "Rentabilidad " in texteando or "Rentabilidad " in texteando or 'Rentabilidad ' in texteando:
                                os.rename(u,r'data/Organizacional-'+str(i)+'.png')
                                ocurrencias.append('data/Organizacional-'+str(i)+'.png')
                                i += 1
    dosocurrencias=[]
    for a in ocurrencias:
        for b in ocurrencias:
            try:
                if str(a) is not str(b) and os.path.exists(a) and os.path.exists(b):
                    an = cv2.imread(a)
                    bn = cv2.imread(b)
                    an = cv2.resize(an,(500,300))
                    bn = cv2.resize(bn,(500,300))
                    difference = cv2.subtract(an, bn)    
                    result = not np.any(difference)
                    if result is True:
                        ocurrencias.remove(b)
                        dosocurrencias.append(b)
            except OSError as e:
                print("Failed with:"+e.strerror)
                continue
    for i in dosocurrencias:
        if (i in ocurrencias):
            dosocurrencias.remove(i)
    for i in dosocurrencias:
        if(os.path.exists(i)):
            os.remove(os.path.abspath(i))
    if not ocurrencias:
        ocurrencias=buscarCoincidencias(palabra,10)
        p=0
        results=''
        for j in ocurrencias:
            if 'RENTABILIDAD' in j or 'Rentabilidad' in j or 'rentabilidad' in j:
                fecha = ocurrencias[p:p+10]
                results = fecha
                return results
            p += 1
    return ocurrencias

try:
    valor = buscarPresupuesto()
    print(valor)
except OSError as e:
    print("Failed with:"+e.strerror)
    print("Valor no encontrado")
try:
    codigo=buscarCodigo()
    print(codigo)
except OSError as e:
    print("Failed with:"+e.strerror)
    print("Codigo no encontrado")
try:
    objeto=buscarObjeto()
    pobjeto=objeto.split()
    h=''
    for k in pobjeto:
        h=h+' '+spell.correction(k)
    print(h)
except OSError as e:
    print("Failed with:"+e.strerror)
    print("Objeto no encontrado")
try:
    h=''
    ejecucion=buscarPlazo()
    try:
        pejecucion=ejecucion.split()
        for k in pejecucion:
            h=h+' '+spell.correction(k)
    except:
        print('Plazo de ejecucion no encontrado')
    print(h)
except OSError as e:
    print("Failed with:"+e.strerror)
    print('Plazo de ejecucion no encontrado')
try:
    finales=buscarUNSPSC()
    unspsc=list(dict.fromkeys(finales))
    print(unspsc)
except OSError as e:
    print("Failed with:"+e.strerror)
    print("Clasificacion UNSPSC no encontrada")
try:
    finales=buscarFinanciera()
    financieros=list(dict.fromkeys(finales))
    if not financieros:
        print('Datos financieros no encontrados')
    else:
        for j in financieros:
            print(j)
except OSError as e:
    print("Failed with:"+e.strerror)
    print("Datos financieros no encontrados")
try:
    finales=buscarOrganizacional()
    organizacionales=list(dict.fromkeys(finales))
    if not organizacionales:
        print('Datos organizacionales no encontrados')
    else:
        for j in organizacionales:
            print(j)
except OSError as e:
    print("Failed with:"+e.strerror)
    print("Datos organizacionales no encontrados")
#shutil.rmtree(rutanueva, ignore_errors=True)