Lenguaje de marcado
=========================

¿Qué es lo que se puede hacer con el lenguaje de marcado *Marke37*?

En este documento se detallan las dos grandes categorías de lo que se puede hacer:

#. Estilizar cada una de las secciones de una letra.
#. Agregar algunos efectos a la voz, o voces, durante la interpretación.



Secciones
---------



Título
~~~~~~

El título se busca una sola vez en el documento. Se denota con una línea de símbolos de igual debajo del texto del título, así:

.. code-block:: me37

	El título es este
	=================



Verso
~~~~~

En realidad, el verso no necesita especificación o símbolo alguno. Cualquier párrafo delimitado por saltos de línea cuenta como un verso:

.. code-block:: me37

    Este es un verso
    Compuesto de cuatro líneas
    Aunque debe tener rimas
    De lo contrario, es incorrecto

Bajo esa definición, lo siguiente son dos versos:

.. code-block:: me37

	Este es un verso
	Hay una línea vacía antes de él

	Y este es otro verso
	Pues hay salto de línea aquí también


Coro
~~~~

El coro se delimita por dos signos de estrella (``**``), al inicio y al final de la sección. Sí, como las negritas en Markdown convencional.

.. code-block:: me37

	**Las estrellas delimitan el coro
	Van al inicio y al final de todo
	No en cada línea
	Sería enfadoso**



Puente
~~~~~~

El puente se delimita mediante un guión bajo (``_``):

.. code-block:: me37

	_Este es el puente
	Se ve un poco diferente_



Intro
~~~~~

El intro se utiliza combinando los símbolos de coro y puente, como ``_**`` para la apertura, y ``**_`` para la clausura:

.. code-block:: me37

	_**Esta es la intro
	Que tiene otro estilo**_



Outro
~~~~~

Usa los mismos símbolos que el intro, pero en diferente orden:

.. code-block:: me37

	**_Los símbolos tienen diferente orden
	Espero no sea motivo de errores_**



Precoro
~~~~~~~

El precoro, una sección que puede estar presente antes del coro, se denota por dos almohadillas o signos de gato (`#`).

.. code-block:: me37

	##Este es el precoro
	Y va antes que el coro##



Postcoro
~~~~~~~~

También podemos poner una sección después del coro, llamada post coro, que se denota mediante dos signos de pesos (``$``):

.. code-block:: me37

	$$Este es el postcoro
	Y va después que el coro$$



Voces
-----



De manera predeterminada, se utiliza una voz en cada letra, y se asume que no cambia a lo largo de la canción.

No obstante, se pueden agregar ciertos *efectos* (por decirlo de alguna manera) a través de caracteres especiales.



Gritos
~~~~~~

¿Qué sería una canción de rock o metal sin unos buenos gritos guturales? Para indicar esto, si se desea, se puede encerrar la letra pertinente entre barras verticales (``|``):

.. code-block:: me37

	Este es un verso
	No hay nada siniestro
	Hasta que llega un |grito| y nada
	Vuelve a ser igual



Segunda voz
~~~~~~~~~~~

La segunda voz se logra encerrando el texto deseado entre corchetes (``[`` y ``]``).

.. code-block:: me37

	**[Este es un coro
	Pero con segunda voz
	Lo dicen los corchetes
	No lo digo yo]**

De manera predetermina, el tema coloca esto en color rosa oscuro, para denotar que es una voz femenina.



Tercera voz
~~~~~~~~~~~

En caso de necesitar aún otra voz, encerrar el texto entre llaves (``{`` y ``}``).

.. code-block:: me37

	_{Esto es el puente
	Hecho por otra voz
	Tantas combinaciones
	Ya son un crimen atroz}_



Otras amenidades
----------------



Comentarios
~~~~~~~~~~~

Los comentarios empiezan con un signo de porcentaje:

.. code-block:: me37

	% Esta línea es un comentario.
	Esta ya no.

También pueden aparecer al final de la línea:

.. code-block:: me37

	Esto no es comentario % pero todo esto sí.

