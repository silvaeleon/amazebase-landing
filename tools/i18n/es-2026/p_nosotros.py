# -*- coding: utf-8 -*-
EN_PATH = "/about.html"
ES_PATH = "/es/nosotros.html"

META = dict(
    title="Nosotros",
    desc="Por qu&eacute; construimos AmazeBase, c&oacute;mo pensamos y las seis ideas sobre las que est&aacute; hecho el producto. Construido desde la experiencia, afinado con datos, formado por vendedores.",
    og_title="Construido desde la experiencia. Afinado con datos.",
    og_desc="Por qu&eacute; construimos AmazeBase, c&oacute;mo pensamos y las seis ideas sobre las que est&aacute; hecho el producto.",
    crumb_en="About", crumb_es="Nosotros",
    waitlist_href="/index.html#waitlist",
)

MAIN = u'''<main id="main">

<!-- ====================================================================
     NOSOTROS &mdash; HERO
==================================================================== -->
<section class="section" id="about">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">Sobre nosotros</span>
    <h1>Construido desde la experiencia.<br>Afinado con datos.<br>Formado por vendedores.</h1>
    <p>Creemos que la parte m&aacute;s dif&iacute;cil de llevar un negocio de venta no es
       conseguir m&aacute;s datos. Es saber qu&eacute; te est&aacute;n diciendo esos datos,
       qu&eacute; importa, qu&eacute; falta y qu&eacute; hacer despu&eacute;s.</p>
  </div>

  <figure class="mod-figure is-wide" data-reveal>
    <img width="2272" height="900" src="/assets/img/about-hero.webp"
         alt="Decenas de datos dispersos que se resuelven en una sola decisi&oacute;n" decoding="async">
  </figure>

  <p class="ab-statement" data-reveal>Construimos nuestra plataforma para resolver ese problema.</p>

</div>
</section>


<!-- ====================================================================
     POR QU&Eacute; CONSTRUIMOS ESTO
==================================================================== -->
<section class="section" id="why">
<div class="container">

  <article class="mod" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">Por qu&eacute; construimos esto</span>
      <h3>Vender en l&iacute;nea genera una cantidad enorme de informaci&oacute;n.</h3>
      <p class="mod-lead">Ventas, publicidad, inventario, costos, comisiones, flujo de
         caja, investigaci&oacute;n de productos, proveedores, pron&oacute;sticos y decenas de
         variables m&aacute;s influyen en las decisiones que tomas.</p>
      <p class="mod-lead">Pero esos datos casi nunca viven juntos. Y aun cuando lo hacen,
         m&aacute;s informaci&oacute;n no hace necesariamente m&aacute;s f&aacute;cil decidir.</p>
      <p class="mod-lead"><b>Quer&iacute;amos construir algo distinto.</b></p>
      <ul class="mod-list">
        <li>Que re&uacute;na <b>los datos que importan</b></li>
        <li>Que haga <b>entendibles las relaciones complejas</b></li>
        <li>Que te ayude a <b>concentrarte en lo que merece tu atenci&oacute;n</b></li>
        <li>Que te diga <b>qu&eacute; falta</b> en vez de simplemente detenerte</li>
      </ul>
      <p class="mod-benefit">El objetivo no es otro panel m&aacute;s.
         <b>El objetivo son mejores decisiones.</b></p>
    </div>
    <figure class="mod-figure">
    <img width="1536" height="1000" src="/assets/img/about-inputs-converge.webp"
         alt="Ventas, publicidad, inventario, costos, comisiones, flujo de caja, proveedores y pron&oacute;sticos convergiendo en una sola decisi&oacute;n" decoding="async">
  </figure>
  </article>

</div>
</section>


<!-- ====================================================================
     LAS TRES PERSPECTIVAS
==================================================================== -->
<section class="section" id="intersection">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">C&oacute;mo pensamos</span>
    <h2>Construido en el cruce entre vender, datos y tecnolog&iacute;a.</h2>
    <p>Nuestro enfoque nace de combinar tres perspectivas que no siempre coinciden.</p>
  </div>

  <div class="sec-grid" data-reveal-stagger>

    <article class="sec-card">
      <span class="sec-ico"><svg><use href="#i-box"/></svg></span>
      <h3>Vender de verdad</h3>
      <p>Entender las decisiones, las restricciones y los sacrificios que los vendedores
         enfrentan cada d&iacute;a.</p>
    </article>

    <article class="sec-card">
      <span class="sec-ico"><svg><use href="#i-db"/></svg></span>
      <h3>Datos e IA</h3>
      <p>A&ntilde;os de experiencia trabajando con datos complejos, sistemas anal&iacute;ticos e
         IA, incluida m&aacute;s de una d&eacute;cada en datos e IA en IBM.</p>
    </article>

    <article class="sec-card">
      <span class="sec-ico"><svg><use href="#i-gear"/></svg></span>
      <h3>Tecnolog&iacute;a</h3>
      <p>Construir sistemas que convierten ideas anal&iacute;ticas complejas en herramientas
         que la gente puede usar, entender y accionar de verdad.</p>
    </article>

  </div>

  <p class="ab-statement" data-reveal>Ninguna de estas perspectivas basta por s&iacute; sola.<br>
     Juntas, crean algo mucho m&aacute;s &uacute;til.</p>

</div>
</section>


<!-- ====================================================================
     NUESTRA FILOSOF&Iacute;A
     Seis bloques, alternando lados, cada uno con su propio hueco de gr&aacute;fico.
==================================================================== -->
<section class="section" id="philosophy">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">Nuestra filosof&iacute;a</span>
    <h2>Seis ideas sobre las que est&aacute; construido el producto.</h2>
  </div>

  <article class="mod" id="everything" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">Todo lo que importa</span>
      <h3>Las decisiones importantes casi nunca dependen de una sola m&eacute;trica.</h3>
      <p class="mod-lead">Las ventas pueden verse sanas mientras la rentabilidad cae. La
         publicidad puede ser eficiente mientras el inventario se convierte en un
         cuello de botella. Un producto puede parecer atractivo hasta que se incluyen
         sus costos reales.</p>
      <p class="mod-benefit">Dise&ntilde;amos la plataforma para <b>conectar los datos que de
         verdad influyen en una decisi&oacute;n</b>, en lugar de optimizar un solo
         n&uacute;mero de forma aislada.</p>
    </div>
    <figure class="mod-figure">
    <img width="1536" height="1000" src="/assets/img/about-sales-vs-reality.webp"
         alt="Ingresos que suben a lo largo de 24 meses mientras el margen bruto, la cobertura de stock y la inversi&oacute;n publicitaria como porcentaje de los ingresos se mueven en la direcci&oacute;n equivocada" decoding="async">
  </figure>
  </article>

  <article class="mod is-flipped" id="complexity" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">Hacer entendible lo complejo</span>
      <h3>No creemos que un software potente tenga que sentirse complicado.</h3>
      <p class="mod-lead">La complejidad deber&iacute;a vivir debajo del sistema, que es
         donde le toca.</p>
      <p class="mod-lead">Nuestro trabajo es tomar grandes cantidades de
         informaci&oacute;n, relaciones y c&aacute;lculos y convertirlas en algo lo bastante
         entendible como para decidir con confianza.</p>
      <p class="mod-benefit">Complejo por debajo.<br><b>Simple donde importa.</b></p>
    </div>
    <figure class="mod-figure">
    <img width="1536" height="1000" src="/assets/img/about-complexity-below.webp"
         alt="Una respuesta en lenguaje claro sobre los treinta c&aacute;lculos que la sostienen" decoding="async">
  </figure>
  </article>

  <article class="mod" id="diagnose" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">No bloquees. Diagnostica.</span>
      <h3>Los negocios reales casi nunca tienen informaci&oacute;n perfecta.</h3>
      <p class="mod-lead">Que falten datos no deber&iacute;a significar siempre chocar contra
         un muro.</p>
      <p class="mod-lead">Cuando falta algo importante, el sistema deber&iacute;a ayudarte a
         entender qu&eacute; falta, por qu&eacute; importa y qu&eacute; puedes hacer al
         respecto.</p>

      <div class="ab-contrast">
        <article class="is-bad">
          <span class="ab-label">En vez de</span>
          <p>&laquo;No se puede continuar.&raquo;</p>
        </article>
        <article class="is-good">
          <span class="ab-label">Queremos que escuches</span>
          <p>&laquo;Esto es lo que nos falta, y esta es la raz&oacute;n por la que
             importa.&raquo;</p>
        </article>
      </div>
    </div>
    <figure class="mod-figure">
    <img width="1536" height="1000" src="/assets/img/about-completeness.webp"
         alt="Cuatro de seis fuentes conectadas, las dos que faltan nombradas, y lo que se desbloquear&iacute;a al conectarlas" decoding="async">
  </figure>
  </article>

  <article class="mod is-flipped" id="one-percent" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">El principio del 1&nbsp;%</span>
      <h3>No necesitas pasarte el tiempo analizando todo.</h3>
      <p class="mod-lead">Necesitas encontrar esa peque&ntilde;a parte que merece tu
         atenci&oacute;n. Nuestro enfoque anal&iacute;tico est&aacute; dise&ntilde;ado para ir
         estrechando el campo:</p>
      <ul class="mod-list">
        <li><b>Entender el conjunto.</b></li>
        <li><b>Identificar lo que es inusual</b>, importante o potencialmente valioso.</li>
        <li><b>Concentrarse en las pocas cosas</b> que pueden marcar una diferencia real.</li>
        <li><b>Y entonces actuar.</b></li>
      </ul>
      <p class="mod-benefit">El objetivo no es darte m&aacute;s cosas que mirar.
         <b>Es ayudarte a encontrar el 1&nbsp;% sobre el que vale la pena actuar.</b></p>
    </div>
    <figure class="mod-figure">
    <img width="1536" height="1000" src="/assets/img/about-narrowing.webp"
         alt="Un campo que se estrecha de 1,284 elementos a los siete que vale la pena abrir hoy" decoding="async">
  </figure>
  </article>

  <article class="mod" id="learn" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">Aprende de ti. Aprende de los mejores.</span>
      <h3>Tu negocio tiene una historia.</h3>
      <p class="mod-lead">Tus decisiones tienen consecuencias. Tu desempe&ntilde;o cambia con
         el tiempo. Queremos que la plataforma te ayude a entender esa trayectoria en vez
         de tratar cada d&iacute;a, producto o decisi&oacute;n como un hecho aislado.</p>
      <p class="mod-lead">Y, cuando corresponda y cuidando la privacidad, los datos
         agregados pueden dar otra perspectiva: c&oacute;mo se compara tu desempe&ntilde;o con
         patrones m&aacute;s amplios y qu&eacute; est&aacute;n haciendo distinto los que mejor
         lo hacen.</p>
      <p class="mod-benefit">Los benchmarks no son instrucciones. <b>Son contexto.</b> El
         objetivo no es decirle a cada vendedor que se comporte igual. Es ayudarte a
         entender d&oacute;nde est&aacute;s parado, descubrir patrones y tomar mejores
         decisiones para tu propio negocio.</p>
    </div>
    <figure class="mod-figure">
    <img width="1536" height="1000" src="/assets/img/about-trajectory.webp"
         alt="Tu propia l&iacute;nea de tendencia elev&aacute;ndose por encima del rango medio de vendedores comparables" decoding="async">
  </figure>
  </article>

  <article class="mod is-flipped" id="with-users" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">Construido con los usuarios</span>
      <h3>Un producto as&iacute; no se puede dise&ntilde;ar solo desde una hoja de c&aacute;lculo o una sala de juntas.</h3>
      <p class="mod-lead">La realidad de llevar un negocio de venta tiene demasiados
         matices. Por eso la plataforma se va formando continuamente con feedback, flujos
         de trabajo reales y la experiencia de quienes la usan.</p>
      <ul class="mod-list">
        <li>Escuchamos <b>d&oacute;nde se atascan los usuarios</b>.</li>
        <li>Prestamos atenci&oacute;n a <b>qu&eacute; necesitan entender</b>.</li>
        <li><b>Cuestionamos supuestos</b>.</li>
        <li>Y <b>afinamos el producto</b> en consecuencia.</li>
      </ul>
      <p class="mod-benefit">La metodolog&iacute;a no est&aacute; terminada.
         <b>Mejora a medida que aprendemos.</b></p>
    </div>
    <figure class="mod-figure">
    <img width="1536" height="1000" src="/assets/img/about-built-with-users.webp"
         alt="Tres comentarios de vendedores y los tres cambios de producto que produjeron" decoding="async">
  </figure>
  </article>

</div>
</section>


<!-- ====================================================================
     DE LOS DATOS A LA DECISI&Oacute;N
==================================================================== -->
<section class="section" id="loop">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">De los datos a la decisi&oacute;n</span>
    <h2>Casi todos los sistemas anal&iacute;ticos se detienen en la informaci&oacute;n.<br>Nosotros queremos ir m&aacute;s lejos.</h2>
  </div>

  <div class="ab-flow" data-reveal-stagger>
    <article><h3>Datos</h3><p>&iquest;Qu&eacute; pas&oacute;?</p></article>
    <article><h3>Contexto</h3><p>&iquest;Por qu&eacute; pudo haber pasado?</p></article>
    <article><h3>An&aacute;lisis</h3><p>&iquest;Qu&eacute; importa?</p></article>
    <article><h3>Foco</h3><p>&iquest;Qu&eacute; merece atenci&oacute;n?</p></article>
    <article><h3>Acci&oacute;n</h3><p>&iquest;Qu&eacute; deber&iacute;as investigar o hacer ahora?</p></article>
    <article><h3>Aprendizaje</h3><p>&iquest;Qu&eacute; pas&oacute; como resultado?</p></article>
  </div>

  <figure class="mod-figure is-wide" data-reveal style="margin-top:var(--s4)">
    <img width="2272" height="900" src="/assets/img/about-decision-loop.webp"
         alt="Las seis etapas &mdash; datos, contexto, an&aacute;lisis, foco, acci&oacute;n, aprendizaje &mdash; dibujadas como un ciclo cerrado, con el aprendizaje realimentando los datos" decoding="async">
  </figure>

  <p class="ab-statement" data-reveal>Mientras m&aacute;s se usa este ciclo, m&aacute;s &uacute;til
     se vuelve el sistema.</p>

</div>
</section>


<!-- ====================================================================
     COMUNIDAD
==================================================================== -->
<section class="section" id="community">
<div class="container">

  <article class="mod" data-reveal>
    <div class="mod-copy">
      <span class="mod-eyebrow">Comunidad</span>
      <h3>El conocimiento no deber&iacute;a quedarse con un solo vendedor.</h3>
      <p class="mod-lead">Todo vendedor termina descubriendo algo por las malas.</p>
      <ul class="mod-list">
        <li>Una decisi&oacute;n de precio.</li>
        <li>Un error de inventario.</li>
        <li>Una estrategia publicitaria que funcion&oacute; inesperadamente bien.</li>
        <li>Un producto que parec&iacute;a prometedor y no lo era.</li>
        <li>Un proceso que ahorr&oacute; horas cada semana.</li>
      </ul>
      <p class="mod-lead">Creemos que esas experiencias valen. Por eso la comunidad es
         parte de la visi&oacute;n.</p>
      <p class="mod-benefit">No una red social por tenerla.
         <b>Un lugar donde experiencias, decisiones, experimentos y lecciones reales
         puedan servirle a otras personas que enfrentan problemas parecidos.</b></p>
    </div>
    <figure class="mod-figure">
    <img width="1536" height="1000" src="/assets/img/about-community.webp"
         alt="La lecci&oacute;n de un vendedor convertida en una tarjeta sobre la que act&uacute;an otros tres vendedores" decoding="async">
  </figure>
  </article>

</div>
</section>


<!-- ====================================================================
     EN QU&Eacute; CREEMOS  /  NUESTRO EST&Aacute;NDAR
==================================================================== -->
<section class="section" id="believe">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">En qu&eacute; creemos</span>
    <h2>Los vendedores no necesitan otro sitio donde mirar n&uacute;meros.<br>
        Necesitan una mejor forma de entender qu&eacute; significan esos n&uacute;meros.</h2>
  </div>

  <ul class="ab-list" data-reveal>
    <li><svg><use href="#i-check"/></svg>
        <span>No deber&iacute;an tener que <b>volverse cient&iacute;ficos de datos</b> para usar sus propios datos.</span></li>
    <li><svg><use href="#i-check"/></svg>
        <span>No deber&iacute;an tener que <b>conectar decenas de hojas de c&aacute;lculo</b> antes de poder decidir.</span></li>
    <li><svg><use href="#i-check"/></svg>
        <span>No deber&iacute;an quedar <b>bloqueados porque falta un dato</b>.</span></li>
    <li><svg><use href="#i-check"/></svg>
        <span>Y no deber&iacute;an tener que <b>pasarse horas buscando</b> entre todo para encontrar lo &uacute;nico que de verdad importa.</span></li>
  </ul>

  <p class="ab-statement" data-reveal>Creemos que el software deber&iacute;a hacer m&aacute;s del
     trabajo anal&iacute;tico duro para que la gente dedique m&aacute;s tiempo a decidir.</p>

</div>
</section>


<section class="section" id="standard">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">Nuestro est&aacute;ndar</span>
    <h2>Estamos construyendo esto con un principio simple.</h2>
  </div>

  <ul class="ab-list" data-reveal>
    <li><svg><use href="#i-arrow"/></svg><span>Si el sistema puede <b>aclarar algo</b>, deber&iacute;a hacerlo.</span></li>
    <li><svg><use href="#i-arrow"/></svg><span>Si puede <b>sacar a la luz algo importante</b>, deber&iacute;a hacerlo.</span></li>
    <li><svg><use href="#i-arrow"/></svg><span>Si falta algo, deber&iacute;a <b>explicar por qu&eacute;</b>.</span></li>
    <li><svg><use href="#i-arrow"/></svg><span>Si hay incertidumbre, deber&iacute;a <b>hacerla visible</b>.</span></li>
    <li><svg><use href="#i-arrow"/></svg><span>Si hay una <b>mejor pregunta que hacer</b>, deber&iacute;a ayudarte a encontrarla.</span></li>
    <li><svg><use href="#i-arrow"/></svg><span>Y si hay algo que a&uacute;n no sabemos, <b>deber&iacute;amos decirlo</b>.</span></li>
  </ul>

  <figure class="quote" data-reveal style="margin-top:var(--s5)">
    <span class="quote-face"><svg class="icon-sm"><use href="#i-shield"/></svg></span>
    <div>
      <p>Porque el software confiable no es el que finge saberlo todo. Es el que te
         ayuda a entender qu&eacute; sabes, qu&eacute; no, y qu&eacute; merece tu atenci&oacute;n
         ahora.</p>
      <cite>&mdash; Nuestro est&aacute;ndar</cite>
    </div>
  </figure>

</div>
</section>


<!-- ====================================================================
     HACIA D&Oacute;NDE VAMOS
==================================================================== -->
<section class="section" id="going">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">Hacia d&oacute;nde vamos</span>
    <h2>Empezamos con un problema simple:<br>demasiada informaci&oacute;n y poca claridad.</h2>
    <p>La visi&oacute;n m&aacute;s grande es construir un sistema donde los vendedores puedan
       reunir la informaci&oacute;n que importa, entender su negocio como un todo, aprender
       de su propia historia, aprender de otros y tomar mejores decisiones con menos
       esfuerzo desperdiciado.</p>
  </div>

  <figure class="mod-figure is-wide" data-reveal>
    <img width="2272" height="900" src="/assets/img/about-horizon.webp"
         alt="Cinco etapas en el horizonte: reunir la informaci&oacute;n, entender el negocio como un todo, aprender de tu propia historia, aprender de otros vendedores, decidir con menos esfuerzo desperdiciado" decoding="async">
  </figure>

  <p class="ab-statement" data-reveal>
    No m&aacute;s ruido.<br>No m&aacute;s paneles.<br>
    <b>M&aacute;s entendimiento. Y, al final, mejores decisiones.</b>
  </p>

  <div class="section-head" data-reveal style="margin-top:var(--s5)">
    <a class="btn btn--primary btn--lg" href="#waitlist" data-waitlist-open data-source="about" data-magnetic>
      &Uacute;nete a la lista de espera <svg class="icon-sm"><use href="#i-arrow"/></svg>
    </a>
  </div>

</div>
</section>

</main>'''
