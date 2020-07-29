# BirdBOT
Código fuente de un bot de Discord escrito en Python con comandos utiles y curiosos para un grupos de jugadores.

---

## Dependencias
* ffmpeg
* python 3.7+
* virtualenv (recomendado)
* discord.py
* requests
* bs4
* lxml
* PyNaCl


## Descarga e instalación
* Instalar [_ffmpeg_](https://ffmpeg.org/download.html)

* Instalar [_virtualenv_](https://pypi.org/project/virtualenv/)

* Ejecutar en bash: 
    ```bash
    $ git clone https://github.com/jddma/BirdBOT.git
    $ cd BirdBOT/
    $ virtualenv venv --python=python3.7
    
    # GNU Linux / macOS
    $ source venv/bin/activate
    
    # Windows
    $ cd venv/Scripts/
    $ activate.bat
    
    (venv)$ pip3 install -r requirements.txt
    ```

## Configuración

* En el directorio _resources/sounds/_ colocar los ficheros _.mp3_ con los sonidos a implementar.

* En el directorio _resources/_ crear un fichero _global_vars.json_ con el siguiente contenido, donde la posición "sounds" sea un diccionario cuyas claves sean el argumento que se le pasara al comando _sound_ para reproducir el fichero _.mp3_, cuyo nombre debera ser indicado en los valores de diccionario. 
    ```file
    {
        "prefix": "//",
        "token": "bot token",
        "sounds": {
            "sound_argument": "sound_file_name",
            ... ,
            ... ,
            ... ,
        }
    }
    ```

## Licencia
BirdBOT esta bajo la licencia GNU General Public License v3.0, Leer el archivo [LICENSE](https://github.com/jddma/BirdBOT/blob/master/LICENSE) para mas información.