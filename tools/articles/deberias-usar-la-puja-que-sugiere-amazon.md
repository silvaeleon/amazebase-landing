title:        ¿Deberías usar la puja que sugiere Amazon?
slug:         deberias-usar-la-puja-que-sugiere-amazon
translation_of: amazon-suggested-bid-and-down-only
summary:      La puja sugerida de Amazon te dice lo que pagan otros anunciantes. Tus propios costos y tu tasa de conversión de anuncios te dicen lo que puedes pagar tú.
categories:   PPC & Advertising
hero_alt:     Un vendedor compara la puja sugerida de Amazon con su propio techo calculado
reading_time: 7

Cuando agregas una palabra clave a una campaña de Sponsored Products, Amazon muestra un número junto a ella y lo llama puja sugerida. La mayoría de los vendedores nuevos la usa, porque la pantalla no ofrece otra alternativa.

Es una lectura del mercado: aproximadamente lo que otros anunciantes han pagado por esa palabra clave. No sabe nada de tu precio de venta, de tus tarifas, de tu costo puesto en destino ni de con qué frecuencia los clics de tus anuncios se convierten en pedidos, y son esas cosas las que deciden cuánto vale un clic para ti.

## Qué encontrarás en esta guía

- Qué representan la puja sugerida y su rango
- Lo máximo que puedes pagar por un clic
- Qué le hacen a tu puja las tres configuraciones de puja
- Por qué muchos anunciantes prefieren down only mientras aprenden
- Los ajustes por ubicación, y por qué se fijan por campaña
- Cómo probar cuánto cuesta de verdad un clic
- Qué controla tu puja y qué no

## ¿Qué es la puja sugerida y qué te está diciendo?

Aparece en la consola de publicidad. A medida que agregas palabras clave u objetivos de producto a una campaña en Campaign Manager, Amazon muestra una puja sugerida junto a cada uno, más un rango de puja sugerida con un extremo bajo y un extremo alto.

Amazon describe estas recomendaciones como el resultado de analizar un grupo de pujas ganadoras de anuncios recientes y similares dentro de tu categoría, que se actualiza a medida que cambian las pujas de la competencia. Resumen lo que otros pagaron; no pronostican lo que vas a pagar tú.

[[La distinción]]
La puja sugerida lee el mercado, no tu negocio. Todos los datos que deciden si vale la pena comprar un clic están ausentes de ella. Dos vendedores que ven la misma sugerencia de $1.35 pueden tener razón al pujar $2.00 y $0.40.

[[La trampa]]
Cuando una palabra clave no recibe impresiones, el rango te invita a saltar a su extremo alto y dejar de pensar. Entonces pagas un precio que nunca contrastaste con tus propios números.

## ¿Cuánto puedes pagar por un clic?

Empieza por la contribución por unidad: lo que deja una venta después de todos los costos excepto la publicidad. Para un producto importado, es el precio de venta menos la tarifa por referencia, la tarifa de gestión logística de FBA y el costo puesto en destino de la unidad.

Precio de venta | $30.00
Tarifa por referencia al 15% | $4.50
Tarifa de gestión logística de FBA | $5.80
Costo puesto en destino por unidad, producto importado | $7.20
Contribución por unidad antes de la inversión publicitaria | $12.50

Esos $12.50 son todo el presupuesto de publicidad que te da una venta. Tu tasa de conversión de anuncios es la proporción de clics de anuncios que se convierten en pedidos atribuidos al anuncio. Con 8%, una venta requiere 12.5 clics, porque 1 dividido entre 0.08 es 12.5.

[[Ejemplo práctico]]
Contribución por unidad | $12.50
Tasa de conversión de anuncios | 8%
Clics por venta, 1 dividido entre 0.08 | 12.5
Costo por clic de equilibrio, $12.50 multiplicado por 8% | $1.00
ACOS de equilibrio, $12.50 dividido entre $30.00 | 41.7%

Con $1.00 no te quedas con nada, así que el equilibrio no es tu techo; es la pared que hay detrás. Si la publicidad puede llevarse la mitad de la contribución, tu techo es $0.50 por clic: $6.25 de inversión publicitaria por venta y $6.25 de utilidad.

