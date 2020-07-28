# BirdBOT
Código fuente de un bot de Discord escrito en Python con comandos utiles y curiosos para un grupos de jugadores.

---

## Dependencias
* python 3.7+
* virtualenv (recomendado)
* discord.py
* requests
* bs4
* lxml

## Descarga e instalación
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
En el directorio _resources/_ crear un archivo global_vars.json con el siguiente contenido 
```file
{
    "prefix": "//",
    "token": "bot token"
}
```

## Licencia
BirdBOT esta bajo la licencia GNU General Public License v3.0, Leer el archivo [LICENSE](https://github.com/jddma/BirdBOT/blob/master/LICENSE) para mas información.