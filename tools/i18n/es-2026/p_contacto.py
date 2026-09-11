# -*- coding: utf-8 -*-
EN_PATH = "/contact.html"
ES_PATH = "/es/contacto.html"

META = dict(
    title="Contacto",
    desc="Contacta con AmazeBase. Desarrollado y operado por Silbros Trading LLC, Albuquerque, Nuevo M&eacute;xico. Correo: contact@silbrostrading.com.",
    og_title="Contacto",
    og_desc="Contacta con AmazeBase. Desarrollado y operado por Silbros Trading LLC, Albuquerque, Nuevo M&eacute;xico.",
    crumb_en="Contact", crumb_es="Contacto",
    waitlist_href="/index.html#waitlist",
)

MAIN = u'''<main id="main">

<!-- ====================================================================
     CONTACTO
==================================================================== -->
<section class="section" id="contact">
<div class="container">

  <div class="section-head" data-reveal>
    <span class="eyebrow">Empresa</span>
    <h1>Hablemos.</h1>
    <p>Preguntas, alianzas o prensa &mdash; nos gustar&iacute;a saber de ti.</p>
  </div>

  <!-- .is-flipped pone la figura a la IZQUIERDA y los datos a la derecha -->
  <article class="mod is-flipped" data-reveal>

    <div class="mod-copy">
      <span class="mod-eyebrow">Nuestros datos</span>
      <h3>Silbros Trading LLC</h3>
      <p class="mod-lead">AmazeBase est&aacute; desarrollado y operado por Silbros Trading LLC.</p>

      <div class="ct-details">

        <div class="ct-row">
          <span class="sec-ico"><svg><use href="#i-globe"/></svg></span>
          <div>
            <span class="ct-label">Domicilio social</span>
            <address class="ct-value">
              <span class="ct-company">Silbros Trading LLC</span><br>
              1209 Mountain Road Pl NE # 11990<br>
              Albuquerque, NM 87110<br>
              Estados Unidos
            </address>
          </div>
        </div>

        <div class="ct-row">
          <span class="sec-ico"><svg><use href="#i-msg"/></svg></span>
          <div>
            <span class="ct-label">Correo</span>
            <p class="ct-value">
              <a href="mailto:contact@silbrostrading.com">contact@silbrostrading.com</a>
            </p>
          </div>
        </div>

        <div class="ct-row">
          <span class="sec-ico"><svg><use href="#i-spark"/></svg></span>
          <div>
            <span class="ct-label">Acceso anticipado</span>
            <p class="ct-value">
              &Uacute;nete a la lista de espera y responde al correo que recibas
              &mdash; llega a la misma bandeja de entrada.
            </p>
          </div>
        </div>

      </div>

      <p class="mod-benefit">Leemos todo lo que llega.
         <b>Si vendes en Amazon, cu&eacute;ntanos con qu&eacute; est&aacute;s atascado</b>
         &mdash; ese es el feedback con el que se va formando el producto.</p>

      <p style="margin-top:var(--s4)">
        <a class="btn btn--primary btn--lg" href="#waitlist" data-waitlist-open data-source="contact" data-magnetic>
          &Uacute;nete a la lista de espera <svg class="icon-sm"><use href="#i-arrow"/></svg>
        </a>
      </p>
    </div>

    <figure class="mod-figure ct-figure">
      <img width="1000" height="1280" src="/assets/img/contact-message-loop.webp"
           alt="Mensajes de vendedores que llegan, convergen en un solo punto donde se leen y se convierten en el producto AmazeBase" decoding="async">
    </figure>

  </article>

</div>
</section>

</main>'''
