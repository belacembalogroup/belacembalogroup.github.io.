// Casa Bela Cembalo, Atlántida - recibe las solicitudes de la página web
// y las envía por email a casabelacembalo@gmail.com desde la misma cuenta.
const DESTINO = 'casabelacembalo@gmail.com';

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p.web) return listo();                       // trampa anti-spam
  const t = v => String(v || '').trim().slice(0, 1000);
  const ci = t(p.ci), co = t(p.co), nombre = t(p.nombre), tel = t(p.tel), email = t(p.email);
  const fecha = /^\d{4}-\d{2}-\d{2}$/;
  if (!fecha.test(ci) || !fecha.test(co) || !nombre || !tel) return listo();

  const asunto = 'Solicitud de reserva directa - Casa Bela Cembalo, Atlántida: ' + ci + ' a ' + co;
  const cuerpo = [
    'Solicitud de reserva directa - Casa Bela Cembalo, Atlántida',
    'Canal elegido por el huésped: ' + (t(p.canal) || '-'),
    'Idioma: ' + ({ es: 'Español', en: 'English', pt: 'Português' }[t(p.idioma)] || 'Español'),
    '',
    'Llegada: ' + ci,
    'Salida: ' + co,
    'Noches: ' + t(p.noches),
    'Huéspedes: ' + t(p.huespedes),
    t(p.precio) || 'Precio noches: a confirmar',
    '',
    'Nombre: ' + nombre,
    'Teléfono: ' + tel,
    'Email: ' + (email || '-'),
    '',
    'Mensaje: ' + (t(p.mensaje) || '-'),
    '',
    'Enviado desde belacembalogroup.com/atlantida'
  ].join('\n');

  const opciones = { name: 'Web Casa Bela Cembalo' };
  if (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) opciones.replyTo = email;
  MailApp.sendEmail(DESTINO, asunto, cuerpo, opciones);
  return listo();
}

function listo() {
  return ContentService.createTextOutput('ok');
}