[[La regla]]
Lo máximo que puedes pagar por un clic es la contribución por unidad multiplicada por la tasa de conversión de anuncios. Todos los datos son tuyos, y ninguno aparece donde aparece la puja sugerida.

Si en cambio pagas la sugerencia de $1.35, una venta cuesta $1.35 multiplicado por 12.5 clics, o sea $16.88 contra $12.50 de contribución: una pérdida de $4.38 por unidad.

Toma tu tasa de conversión de anuncios de Campaign Manager: clics y pedidos atribuidos al anuncio para el ASIN durante al menos 30 días, el segundo dividido entre el primero. No uses unit session percentage de Business Reports de Seller Central, que cuenta también las sesiones orgánicas y describe tu listing, no tus anuncios.

[[El riesgo]]
Un producto nuevo no tiene una tasa de conversión de anuncios medida, y suponer una demasiado alta infla tu techo. Los productos con pocas reseñas suelen convertir peor, así que planifica bajo y reemplaza el supuesto cuando tengas unos cuantos cientos de clics.

## ¿Qué le hacen a tu puja las tres configuraciones de puja?

La estrategia de puja es una configuración de la campaña. Decide qué puede hacer Amazon con tu puja antes de que entre a una subasta.

| Configuración | Qué hace Amazon con la puja que ingresaste | ¿Puede subir esa puja? |
|---|---|---|
| Dynamic bids - down only (pujas dinámicas, solo hacia abajo) | La baja en las subastas que considera menos probables de convertir | No |
| Dynamic bids - up and down (pujas dinámicas, hacia arriba y hacia abajo) | La sube en las subastas que considera más probables de convertir, y la baja en el resto | Sí — Amazon indica que hasta 100%, para todas las ubicaciones |
| Fixed bids (pujas fijas) | Usa exactamente la puja que ingresaste | No |

El límite que Amazon publica para up and down es el 100% de esa tabla. Por eso una puja de $0.50 puede competir hasta en $1.00 — el precio de equilibrio de arriba, y el doble del techo que fijaste.

Bajo las tres, todavía se puede aplicar encima un ajuste por ubicación: una configuración de campaña aparte, que se explica más abajo.

[[FIGURE: Una misma puja ingresada convertida en tres pujas de subasta distintas bajo las tres configuraciones]]

## ¿Por qué muchos anunciantes prefieren down only mientras aprenden?

Porque elimina una incógnita. Con up and down, lo que pagaste por un clic resulta de dos cosas que no puedes ver: lo que exigió la subasta, y cuánto subió Amazon tu puja. Cuando el costo vuelve más alto de lo esperado, no puedes saber cuál de las dos lo causó.

[[Por qué]]
Con down only, la puja que entra a la subasta nunca es mayor que el número que escribiste, antes de cualquier ajuste por ubicación, así que la puja que fijaste y el costo que observaste son comparables. Mientras aprendes, esa lectura más limpia suele valer más que las impresiones que up and down podría ganar. Es una preferencia, no una ley: down only sí deja escapar algunas ventas que se podían ganar.

## ¿Qué son los ajustes por ubicación y por qué se fijan por campaña?

Los anuncios de Sponsored Products aparecen en tres tipos de posición. La parte superior de la búsqueda (primera página) es la fila de resultados patrocinados por encima de los resultados orgánicos en la primera página de una búsqueda. El resto de la búsqueda es cualquier otra posición patrocinada dentro de los resultados de búsqueda. Las páginas de producto son los espacios patrocinados de una página de detalle.

Amazon permite un ajuste de hasta 900% en cada una, para todos los tipos de segmentación y todas las estrategias de puja. Multiplica la puja que ingresaste, solo para esa ubicación.

Puja que ingresaste | $0.50
Ajuste de la parte superior de la búsqueda | 50%
Puja que compite en la parte superior de la búsqueda, $0.50 multiplicado por 1.50 | $0.75
Puja que compite en todas las demás ubicaciones | $0.50

