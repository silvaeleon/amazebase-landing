# -*- coding: utf-8 -*-
EN_PATH = "/solutions.html"
ES_PATH = "/es/soluciones.html"

META = dict(
    title="Soluciones",
    desc="Tres formas de usar AmazeBase, seg&uacute;n d&oacute;nde est&eacute; el negocio hoy: planificar tus primeros productos, gestionar un portafolio a escala o llevar cuentas de otras personas.",
    og_title="Tres formas de usar AmazeBase",
    og_desc="Principiantes, vendedores con experiencia y agencias. Tres formas de usar AmazeBase, seg&uacute;n d&oacute;nde est&eacute; el negocio hoy.",
    crumb_en="Solutions", crumb_es="Soluciones",
    waitlist_href="/index.html#waitlist",
)

MAIN = u'''<main id="main">

<!-- ====================================================================
     SOLUCIONES &mdash; tres formas de entrar
     Una p&aacute;gina, tres p&uacute;blicos anclados. El men&uacute; Soluciones de cada
     p&aacute;gina apunta a las tres anclas de abajo, as&iacute; que los elementos del
     men&uacute; y las secciones se mantienen sincronizados: #beginners,
     #experts, #agencies.
==================================================================== -->
<section class="section" id="solutions">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">Soluciones</span>
    <h1>No necesitas el sistema completo desde el primer d&iacute;a.</h1>
    <p>Tres formas de usar AmazeBase, seg&uacute;n d&oacute;nde est&eacute; el negocio hoy
       &mdash; planificando tus primeros productos, gestionando un portafolio a escala
       o llevando cuentas de otras personas.</p>
  </div>

  <div class="sol-switch" data-reveal-stagger>
    <a class="sol-card" href="#beginners">
      <span class="sol-ico"><svg><use href="#i-rocket"/></svg></span>
      <h2>Principiantes</h2>
      <p>Planifica y simula antes de gastar. No hace falta conectar Amazon.</p>
      <span class="sol-go">Planificaci&oacute;n y simulaciones <svg class="icon-sm"><use href="#i-arrow"/></svg></span>
    </a>
    <a class="sol-card" href="#experts">
      <span class="sol-ico"><svg><use href="#i-chart"/></svg></span>
      <h2>Vendedores con experiencia</h2>
      <p>Todos los m&oacute;dulos, apoyados en la misma columna vertebral: tu costo real puesto en destino.</p>
      <span class="sol-go">Los ocho m&oacute;dulos <svg class="icon-sm"><use href="#i-arrow"/></svg></span>
    </a>
    <a class="sol-card" href="#agencies">
      <span class="sol-ico"><svg><use href="#i-case"/></svg></span>
      <h2>Agencias</h2>
      <p>Muchas cuentas, muchos marketplaces y reportes que los clientes s&iacute; leen.</p>
      <span class="sol-go">Multicuenta <svg class="icon-sm"><use href="#i-arrow"/></svg></span>
    </a>
  </div>

</div>
</section>


<!-- ====================================================================
     PRINCIPIANTES
==================================================================== -->
<section class="section" id="beginners">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">Para principiantes</span>
    <h2>Empieza a decidir antes de empezar a vender.</h2>
    <p>Los m&oacute;dulos de planificaci&oacute;n y simulaci&oacute;n funcionan antes de que
       env&iacute;es una sola unidad. Sin cuenta que conectar, sin claves de API, sin
       esperar datos. Trae la investigaci&oacute;n que ya tienes y averigua qu&eacute; idea
       vale de verdad el dinero.</p>
  </div>

  <article class="mod" id="planning" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">Planificaci&oacute;n e investigaci&oacute;n de productos</span>
      <h3>Punt&uacute;a la idea antes de comprar el inventario.</h3>
      <p class="mod-lead">Sube la investigaci&oacute;n que ya hiciste y pasa cada idea por la
         misma prueba, para que &laquo;esta me da buena espina&raquo; se convierta en un
         n&uacute;mero con el que puedas comparar dos productos.</p>
      <ul class="mod-list">
        <li><b>Cuatro dimensiones que lo deciden</b> &mdash; visibilidad, tama&ntilde;o de
            mercado, competencia y rentabilidad, puntuadas igual siempre</li>
        <li><b>Arma tu propio sistema de puntuaci&oacute;n.</b> Pondera lo que le importa a
            tu negocio en vez de aceptar la definici&oacute;n ajena de un buen producto</li>
        <li><b>Compara productos lado a lado</b> en vez de quedarte con el que miraste
            m&aacute;s recientemente</li>
        <li><b>Trae tu propia investigaci&oacute;n.</b> Importa los archivos que ya tienes
            &mdash; nada que conectar, nada que esperar</li>
      </ul>
      <p class="mod-benefit">La puntuaci&oacute;n nunca fue el objetivo. <b>Lo que importa es
         saber cu&aacute;l de tus diez ideas merece el efectivo.</b></p>
    </div>
    <figure class="mod-figure" data-reveal>
      <img width="975" height="635" src="/assets/img/sol-planning.webp"
           alt="El m&oacute;dulo de Planificaci&oacute;n puntuando diez ideas de producto por tama&ntilde;o de mercado, cuota de los cuatro primeros, n&uacute;mero de palabras clave y margen, cada una con un veredicto de Buena o Marginal" decoding="async">
    </figure>
  </article>

  <article class="mod is-flipped" id="simulations" data-reveal>
    <figure class="mod-figure" data-reveal>
      <img width="1058" height="689" src="/assets/img/sol-simulations.webp"
           alt="El m&oacute;dulo de Simulaciones mostrando una corrida que falla: no se alcanza el punto de equilibrio, ROI de menos 174 por ciento y una l&iacute;nea de saldo de efectivo que cae por debajo de cero en la quincena 25 hasta un m&iacute;nimo de menos 37,043 d&oacute;lares, con inventario en stock todo el tiempo" decoding="async">
    </figure>
    <div class="mod-copy">
      <span class="mod-eyebrow">Simulaciones</span>
      <h3>Averigua si puedes pagar el plan antes de comprometerte con &eacute;l.</h3>
      <p class="mod-lead">Modela el lanzamiento hacia adelante partiendo del efectivo que
         de verdad tienes &mdash; producci&oacute;n, env&iacute;o, la curva de ventas, la
         reposici&oacute;n &mdash; y mira d&oacute;nde aguanta y d&oacute;nde se rompe.</p>
      <ul class="mod-list">
        <li><b>Cu&aacute;ntos productos puede sostener tu efectivo de verdad</b>, no
            cu&aacute;ntos te gustar&iacute;a</li>
        <li><b>Cu&aacute;ndo funciona el flujo de caja y cu&aacute;ndo no</b>, quincena a
            quincena</li>
        <li><b>Cu&aacute;ndo lanzar y cu&aacute;ndo esperar</b> &mdash; el mismo producto
            puede ser buena idea en marzo y mala en noviembre</li>
        <li><b>Si tus propios supuestos te dejan sin stock</b> antes de que llegue la
            reposici&oacute;n</li>
        <li><b>Si la utilidad compensa el riesgo</b> que est&aacute;s corriendo para
            conseguirla</li>
        <li><b>Planifica efectivo y lanzamientos con meses de anticipaci&oacute;n</b>, no
            una orden de compra a la vez</li>
      </ul>
      <p class="mod-benefit">Puedes ser rentable en el papel y aun as&iacute; quedarte sin
         dinero. <b>Aqu&iacute; es donde te enteras mientras todav&iacute;a es gratis.</b></p>
    </div>
  </article>

</div>
</section>


<!-- ====================================================================
     VENDEDORES CON EXPERIENCIA
==================================================================== -->
<section class="section" id="experts">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">Para vendedores con experiencia</span>
    <h2>Todos los m&oacute;dulos, apoyados en el mismo n&uacute;mero.</h2>
    <p>Conecta tus datos y los m&oacute;dulos dejan de comportarse como herramientas
       sueltas. El costo puesto en destino alimenta la utilidad. La utilidad fija el
       punto de equilibrio contra el que se juzga cada decisi&oacute;n publicitaria. Las
       decisiones publicitarias mueven el inventario. Acierta ese n&uacute;mero y todo el
       sistema dice la verdad.</p>
  </div>

  <article class="mod" id="financials" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">Finanzas</span>
      <h3>Sabe cu&aacute;nto ganaste y a d&oacute;nde se fue.</h3>
      <p class="mod-lead">Un estado de resultados real reconstruido desde tus
         liquidaciones y no desde tu reporte de ventas &mdash; ingresos, toda la pila de
         comisiones de Amazon, lo que de verdad te costaron las unidades, publicidad,
         devoluciones y los gastos generales que solo t&uacute; conoces.</p>
      <ul class="mod-list">
        <li><b>Por mes y por SKU</b>, para que un buen mes no pueda esconder un mal
            producto</li>
        <li><b>Dos n&uacute;meros de utilidad</b> &mdash; contribuci&oacute;n y neta &mdash;
            porque responden preguntas distintas</li>
        <li><b>Las comisiones de Amazon desglosadas</b>, no aplastadas en una sola
            l&iacute;nea que no puedes discutir</li>
        <li><b>De d&oacute;nde vino el efectivo y a d&oacute;nde se fue</b>, rastreable hasta
            la fila que lo origin&oacute;</li>
      </ul>
    </div>
    <figure class="mod-figure" data-reveal>
      <img width="975" height="635" src="/assets/img/sol-financials.webp"
           alt="El m&oacute;dulo Financiero mostrando ingresos, utilidad neta, utilidad de contribuci&oacute;n, inversi&oacute;n publicitaria y TACoS sobre un gr&aacute;fico de ingresos y rentabilidad desglosado por trimestre" decoding="async">
    </figure>
  </article>

  <article class="mod is-flipped" id="ledger" data-reveal>
    <figure class="mod-figure" data-reveal>
      <img width="975" height="635" src="/assets/img/sol-ledger.webp"
           alt="El m&oacute;dulo Ledger mostrando costo puesto en destino, eventos de costo, &oacute;rdenes de compra abiertas y costos sin conciliar sobre una lista de cargos recientes de proveedores y aduana" decoding="async">
    </figure>
    <div class="mod-copy">
      <span class="mod-eyebrow">Ledger</span>
      <h3>Cada d&oacute;lar que cost&oacute; traer las unidades hasta aqu&iacute;.</h3>
      <p class="mod-lead">&Oacute;rdenes de compra, flete, aduana y aranceles,
         inspecci&oacute;n, moldes, herramentales y dise&ntilde;o &mdash; ensamblados en un
         costo puesto en destino por unidad que podr&iacute;as defender ante un contador.</p>
      <ul class="mod-list">
        <li><b>Cada orden de compra y d&oacute;nde est&aacute; de verdad</b> &mdash;
            fabricaci&oacute;n, flete, aduana, inspecci&oacute;n, recibida</li>
        <li><b>Costos de producto y no-producto juntos</b> &mdash; transporte, impuestos,
            moldes, dise&ntilde;adores, muestras, todo lo que las hojas de c&aacute;lculo
            dejan caer sin avisar</li>
        <li><b>Costo puesto en destino por unidad que lleg&oacute;</b>, no por unidad que
            pediste</li>
        <li><b>Sabe qu&eacute; falta</b> &mdash; una factura de flete que nunca entr&oacute;,
            y a qu&eacute; orden de compra pertenece</li>
      </ul>
      <p class="mod-benefit"><b>Este es el n&uacute;mero sobre el que est&aacute; construido
         el resto del producto.</b> Si lo tienes mal, todas las cifras de utilidad
         aguas abajo son ficci&oacute;n.</p>
    </div>
  </article>

  <article class="mod" id="inventory" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">Inventario</span>
      <h3>No &laquo;te queda poco stock&raquo;. El &uacute;ltimo d&iacute;a en que puedes pedir sin riesgo.</h3>
      <p class="mod-lead">Fechas l&iacute;mite de pedido, cantidades sugeridas y velocidad
         real, en todos los lugares donde tu stock est&aacute; realmente.</p>
      <ul class="mod-list">
        <li><b>Cu&aacute;ndo pedir y cu&aacute;ntas unidades</b> &mdash; el quiebre de stock
            menos tu tiempo de reposici&oacute;n, no un umbral que alguien adivin&oacute;</li>
        <li><b>Velocidad de ventas que refleja la realidad</b>, incluido lo que la
            publicidad est&aacute; sosteniendo</li>
        <li><b>FBA, AWD y 3PL en una sola vista</b> en vez de tres pesta&ntilde;as y una
            nota mental</li>
        <li><b>El atraso dicho en voz alta</b> &mdash; &laquo;14 d&iacute;as de
            atraso&raquo;, no un punto amarillo que aprendes a ignorar</li>
      </ul>
      <p class="mod-benefit"><b>Nunca te quedes sin el producto que estaba funcionando.</b></p>
    </div>
    <figure class="mod-figure" data-reveal>
      <img width="1536" height="1000" src="/assets/img/sol-inventory.webp"
           alt="El stock de un SKU repartido entre FBA, AWD y 3PL como una sola barra: 612 vendibles ahora, 285 en reserva, 180 a&uacute;n antes de llegar a Amazon, sobre el &uacute;ltimo d&iacute;a en que puede reponerse sin riesgo" decoding="async">
    </figure>
  </article>

  <article class="mod is-flipped" id="ads" data-reveal>
    <figure class="mod-figure" data-reveal>
      <img width="975" height="635" src="/assets/img/sol-ads.webp"
           alt="El m&oacute;dulo de Publicidad mostrando inversi&oacute;n publicitaria, ventas por publicidad, margen despu&eacute;s de PPC, ACoS y TACoS sobre dos a&ntilde;os de ventas netas diarias frente al margen" decoding="async">
    </figure>
    <div class="mod-copy">
      <span class="mod-eyebrow">Consola de publicidad</span>
      <h3>PPC y org&aacute;nico, por fin juzgados juntos.</h3>
      <p class="mod-lead">Palabras clave, campa&ntilde;as, ubicaciones, franjas horarias y
         brand analytics en una sola consola &mdash; con los clics automatizados y las
         decisiones explicadas.</p>
      <ul class="mod-list">
        <li><b>Punto de equilibrio, no ACoS</b> &mdash; cada campa&ntilde;a juzgada contra
            lo que ese producto en concreto puede permitirse</li>
        <li><b>Posici&oacute;n y ventas org&aacute;nicas junto a las de pago</b>, para que
            veas qu&eacute; est&aacute;s alquilando y qu&eacute; es tuyo</li>
        <li><b>Palabras clave, t&eacute;rminos de b&uacute;squeda, ubicaciones y franjas
            horarias</b> en un solo lugar, con brand analytics al lado</li>
        <li><b>El trabajo manual automatizado</b> &mdash; cuarenta cambios de puja en una
            sola carga en vez de una tarde de clics</li>
      </ul>
      <p class="mod-benefit"><b>Control total del PPC, sin las tardes.</b></p>
    </div>
  </article>

</div>
</section>


<!-- ====================================================================
     AGENCIAS
==================================================================== -->
<section class="section" id="agencies">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">Para agencias</span>
    <h2>Cada cliente, cada marketplace, una sola consola.</h2>
    <p>Gestiona varias cuentas en varios mercados sin rehacer la misma hoja de
       c&aacute;lculo para cada una &mdash; y dales a tus clientes algo que de verdad
       quieran abrir.</p>
  </div>

  <article class="mod" id="multi-account" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">Multicuenta y multimercado</span>
      <h3>Cambia de cliente sin cambiar de herramienta.</h3>
      <p class="mod-lead">Cada cuenta que gestionas, en cada marketplace donde vende, bajo
         un solo acceso &mdash; con los mismos n&uacute;meros calculados de la misma forma
         para todas.</p>
      <ul class="mod-list">
        <li><b>Varias cuentas lado a lado</b>, cada una con sus propios costos puestos en
            destino, comisiones y m&aacute;rgenes</li>
        <li><b>Varios marketplaces por cuenta</b>, con las diferencias de moneda y de
            comisiones gestionadas en vez de ignoradas</li>
        <li><b>Acceso por cliente</b> &mdash; dale a un cliente una ventana a su propia
            cuenta sin darle la de los dem&aacute;s</li>
        <li><b>Vista de portafolio o de un solo cliente</b>, seg&uacute;n la
            conversaci&oacute;n en la que est&eacute;s</li>
      </ul>
    </div>
    <figure class="mod-figure" data-reveal>
      <img width="1536" height="1000" src="/assets/img/sol-multi-account.webp"
           alt="Siete cuentas de clientes en una lista, cada una con los marketplaces donde vende, sus ingresos y su margen, con una cuenta marcada para revisar" decoding="async">
    </figure>
  </article>

  <article class="mod is-flipped" id="reporting" data-reveal>
    <figure class="mod-figure" data-reveal>
      <img width="1536" height="1000" src="/assets/img/sol-reporting.webp"
           alt="Cuatro cambios que hizo una agencia, cada uno con la evidencia detr&aacute;s y el resultado calificado: tres marcados como funcion&oacute; y uno como mixto" decoding="async">
    </figure>
    <div class="mod-copy">
      <span class="mod-eyebrow">Reportes e insights</span>
      <h3>Reportes que leen. Insights que recuerdan.</h3>
      <p class="mod-lead">Cualquiera puede mandarle a un cliente una tabla con los
         n&uacute;meros del mes pasado. La conversaci&oacute;n de renovaci&oacute;n la gana la
         agencia que puede decir qu&eacute; cambi&oacute;, por qu&eacute; y qu&eacute; pas&oacute;
         despu&eacute;s.</p>
      <ul class="mod-list">
        <li><b>Reportes listos para el cliente</b> que van m&aacute;s all&aacute; de lo que
            pas&oacute; y cuentan qu&eacute; hiciste al respecto</li>
        <li><b>La evidencia detr&aacute;s de cada recomendaci&oacute;n</b>, para que el
            consejo sobreviva a que lo cuestionen</li>
        <li><b>Antes y despu&eacute;s de los cambios que hiciste</b> &mdash; calificados, no
            afirmados</li>
        <li><b>El insight que nadie m&aacute;s les est&aacute; mostrando</b> &mdash; el
            margen real puesto en destino, qu&eacute; est&aacute; sosteniendo de verdad la
            publicidad, a d&oacute;nde se va el efectivo</li>
      </ul>
      <p class="mod-benefit"><b>Deja de demostrar que estuviste ocupado. Empieza a
         demostrar que ten&iacute;as raz&oacute;n.</b></p>
    </div>
  </article>

</div>
</section>


<!-- ====================================================================
     CIERRE
==================================================================== -->
<section class="section" id="sol-close">
<div class="container">
  <div class="sol-close" data-reveal>
    <h2>Seas cual seas de los tres, las preguntas son las mismas.</h2>
    <p>&iquest;Cu&aacute;nto me est&aacute; dejando esto de verdad? &iquest;Qu&eacute; deber&iacute;a
       hacer despu&eacute;s? AmazeBase est&aacute; hecho para responder esas dos, desde tu
       primera investigaci&oacute;n de producto hasta tu cuenta n&uacute;mero cincuenta.</p>
    <a class="btn btn--primary btn--lg" href="#waitlist" data-waitlist-open data-source="solutions" data-magnetic>
      &Uacute;nete a la lista de espera <svg class="icon-sm"><use href="#i-arrow"/></svg>
    </a>
  </div>
</div>
</section>

</main>'''
