---
title: GVC Lab @ Great Bay University
layout: home
description: Generative & intelligent Visual Computing (GVC) Lab @ Great Bay University.
intro_image: "images/robot-film-crew-2023-white-v1.png"
intro_image_alt: "Hand-drawn robot filmmaking crew in the lab's 2023 illustration style"
intro_image_width: 1819
intro_image_height: 865
intro_image_absolute: true
intro_image_hide_on_mobile: false
show_call_box: false
show_news: true
show_fundings: true
---

<div class="hero-tagline">
  <h1 class="hero-mission">
    <span>Movies &amp; Games.</span>
    <em>A World Reimagined</em>
    <span>with AI.</span>
  </h1>
</div>

<style>
@font-face {
  font-family: "GVC Editorial";
  src: url("{{ '/assets/fonts/playfair-display-normal-latin.woff2' | relative_url }}") format("woff2");
  font-style: normal;
  font-weight: 500;
  font-display: swap;
}
@font-face {
  font-family: "GVC Editorial";
  src: url("{{ '/assets/fonts/playfair-display-italic-latin.woff2' | relative_url }}") format("woff2");
  font-style: italic;
  font-weight: 500;
  font-display: swap;
}
.hero-tagline {
  margin: 0;
  padding: 0.5rem 0;
}
.hero-mission {
  font-family: "GVC Editorial", Georgia, serif;
  font-size: clamp(2.5rem, 3.9vw, 3.4rem);
  font-weight: 500;
  line-height: 1.15;
  letter-spacing: -0.035em;
  color: #263d3d;
  margin: 0;
}
.hero-mission > span,
.hero-mission > em {
  display: block;
  white-space: nowrap;
}
.hero-mission em {
  font-style: italic;
  font-weight: inherit;
  color: var(--gvc-orange);
}
@media (max-width: 991px) {
  .hero-mission { font-size: clamp(2.375rem, 5.7vw, 3.25rem); }
}
@media (max-width: 420px) {
  .hero-mission { font-size: clamp(1.375rem, 8.7vw, 2.375rem); }
}
</style>