Ahora la campaña compite a $0.75 en una ubicación, por encima del techo que fijaste. Eso puede ser deliberado, pero solo si tú lo elegiste.

[[El límite]]
El ajuste pertenece a la campaña, no a la palabra clave: una campaña, un juego de tres porcentajes, aplicado a todas las palabras clave que contiene. Una campaña con veinte palabras clave no puede darle a ninguna de ellas su propia estrategia de ubicaciones. Ese es el argumento práctico más fuerte a favor de pocas palabras clave por campaña.

Lee el informe de ubicaciones de Amazon para Sponsored Products antes de fijar un ajuste.

## ¿Cómo pruebas cuánto cuesta de verdad un clic?

A veces una palabra clave devuelve casi ninguna impresión, y esperar no ayuda: una puja por debajo del nivel al que cierra la subasta no recoge datos. La única forma de conocer el precio de entrada es subir la puja y observar.

[[Qué hacer]]
1. Anota la fecha, la palabra clave y la puja desde la que estás cambiando.
2. Pon esa campaña en down only o en fixed bids, para que el costo que observes corresponda a la puja que fijaste.
3. Limita lo que la prueba puede gastar, con el presupuesto diario y una fecha de término.
4. Sube la puja en un solo paso, no en varios repartidos a lo largo de semanas.
5. Al final, lee el costo por clic promedio que Amazon reporta para esa palabra clave, devuelve la puja a tu techo y marca las fechas de la prueba en tus notas.

Marcar las fechas protege tus datos: la prueba infla el costo por clic y el ACOS a propósito, y la puja subida puede ganar clics en ubicaciones que normalmente no alcanzas, así que la tasa de conversión de esa ventana no es la tuya normal.

[[La trampa]]
Las ventas suelen subir durante la prueba, porque una puja más alta compra más clics. Eso no es evidencia de que sea asequible: los clics por encima de tu techo producen más ventas y menos utilidad al mismo tiempo.

## ¿Qué controla en realidad tu puja?

Una puja es lo máximo que estás dispuesto a pagar por un clic: un límite que fijas tú, no un precio que acordaste. Influye en si entras a la subasta y en con qué frecuencia ganas. Amazon es explícito en que no es el único factor, porque la relevancia de tu anuncio para la búsqueda del comprador también decide si aparece.

[[La confusión]]
Tu puja no fija tu costo por clic. Lo fija la subasta, que está hecha de las pujas de otros anunciantes, que cambian a diario y no tienen nada que ver con tu margen. Subir una puja de $0.90 a $1.20 no compra un clic de $1.20; compra el permiso de que te cobren hasta esa cifra.

Así que juzga una palabra clave por el costo por clic que Amazon reporta — la inversión dividida entre los clics — nunca por la puja que escribiste.

## Preguntas frecuentes

**Mi puja era de $0.90 y mi costo por clic reportado es de $1.60. ¿Cómo?**
Revisa la estrategia de puja, ya que up and down puede subir una puja hasta 100%. Después, los ajustes por ubicación de la campaña, que aplican bajo cualquier estrategia, down only incluida. Y la cifra reportada es un promedio de los clics del periodo, no el precio de un clic.

**¿Y si mi techo queda por debajo de la puja sugerida?**
Entonces es probable que hoy esa palabra clave no esté a tu alcance. Tres cosas mueven un techo: un precio de venta más alto, costos más bajos y una mejor tasa de conversión de anuncios.

## Para cerrar

La puja sugerida te dice, rápido y gratis, aproximadamente lo que una palabra clave le cuesta a otras personas. No te puede decir si ese es un precio que deberías pagar.

Hay una forma de seguir esta guía al pie de la letra y aun así perder dinero. Un techo está tan al día como los dos números que lo sostienen, así que si tu tasa de conversión de anuncios baja, o si tus tarifas o tu costo puesto en destino suben, el techo del trimestre pasado hoy es demasiado alto. Recalcúlalo por producto cada vez que se muevan el precio, los costos o la tasa de conversión.

Cifras de los ejemplos trabajados de este artículo, no de un estudio de mercado.

## New terms

