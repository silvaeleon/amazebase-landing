# -*- coding: utf-8 -*-
"""Spanish mirror of articles/reorder-point.html"""

EN_PATH = "/articles/reorder-point.html"
ES_PATH = "/es/articulos/punto-de-reorden.html"

META = dict(
    title="Punto de reorden en Amazon: la f&oacute;rmula simple que todo vendedor deber&iacute;a conocer",
    desc="Una f&oacute;rmula pr&aacute;ctica de punto de reorden para vendedores de Amazon &mdash; ventas diarias promedio, tiempo total de reposici&oacute;n, stock de seguridad &mdash; m&aacute;s las cinco m&eacute;tricas que debes revisar cada semana y las se&ntilde;ales de alerta que nunca deber&iacute;as ignorar.",
    og_title="Punto de reorden en Amazon: la f&oacute;rmula simple que todo vendedor deber&iacute;a conocer",
    og_desc="La mayor&iacute;a de los quiebres de stock no empiezan cuando te quedas sin inventario. Empiezan semanas antes, cuando dejas pasar el momento de colocar la siguiente orden. Esta es la f&oacute;rmula que lo detecta.",
    headline="Punto de reorden en Amazon: la f\\u00f3rmula simple que todo vendedor deber\\u00eda conocer",
    ld_desc="La mayor\\u00eda de los quiebres de stock empiezan semanas antes de quedarte sin inventario, en el momento en que dejas pasar la siguiente orden. La f\\u00f3rmula del punto de reorden, las cinco m\\u00e9tricas semanales y las se\\u00f1ales de alerta que nunca deber\\u00edas ignorar.",
    breadcrumb="Punto de reorden en Amazon: la f\\u00f3rmula simple que todo vendedor deber\\u00eda conocer",
    keywords=["Punto de reorden", "Planificaci\\u00f3n de reposici\\u00f3n",
              "Stock de seguridad", "Tiempo de reposici\\u00f3n", "D\\u00edas de cobertura"],
)

