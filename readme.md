#Proyecto para gestión de biblioteca.

**Para empezar**.

Para clonar el repositorio, basta con elegir la opción "Fork" arriba a la derecha.
Si no desea hacerlo así, puede 	dar click en el botón verde que dice "Code". Ahí le desplegará varias opciones:
*Copiar el url del repositorio para usarlo en un cliente, como github desktop.
*Abrir directamente github desktop para clonarlo.
*Descargar el código fuente en forma de archivo comprimido.
*Copiar un comando para clonarlo en un cli de consola.

Por el momento, SSH no se recomienda debido a requerimientos extras que esto puede tener.

Se recomienda el uso de un entorno virtual para que no haya conflicto con versiones de librerias locales.
Para ello, es recomendable instalar virtualenv.
En la consola, una vez teniendo abierta la carpeta del proyecto, escribir: pip install 'virtualenv'
Despues, para crear un entorno virtual, escribir virtualenv + el nombre que se desee para el entorno.
Ejemplo: virtualenv biblioteca_env
Una vez terminado, hay que acceder al entorno virtual, para ello se usa este comando:
./(nombre)/Scripts/activate *Ejemplo* ./biblioteca_env/Script/activate
Con esto activado, hay que correr el siguiente comando:
pip install -r requirements.txt
Esto instalará las dependencias de nuestra API.
Para inicializar la base de datos, se recomienda crear un archivo .env y dentro poner:
DATABASE_URL = '(url de base de datos)'
Para inicializar el servidor, basta con ejecutar: python server.py
Para las pruebas con las rutas de API, se recomienda Insomnia o Postman.
Nuestro servidor se ejecuta en el puerto '8080'.
Para hacer una solicitud, basta con elegir "Nueva solicitud" en el programa de nuestra elección,
entonces especificar la ruta. Para autores, es  http://localhost:8080/autores. Para libros, es:
http://127.0.0.1:8080/libros . Para un solo autor, es /autores/(id), donde id es un numero.
Para un solo libro, es /libros/(id), donde id es un numero.
Una vez hecho esto, si la ruta lo permite, en BODY se debe elegir JSON y enviar un JSON.
*Ejemplo*

*Ruta: http://127.0.0.1:8080/libros/1
*Body:
    {
	"titulo": "Juegos Subconsciente",
	"fecha_publicacion": "06-08-2019",
	"autor_id": 3
    }

Esto buscará el libro especificado y cambiará la información de este.