- puja sugerida — el importe que Amazon muestra junto a una palabra clave o un objetivo de producto cuando lo agregas a una campaña de Sponsored Products, tomado de pujas ganadoras recientes de otros anunciantes. Frase del día a día: lo que otros anunciantes han venido pagando. Es una recomendación: no debe traducirse de una forma que suene a instrucción ni a requisito.
- rango de puja sugerida — la banda de mínimo a máximo que Amazon muestra junto a la puja sugerida. Frase del día a día: el abanico de lo que otros anunciantes han venido pagando.
- estrategia de puja — la configuración de campaña que decide si Amazon puede cambiar la puja que ingresaste antes de que entre a una subasta. Frase del día a día: si Amazon puede ajustar tu puja sola.
- Dynamic bids - down only / Dynamic bids - up and down / Fixed bids — los tres valores de esa configuración, tal como aparecen en la consola de publicidad. Se dejan en inglés y se glosan una sola vez, en la tabla de la sección correspondiente, para que el lector pueda emparejar el texto con la pantalla. En el resto del artículo se usan las formas cortas down only, up and down y fixed bids, también en inglés.
- ajuste por ubicación — un porcentaje que multiplica tu puja solo para una ubicación, fijado en la campaña. Frase del día a día: pagar más o menos según dónde aparezca el anuncio.
- ubicación — NUEVO en el glosario ES. Es el «placement» del inglés; el portugués ya tiene «posicionamento» (§3 PT). Se elige «ubicación» porque es la palabra que usa la consola de Amazon en español. Propuesta: añadirla a GLOSARIO-ES §3.
- parte superior de la búsqueda (primera página) / resto de la búsqueda / páginas de producto — las tres ubicaciones que Amazon deja ajustar por separado. Frases del día a día: la fila patrocinada sobre la primera página de resultados; las posiciones patrocinadas del resto de la búsqueda; los espacios patrocinados de una página de detalle.
- contribución por unidad — lo que queda de una venta después de todos los costos excepto la publicidad. Frase del día a día: el dinero que una venta te deja para anuncios y utilidad. Se mantiene distinta de «margen», que aquí nunca se usa como sustituto.
- costo por clic de equilibrio — el costo por clic al que la publicidad se come toda la contribución por unidad y la utilidad es cero. Frase del día a día: el precio de clic donde dejas de ganar.
- techo — lo máximo que un clic puede valer para el lector, calculado como contribución por unidad multiplicada por tasa de conversión de anuncios y fijado por debajo del equilibrio para dejar utilidad. Frase del día a día: la puja más alta que te permites. NUEVO en el glosario ES.
- tasa de conversión de anuncios — ya está en GLOSARIO-ES §3 (añadida 2026-09-12). Pedidos atribuidos al anuncio divididos entre los clics, tomados de Campaign Manager. Este artículo se apoya mucho en ella, porque sin ella no se puede calcular el techo. Debe seguir siendo distinta de la tasa de conversión del listing.
- pedido atribuido al anuncio — ya está en GLOSARIO-ES §3. Sin cambios.
- unit session percentage — se deja en inglés (§2). Aparece SOLO como la métrica que el lector NO debe usar para una decisión de publicidad, así que el contraste con la tasa de conversión de anuncios tiene que sobrevivir a la traducción.
- tarifa por referencia — el porcentaje del precio de venta que se queda Amazon en cada venta. Frase del día a día: la comisión de Amazon. NUEVO en el glosario ES; es la forma que usa Seller Central en español. NECESITA VISTO BUENO.
- tarifa de gestión logística de FBA — la tarifa por unidad que cobra Amazon por preparar y enviar un pedido de FBA. NUEVO en el glosario ES. NECESITA VISTO BUENO: en la práctica muchos vendedores dicen «tarifa de FBA» a secas.
- objetivo de producto — lo que el inglés llama «product target»: el ASIN o la categoría a la que apuntas en una campaña. NUEVO en el glosario ES.
- No hizo falta ninguna etiqueta de callout nueva. Todas las usadas tienen precedente medido en el corpus español: La distinción, La trampa, Ejemplo práctico, La regla, El riesgo, Por qué, El límite, Qué hacer, La confusión.
