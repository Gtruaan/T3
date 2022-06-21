# Tarea 3: DCCasillas :checkered_flag: 


## Consideraciones generales :octocat:

La tarea... se ejecuta. Algo es algo. Puede manejar desconexiones de clientes en la sala de espera.
Esta tarea no la hice con tanto cariño como las otras y fue la que mas me tomo tiempo por la cantidad
gigante de errores que aparecian. No me siento para nada conforme con el resultado pero ya no tengo tiempo ni voluntad para seguir:(
Modele y defini las funciones de codificacion, decodificacion, encrypting y decrypting pero no pude usarlas en la tarea porque hubo
un error en la de decrypting que no supe arreglar.

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación:
- ❌ si **NO** complete lo pedido
- ✅ si complete **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

#### Networking: 23 pts (18%)
##### ✅ Protocolo: Uso TCP e IP para instanciar los sockets en ```Servidor\server.py```.
##### ✅ Sockets: Hago uso de los sockets con cuidado al manejar excepciones, y me aseguro de instanciarlos correctamente.
##### ✅ Conexión: Creo un modelo que recibe mensajes y escucha constantemente, y permite repartir mensajes entre todos los clientes
##### ✅ Manejo de clientes: Los clientes se comunican de forma concurrente con el servidor, y el servidor con los clientes
#### Arquitectura Cliente - Servidor: 31 pts (25%)
##### ✅ Roles: Todo se checkea, se revisa y se procesa en el servidor. Backend del cliente se encarga de enviar y bajar la informacion
##### ✅ Consistencia: La informacion se actualiza para todos los clientes simultaneamente. No es necesario usar locks debido a que no uso threading aca.
##### ✅ Logs: El servidor printea todo lo que ocurre con un simbolo asociado ([i], ( ! ), <#>)
#### Manejo de Bytes: 26 pts (21%)
##### ✅ Codificación: Defino la funcion codificacion en los archivos ```utils.py``` de cliente y servidor. Utiliza little endian y big endian cuando se pide, y separa el mensaje correctamente (hasta donde yo se)
##### 🟠 Decodificación: Tanbien esta definida en ```utils.py``` pero no la termine de probar. Revierte la codificacion. Recibe un mensaje en bloques de 26 y lo descompone.
##### ✅ Encriptación: La encriptacion esta definida en ```utils.py``` y se comporta tal como lo pide el enunciado. Se crea una funcion auxiliar ```cbs()``` que entrega la suma de los bytes centrales de una string de bytes
##### 🟠 Desencriptación: Trate de implementarla con un algoritmo que planee pero por alguna razon no funciona como deberia. Estoy seguro de que se trata de un booleano mal puesto. :( triste
##### 🟠 Integración: Obviamente no pude integrar el protocolo tal como se pedia en el enunciado debido a que no pude hacer funcionar la desencriptacion, asi que lo supli con una codificacion largo + mensaje
#### Interfaz: 23 pts (18%)
##### ✅ Ventana inicio: Funciona, muestra alertas y se ve bonita
##### ✅ Sala de Espera: Se actualiza para todos los usuarios. Si el administrador se sale, se le entrega el privilegio a alguien mas. La partida no se puede empezar sin MIN_JUGADORES jugadores y empieza automaticamente cuando hay MAX_JUGADORES jugadores
##### ✅ Sala de juego: Funciona y se actualiza correctamente
##### ❌ Ventana final: Se crashea y ni idea por que pero por ultimo abre
#### Reglas de DCCasillas: 18 pts (14%)
##### ✅ Inicio del juego: Todo chill de acuerdo al enunciado
##### ✅ Ronda: Todo se implementa tal como sale en la pauta
##### ✅ Termino del juego: No se ve pero se asigna correctamente al ganador. Esto se puede ver en los logs del servidor.
#### General: 4 pts (3%)
##### ✅ Parámetros (JSON): Defino una funcion ```params()``` en ```utils.py``` para cargar parametros JSON
#### Bonus: 5 décimas máximo
##### ❌ Cheatcode: Nop
##### ❌ Turnos con tiempo: No
##### ❌ Rebote: Nounounou

## Ejecución :computer:
En las carpetas Servidor y Cliente se deben ejecutar los main.py. El servidor va primero. La carpeta Sprites va en Cliente y no en Frontend.


## Librerías :books:
### Librerías externas utilizadas
Use PyQT5, Socket, Threading, random, sys y os

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```\Cliente\utils.py``` y ```\Servidor\utils.py```: Contiene metodos para leer parametros y codificar mensajes
2. ```\Servidor\board.py```: Contiene una clase que modela el tablero como estructura nodal. Es gigante
3. ...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Siempre he jugado Ludo Online y ahi es posible avanzar en las casillas de color siempre y cuando no se caiga en la casilla de victoria con un numero inexacto. La interaccion la lleve a cabo de esa forma.

PD: xfa piedad


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. La AF3 para basar el modelamiento basico de las clases cliente y servidor
2. Documentacion de pyQt5


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).