BODY = u'''<div class="wrap">

<p class="back-link"><a href="/resources.html?lang=es">&larr; Centro de Conocimiento</a></p>

<header class="article-head">
  <p class="eyebrow">Planificaci&oacute;n de inventario</p>

  <h1>Punto de reorden en Amazon: <span class="accent">la f&oacute;rmula simple que todo vendedor deber&iacute;a conocer</span></h1>

  <p class="deck">
    La mayor&iacute;a de los problemas de inventario en Amazon no empiezan cuando te
    quedas sin stock. Empiezan semanas antes, cuando dejas pasar el momento justo
    para colocar tu siguiente orden de compra. No necesitas un software de
    pron&oacute;stico para detectarlo: necesitas unos pocos n&uacute;meros y la
    disciplina de revisarlos.
  </p>

  <p class="meta">
    <span>AmazeBase</span>
    <span class="dot" aria-hidden="true"></span>
    <span><time datetime="2026-07-14">14 de julio de 2026</time></span>
    <span class="dot" aria-hidden="true"></span>
    <span>5 min de lectura</span>
    <span class="dot" aria-hidden="true"></span>
    <span>Inventario y flujo de caja</span>
  </p>
</header>

<figure class="hero-shot">
  <img src="/assets/img/hero-reorder-point.webp"
       alt="Una fila azul de cajas de inventario que avanza por una carretera elevada y termina de golpe al borde de un acantilado; las cajas restantes aparecen solo como estructuras de alambre"
       width="1672" height="941" loading="eager" decoding="async">
</figure>

<div class="shell">

<main id="main" class="article">

  <p class="lead">
    La buena noticia es que no necesitas un software de pron&oacute;stico complejo
    para saber cu&aacute;ndo toca reponer. Unos pocos n&uacute;meros clave &mdash; y la
    disciplina de revisarlos con regularidad &mdash; te pueden ahorrar quiebres de
    stock caros y sobrestock innecesario.
  </p>

  <p>Este es un marco pr&aacute;ctico que puedes empezar a usar hoy mismo.</p>

  <nav class="toc" aria-labelledby="toc-title">
    <h2 id="toc-title">Qu&eacute; encontrar&aacute;s en esta gu&iacute;a</h2>
    <ol>
      <li><a href="#s1">Conoce tus ventas diarias promedio</a></li>
      <li><a href="#s2">Calcula tu tiempo total de reposici&oacute;n</a></li>
      <li><a href="#s3">Calcula tu punto de reorden</a></li>
      <li><a href="#s4">Estima tu stock de seguridad</a></li>
      <li><a href="#metrics">Cinco m&eacute;tricas para revisar cada semana</a></li>
      <li><a href="#warnings">Tres se&ntilde;ales de alerta que nunca debes ignorar</a></li>
      <li><a href="#routine">Una rutina semanal simple</a></li>
    </ol>
  </nav>

  <hr class="rule">

<section class="step">
  <h2 id="s1"><span class="num">Paso 01</span>Conoce tus ventas diarias promedio</h2>

  <p>El primer n&uacute;mero que necesitas es tu velocidad de ventas actual. La f&oacute;rmula es simple:</p>

  <p class="formula"><span class="k">Ventas diarias promedio</span> <span class="op">=</span> <span class="k">unidades vendidas</span> <span class="op">&divide;</span> <span class="k">n&uacute;mero de d&iacute;as</span></p>

  <p><strong>Ejemplo.</strong> Unidades vendidas en los &uacute;ltimos 30 d&iacute;as: 1,200. D&iacute;as: 30.</p>

  <ul class="figures">
    <li><div class="fig is-real"><span class="v">40/d&iacute;a</span><span class="k">1,200 &divide; 30</span></div></li>
  </ul>

  <div class="fixbox">
    <span class="fixbox-k">Qu&eacute; hacer</span>
    <p>Si tus ventas est&aacute;n creciendo r&aacute;pido, no te apoyes en un promedio de 90 d&iacute;as. Usa los &uacute;ltimos 30 d&iacute;as &mdash; o incluso las &uacute;ltimas dos semanas &mdash; para reflejar mejor la demanda actual.</p>
  </div>
</section>

<section class="step">
  <h2 id="s2"><span class="num">Paso 02</span>Calcula tu tiempo total de reposici&oacute;n</h2>

  <p>Muchos vendedores solo cuentan el tiempo de fabricaci&oacute;n. En vez de eso, suma cada etapa del proceso.</p>

  <table class="ltable">
    <thead>
      <tr><th scope="col">Etapa</th><th scope="col">D&iacute;as</th></tr>
    </thead>
    <tbody>
      <tr><td>Fabricaci&oacute;n</td><td>20</td></tr>
      <tr><td>Preparaci&oacute;n del proveedor</td><td>5</td></tr>
      <tr><td>Flete mar&iacute;timo</td><td>28</td></tr>
      <tr><td>Aduana</td><td>7</td></tr>
      <tr><td>Transporte terrestre</td><td>3</td></tr>
      <tr><td>Recepci&oacute;n en Amazon</td><td>6</td></tr>
      <tr><td>Tiempo total de reposici&oacute;n</td><td>69</td></tr>
    </tbody>
  </table>

  <div class="fixbox">
    <span class="fixbox-k">Qu&eacute; hacer</span>
    <p>Este es el n&uacute;mero que importa, no el que te dice tu proveedor.</p>
  </div>
</section>

<section class="step">
  <h2 id="s3"><span class="num">Paso 03</span>Calcula tu punto de reorden</h2>

  <p>Ahora combina esos dos n&uacute;meros.</p>

  <p class="formula"><span class="k">Punto de reorden</span> <span class="op">=</span> <span class="k">ventas diarias promedio</span> <span class="op">&times;</span> <span class="k">tiempo de reposici&oacute;n</span> <span class="op">+</span> <span class="k">stock de seguridad</span></p>

  <ul class="figures">
    <li><div class="fig"><span class="v">40</span><span class="k">Ventas diarias</span></div></li>
    <li><div class="fig"><span class="v">69</span><span class="k">Reposici&oacute;n (d&iacute;as)</span></div></li>
    <li><div class="fig"><span class="v">400</span><span class="k">Stock de seguridad</span></div></li>
    <li><div class="fig is-real"><span class="v">3,160</span><span class="k">Punto de reorden</span></div></li>
  </ul>

  <div class="fixbox">
    <span class="fixbox-k">Qu&eacute; hacer</span>
    <p>Cuando tu inventario disponible baje a 3,160 unidades, es momento de colocar la siguiente orden.</p>
  </div>
</section>

<section class="step">
  <h2 id="s4"><span class="num">Paso 04</span>Estima tu stock de seguridad</h2>

  <p>Un buen punto de partida es mantener inventario suficiente para cubrir retrasos inesperados.</p>

  <p class="formula"><span class="k">Stock de seguridad</span> <span class="op">=</span> <span class="k">ventas diarias promedio</span> <span class="op">&times;</span> <span class="k">d&iacute;as extra de protecci&oacute;n</span></p>

  <p>Si quieres protecci&oacute;n para 10 d&iacute;as adicionales: <strong>40 &times; 10 = 400 unidades</strong>.</p>

  <div class="fixbox">
    <span class="fixbox-k">Qu&eacute; hacer</span>
    <p>Si tu cadena de suministro es muy impredecible, quiz&aacute;s necesites 20 o 30 d&iacute;as de protecci&oacute;n en lugar de 10.</p>
  </div>
</section>

  <hr class="rule">

  <h2 id="metrics">Cinco m&eacute;tricas que deber&iacute;as revisar cada semana</h2>

  <p>Pronosticar no es solo cuesti&oacute;n de f&oacute;rmulas. Tambi&eacute;n es detectar las se&ntilde;ales de alerta a tiempo.</p>

<section class="metric">
  <h3><span class="num">1</span>D&iacute;as de cobertura</h3>
  <p>Preg&uacute;ntate: &laquo;Si vendiera al ritmo actual, &iquest;cu&aacute;ntos d&iacute;as me durar&iacute;a el inventario?&raquo;</p>
  <p class="formula"><span class="k">D&iacute;as de cobertura</span> <span class="op">=</span> <span class="k">inventario disponible</span> <span class="op">&divide;</span> <span class="k">ventas diarias promedio</span></p>
  <ul class="figures">
    <li><div class="fig"><span class="v">2,000</span><span class="k">Inventario</span></div></li>
    <li><div class="fig"><span class="v">40/d&iacute;a</span><span class="k">Ventas</span></div></li>
    <li><div class="fig is-bad"><span class="v">50 d&iacute;as</span><span class="k">D&iacute;as de cobertura</span></div></li>
  </ul>
  <div class="fixbox">
    <span class="fixbox-k">Qu&eacute; hacer</span>
    <p>Si tu tiempo de reposici&oacute;n es de 69 d&iacute;as y tienes 50 d&iacute;as de cobertura, ya est&aacute;s en problemas.</p>
  </div>
</section>

<section class="metric">
  <h3><span class="num">2</span>Tendencia del inventario</h3>
  <p>No mires solo el inventario de hoy: compara semana contra semana. Si tus d&iacute;as de cobertura fueron 90, luego 80, luego 70, luego 60, luego 50&hellip;</p>
  <div class="fixbox">
    <span class="fixbox-k">Qu&eacute; hacer</span>
    <p>Te est&aacute;s acercando a tu punto de reorden mucho m&aacute;s r&aacute;pido de lo que crees.</p>
  </div>
</section>

<section class="metric">
  <h3><span class="num">3</span>Velocidad de ventas</h3>
  <p>&iquest;Cambi&oacute; tu ritmo de ventas diarias? Compara los &uacute;ltimos 7 d&iacute;as contra los &uacute;ltimos 30.</p>
  <div class="fixbox">
    <span class="fixbox-k">Qu&eacute; hacer</span>
    <p>Si est&aacute;s vendiendo 25&nbsp;% m&aacute;s r&aacute;pido que tu promedio mensual, tu pron&oacute;stico probablemente necesita una actualizaci&oacute;n.</p>
  </div>
</section>

<section class="metric">
  <h3><span class="num">4</span>Inventario en tr&aacute;nsito</h3>
  <p>El inventario que va en el barco no es inventario que puedas vender. Separa siempre el inventario disponible, el reservado y el que est&aacute; en tr&aacute;nsito.</p>
  <div class="fixbox">
    <span class="fixbox-k">Qu&eacute; hacer</span>
    <p>Muchos vendedores asumen que las unidades en tr&aacute;nsito llegar&aacute;n exactamente cuando estaba planeado. Amazon suele tener otros planes.</p>
  </div>
</section>

<section class="metric">
  <h3><span class="num">5</span>Semanas de cobertura despu&eacute;s de que llegue tu env&iacute;o</h3>
  <p>Antes de colocar una orden, preg&uacute;ntate: &laquo;Cuando mi env&iacute;o por fin llegue a Amazon, &iquest;cu&aacute;ntas semanas de inventario voy a tener?&raquo;</p>
  <div class="fixbox">
    <span class="fixbox-k">Qu&eacute; hacer</span>
    <p>Pedir de m&aacute;s sale casi tan caro como pedir de menos.</p>
  </div>
</section>

  <hr class="rule">

  <h2 id="warnings">Tres se&ntilde;ales de alerta que nunca deber&iacute;as ignorar</h2>

  <div class="warn">
    <h3>Tus ventas crecen m&aacute;s r&aacute;pido que tu inventario</h3>
    <p>La demanda se est&aacute; acelerando. Tus c&aacute;lculos de reorden puede que ya est&eacute;n desactualizados.</p>
  </div>

  <div class="warn">
    <h3>Tu proveedor incumple los plazos una y otra vez</h3>
    <p>Si la producci&oacute;n se atrasa dos semanas de forma habitual, deja de usar tiempos de reposici&oacute;n optimistas en tus c&aacute;lculos. Pronostica la realidad, no las promesas.</p>
  </div>

  <div class="warn">
    <h3>Est&aacute;s confiando en tu memoria en lugar de en los n&uacute;meros</h3>
    <p>Si te est&aacute;s diciendo &laquo;creo que todav&iacute;a tenemos inventario suficiente&hellip;&raquo;, es momento de calcular, no de adivinar.</p>
  </div>

<aside class="strip">
  <div>
    <h3>Deja de llevar esto en hojas de c&aacute;lculo</h3>
    <p>AmazeBase vigila por ti los d&iacute;as de cobertura, el tiempo de reposici&oacute;n y la velocidad de ventas, y te avisa cu&aacute;ndo pedir.</p>
  </div>
  <a class="strip-btn" href="/index.html#waitlist">&Uacute;nete a la lista de espera</a>
</aside>

  <h2 id="routine">Una rutina semanal de inventario, simple</h2>

  <p>Cada lunes por la ma&ntilde;ana, dedica diez minutos a responder estas preguntas:</p>

  <ol class="routine">
    <li>&iquest;Cu&aacute;les son mis ventas diarias promedio ahora mismo?</li>
    <li>&iquest;Cu&aacute;ntos d&iacute;as de inventario me quedan?</li>
    <li>&iquest;Ha subido la demanda?</li>
    <li>&iquest;Cambi&oacute; mi tiempo de reposici&oacute;n?</li>
    <li>&iquest;Necesito colocar una orden de compra esta semana?</li>
    <li>Si la demanda subiera de golpe un 20&nbsp;%, &iquest;seguir&iacute;a evitando el quiebre de stock?</li>
  </ol>

  <p>Esas seis preguntas por s&iacute; solas pueden evitar buena parte de las emergencias de inventario que viven los vendedores de Amazon.</p>

  <hr class="rule">

  <h2 id="final">Para cerrar</h2>

  <p>Pronosticar inventario no tiene por qu&eacute; ser complicado. No necesitas algoritmos avanzados para tomar mejores decisiones. Necesitas datos confiables, supuestos realistas y un proceso de revisi&oacute;n constante.</p>

  <p>Los vendedores que evitan los quiebres de stock caros no siempre son los que tienen las hojas de c&aacute;lculo m&aacute;s sofisticadas. Casi siempre son los que hacen las preguntas correctas antes de que el inventario se convierta en un problema.</p>

  <blockquote>
    <p>En planificaci&oacute;n de inventario, adelantarte una semana casi siempre es mejor que llegar un d&iacute;a tarde.</p>
  </blockquote>

</main>

<aside class="rail" aria-label="Cifras clave de este art&iacute;culo">

  <div class="rail-card">
    <span class="rail-k">Ejemplo práctico</span>
    <span class="rail-v">3,160</span>
    <p>Unidades. El punto de reorden de un producto que vende 40 al d&iacute;a, con 69 d&iacute;as de reposici&oacute;n y 400 unidades de stock de seguridad.</p>
  </div>

  <div class="rail-card">
    <span class="rail-k">Reposici&oacute;n real</span>
    <span class="rail-v is-amber">69 d&iacute;as</span>
    <p>La fabricaci&oacute;n son solo 20 de ellos. El resto es preparaci&oacute;n, flete, aduana, transporte terrestre y recepci&oacute;n en Amazon.</p>
  </div>

  <div class="rail-card">
    <span class="rail-k">La brecha que duele</span>
    <span class="rail-v is-violet">50 vs. 69</span>
    <p>D&iacute;as de cobertura contra tiempo de reposici&oacute;n. Si el primer n&uacute;mero es menor, ya vas tarde para pedir.</p>
  </div>

  <p class="rail-src">Cifras de los ejemplos trabajados de este art&iacute;culo, no de un estudio de mercado.</p>

</aside>
</div>

<aside class="cta">
  <h2>Conoce tu punto de reorden sin la hoja de c&aacute;lculo</h2>
  <p>
    AmazeBase conecta tus ventas, tu inventario, tus proveedores y tu flujo de caja
    para que cada decisi&oacute;n de reposici&oacute;n los tenga todos en cuenta a la vez.
  </p>
  <a class="btn" href="/index.html#waitlist">
    &Uacute;nete a la lista de espera
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
         stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M5 12h14M13 6l6 6-6 6"/>
    </svg>
  </a>
</aside>

</div><!-- /.wrap -->'''
