#!/bin/bash

# Coloring scheme for notfications and logo
ESC="\x1b["
RESET=$ESC"39;49;00m"
CYAN=$ESC"33;36m"
RED=$ESC"31;01m"
GREEN=$ESC"32;01m"

# Warning
function warning() 
{	echo -e "\n$RED [!] $1 $RESET\n"
	}

# Green notification
function notification() 
{	echo -e "\n$GREEN [+] $1 $RESET\n"
	}

# Cyan notification
function notification_b() 
{	echo -e "\n$CYAN [-] $1 $RESET\n"
	}

function get_gdriver() 
{	printf "\n\n"
	MACHINE_TYPE=`uname -m`
	if [[ ${MACHINE_TYPE} == 'x86_64' ]]; then
		notification "x86_64 architecture detected..."
		sleep 1

		wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
		tar -xvf geckodriver-v0.18.0-linux64.tar.gz
		rm geckodriver-v0.18.0-linux64.tar.gz
		chmod +x geckodriver
		mv geckodriver /usr/sbin
		sudo ln -s /usr/sbin/geckodriver /usr/bin/geckodriver

		notification "Geckodriver se ha instalado con éxito"
	else
		notification "arquitectura x32 detectada ..."
		sleep 1
		wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux32.tar.gz
		tar -xvf geckodriver-v0.18.0-linux32.tar.gz
		rm geckodriver-v0.18.0-linux32.tar.gz 
		chmod +x geckodriver 
		mv geckodriver /usr/sbin 
		sudo ln -s /usr/sbin/geckodriver /usr/bin/geckodriver
		notification "Geckodriver ha sido instalado con éxito."
	fi
	}


if [[ "$EUID" -ne 0 ]]; then
    warning "Este script debe ejecutarse como root"
    exit 1
else
    clear && sleep 0.5
    notification_b "Este script instalará Mozilla Geckodriver, del cual JORY depende."
    printf "%bDespués de que esta operación se haya completado, la secuencia de comandos también puede instalar"
    printf "%b\ las dependencias del archivo de requisitos si lo prefiere\n\n"
    
    read -p 'Instalar archivo de requisitos después de la instalación de Geckodriver? Y/n : ' choice
    if [[ $choice == 'y' || $choice == 'Y' ]]; then
        notification "Instalación de Geckodriver y archivo de requisitos." && sleep 2
        get_gdriver && sleep 2
        
        clear
        notification "Instalar archivo de requisitos."
        
        sudo -H pip install -r requirements.txt
        
        notification "Todas las operaciones completadas"
        exit 0
      
        
    else
        notification "Instalando Geckodriver." && sleep 2
        get_gdriver && sleep 2
        
        notification "Todas las operaciones completadas"
        exit 0
    fi 
fi	
