// Odeslani poptavkoveho formulare (ceska, anglicka i nemecka verze).
//
// Formular posila JSON pres fetch(), takze navstevnik zustane na strance.
// Pole "redirect" ve formulari je zalozni cesta pro prohlizec bez JavaScriptu —
// tam probehne klasicky POST a navrat zpet s ?sent=1.
//
// Access key je v HTML formulare, ne tady.
//
// Hlasky i predmet se ridi jazykem stranky (<html lang>). Hodnoty poli ctememe
// pres ID (f-name, f-email, …), protoze atribut name je v kazdem jazyce jiny —
// jde totiz rovnou do e-mailu jako popisek radku.

const JAZYK = (document.documentElement.lang || 'cs').slice(0, 2);

const HLASKY = {
  cs: {
    ok: 'Děkujeme! Poptávka odešla. Ozveme se do dvou pracovních dnů.',
    chyba: 'Odeslání se nepodařilo. Zkuste to prosím znovu, nebo nám zavolejte na +420 776 111 100.',
    odesilam: 'Odesílám…',
    predmet: 'Poptávka bfksystems.cz',
  },
  en: {
    ok: 'Thank you! Your enquiry has been sent. We reply within two working days.',
    chyba: 'Sending failed. Please try again, or call us on +420 776 111 100.',
    odesilam: 'Sending…',
    predmet: 'Enquiry bfksystems.cz',
  },
  de: {
    ok: 'Danke! Ihre Anfrage ist abgeschickt. Wir antworten innerhalb von zwei Arbeitstagen.',
    chyba: 'Das Senden ist fehlgeschlagen. Bitte versuchen Sie es erneut oder rufen Sie uns an: +420 776 111 100.',
    odesilam: 'Wird gesendet…',
    predmet: 'Anfrage bfksystems.cz',
  },
}[JAZYK] || null;

const T = HLASKY || {
  ok: 'Děkujeme! Poptávka odešla. Ozveme se do dvou pracovních dnů.',
  chyba: 'Odeslání se nepodařilo. Zkuste to prosím znovu, nebo nám zavolejte na +420 776 111 100.',
  odesilam: 'Odesílám…',
  predmet: 'Poptávka bfksystems.cz',
};

// Stav po navratu z externi sluzby (varianta bez JavaScriptu).
(function stavZUrl() {
  const params = new URLSearchParams(location.search);
  if (!params.has('sent')) return;
  const el = document.getElementById('contact-status');
  if (!el) return;
  const ok = params.get('sent') === '1';
  el.className = ok ? 'ok' : 'err';
  el.textContent = ok ? T.ok : T.chyba;
  el.scrollIntoView({ block: 'center' });
})();

// Predmet a reply-to doplnujeme az pred odeslanim, at jde notifikace rovnou
// zodpovedet zakaznikovi a v predmetu je videt, o co jde.
function doplnMetadata(form) {
  const podle = (id) => (form.querySelector(`#${id}`)?.value || '').trim();
  const nastav = (n, v) => { const el = form.querySelector(`input[name="${n}"]`); if (el && v) el.value = v; };

  const jmeno = podle('f-name');
  const zajem = podle('f-zajem') || podle('f-topic');   // cesky f-zajem, EN/DE f-topic
  const misto = podle('f-misto');                        // jen ceska verze

  nastav('replyto', podle('f-email'));
  nastav('subject', [T.predmet, zajem, misto, jmeno].filter(Boolean).join(' – '));
}

(function odeslani() {
  const form = document.getElementById('contact-form');
  if (!form) return;
  const status = document.getElementById('contact-status');
  const button = form.querySelector('button[type=submit]');
  const key = form.querySelector('input[name="access_key"]');

  if (!key || key.value.startsWith('PLACEHOLDER')) {
    console.warn('[bfksystems] Access key formuláře není vyplněný — formulář nic neodešle. '
      + 'Doplň ho v nastroje/obsah.py (FORMULAR) a spusť build.');
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const popisek = button.textContent;
    button.disabled = true;
    button.textContent = T.odesilam;
    status.className = '';
    status.textContent = '';

    doplnMetadata(form);

    try {
      // Nazvy poli maji diakritiku; z multipartu je nektere sluzby ctou jako
      // Latin-1 a v e-mailu je pak rozsypany caj. Z JSONu se prectou spravne.
      const pole = Object.fromEntries(new FormData(form).entries());
      const res = await fetch(form.action, {
        method: 'POST',
        headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify(pole),
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.success) {
        status.className = 'ok';
        status.textContent = T.ok;
        form.reset();
      } else {
        status.className = 'err';
        status.textContent = T.chyba;
        console.warn('[bfksystems] Odpověď služby:', res.status, data);
      }
    } catch (err) {
      status.className = 'err';
      status.textContent = T.chyba;
      console.warn('[bfksystems] Odeslání selhalo:', err);
    } finally {
      button.disabled = false;
      button.textContent = popisek;
      status.scrollIntoView({ block: 'center' });
    }
  });
})();
