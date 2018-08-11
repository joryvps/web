#!/usr/bin/env python2.7

import argparse
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from blessings import Terminal

t = Terminal()

# Comprobar si hay args, imprimir el logotipo y el uso
if not len(sys.argv[1:]):
    print t.cyan("""

     ____.________ _______________.___.         ____._____.___.
    |    |\_____  \\______   \__  |   |        |    |\__  |   |
    |    | /   |   \|       _//   |   |        |    | /   |   |
/\__|    |/    |    \    |   \\____   |    /\__|    | \____   |
\________|\_______  /____|_  // ______| /\ \________| / ______|
                  \/       \/ \/        \/            \/       


Bienvenido a JORY.JY

Para comenzar a utilizar este script, proporcione uno o más comandos
argumentos de línea y su valor correspondiente, cuando corresponda.
Para mostrar todas las opciones disponibles, use -h o --help.

Ejemplos:
jory.py -h
jory.py -d inurl:show.php?id= --verbose\n""")
    
    sys.exit(0)


# Handle command line arguments
parser = argparse.ArgumentParser(description="Utilice este script y dorks para buscar aplicaciones web vulnerables.")
group = parser.add_mutually_exclusive_group()
group.add_argument("-d", "--dork", help="		especifica el dork que deseas usar\n")
group.add_argument("-l", "--list", help="		especificar ruta a la lista con dorks\n")
parser.add_argument("-v", "--verbose", action="store_true", help="		toggle verbosity\n")
args = parser.parse_args()

dork_list = []

# Dork list processing
if args.list:
	print "\n[" + t.green("+") + "]Leyendo en lista desde: " + args.list + "\n\n"	
	try:
		with open(args.list, "r") as ins:
			for line in ins:
				dork_list.append(line)
				
				if args.verbose == True:
					print "[" + t.magenta("~") + "]" + line 
				
	except IOError as e:
		print "\n[" + t.red("!") + "]No se pudo leer la lista de dork"
		if args.verbose == True:
			print "\nAn IO Se produjo un error con el siguiente mensaje de error: "
			print "\n %s" % (e)
            
else:
    dork_list.append(args.dork)



print "\n[" + t.green("+") + "]¿Le gustaría que JORY le aprobara la conexión con el motor de búsqueda?"
query = raw_input("[Y]es/[N]o: ").lower()

if query == 'y':
	IP = raw_input("\n[" + t.green("+") + "]Por favor ingrese la IP del host proxy: ")
	PORT = raw_input("\n[" + t.green("+") + "]Por favor ingrese el puerto proxy: ")
	set_proxy = True
elif query == 'n':
	print "\n[" + t.green("+") + "]Estableciendo conexión sin proxy ...\n"
	set_proxy = False
else:
	print "\n[" + t.red("!") + "]Opción no controlada, por defecto a la conexión sin proxy ..."
	set_proxy = False


# Web Driver Proxy
def proxy(PROXY_HOST,PROXY_PORT):
	fp = webdriver.FirefoxProfile()
	print "[" + t.green("+") + "]Proxy host configurado para: " + PROXY_HOST
	print "[" + t.green("+") + "]Proxy puerto configurado para: " + PROXY_PORT
	print "\n[" + t.green("+") + "]Estableciendo conexión..."
	fp.set_preference("network.proxy.type", 1)
	fp.set_preference("network.proxy.http",PROXY_HOST)
	fp.set_preference("network.proxy.http_port",int(PROXY_PORT))
	fp.set_preference("general.useragent.override","'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'")
	fp.update_preferences()
	return webdriver.Firefox(firefox_profile=fp)


# Function to generate and process results based on input
def search():
	link_list = []
	
	if set_proxy == True:
		driver = proxy(IP, PORT)
	else:
		driver = webdriver.Firefox()
    
	for int in range(1):
		try:
			driver.get("http://google.com")
		except Exception as e:
			print "\n[" + t.red("!") + "]No se pudo establecer una conexión"
			if args.verbose == True:
				print "Se produjo un error con el siguiente mensaje de error: "
				print "\n %s" % (e)
				break
				driver.quit()
				sys.exit(0)
			
		assert "Google" in driver.title
		for items in dork_list:
			elem = driver.find_element_by_name("q")
			elem.clear()
			elem.send_keys(items)
			elem.send_keys(Keys.RETURN)
			time.sleep(2.2)
			
			try:
				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "r")))
			except Exception as e:
				driver.quit()
				print "\n[" + t.red("!") + "]La detección de elementos de origen de página falló / se agotó el tiempo de espera\n"
				
				if args.verbose == True:
					print "Se produjo un error con el siguiente mensaje de error: "
					print "\n %s" % (e)
				
				time.sleep(1)
				continue	
				
				
			assert "No se han encontrado resultados" not in driver.page_source
			if "No se han encontrado resultados" in driver.page_source:
				continue

			links = driver.find_elements_by_xpath("//h3//a[@href]")
			for elem in links:
				link_list.append(elem.get_attribute("href"))
            
	driver.quit()
	return link_list

proc_one = search()

with open("results.log", "ab") as outfile:
	for item in proc_one:
		outfile.write("%s\n" % item)

if args.verbose == True:	
	with open("results.log", "r") as infile:
		for line in infile:
			print "[" + t.magenta("~") + "]" + line
		

print "\n\n[" + t.green("+") + "]Hecho. Los resultados se guardaron en un archivo de texto, en el directorio actual como %s para su posterior procesamiento.\n" % outfile
