Convertidor
===========


El convertidor permite transformar las letras a otros formatos más conocidos y utilizados.


-i   Nombre del archivo de entrada, en formato *Marke37*.
-o   Nombre del archivo de salida.
-f   Formato de conversión.
     Los valores permitidos son:

     * ``html`` - Es el formato predeterminado. Genera la letra con ``div`` y ``span``, listo para ser insertado dentro de una página web.
     * ``latex`` - General la letra con entornos LaTeX para rodear la letra y las secciones. Para que funcione, la plantilla de LaTeX debe definir las instrucciones usadas por el convertidor.
     * ``markdown`` o ``md`` - Reduce la sintaxis de *Marke37* a Markdown únicamente.
     * ``pagina`` - Envuelve el formato HTML en una página autocontenida.
     * ``pdf`` - Envuelve la salida en formato LaTeX en una plantilla autocontenida que al ser compilada genera el PDF.
     * ``im``, ``messenger``, o ``whatsapp`` - Utiliza la sintaxis de los servicios de mensajería instantánea, para poder compartir la letra de manera más presentable entre las amistades.
