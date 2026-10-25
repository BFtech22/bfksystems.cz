// Stridani fotek v uvodnim banneru.
//
// Snimky lezi na sobe v .hero .photo, prepina se trida "je-videt" a prolnuti
// resi CSS. Pri zapnutem omezeni pohybu v systemu zustane prvni fotka staticka.
(function heroStridani() {
  const snimky = document.querySelectorAll('.hero .photo .snimek');
  if (snimky.length < 2) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const PRODLEVA = 6000;
  let aktualni = 0;

  setInterval(() => {
    // Na skryte zalozce se neprepina, at se zbytecne nedekoduji obrazky.
    if (document.hidden) return;
    snimky[aktualni].classList.remove('je-videt');
    aktualni = (aktualni + 1) % snimky.length;
    snimky[aktualni].classList.add('je-videt');
  }, PRODLEVA);
})();
