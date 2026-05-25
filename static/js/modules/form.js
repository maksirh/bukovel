let _abortCtrl = null;

export function initForms() {
  if (_abortCtrl) _abortCtrl.abort();
  _abortCtrl = new AbortController();
  const { signal } = _abortCtrl;

  document.addEventListener('change', e => {
    if (e.target.matches('input[name="check_in"]')) {
      const checkIn = e.target;
      const form = checkIn.closest('form');
      const checkOut = form?.querySelector('input[name="check_out"]');
      if (checkOut && checkIn.value) {
        const minStr = addOneDay(checkIn.value);
        checkOut.min = minStr;
        if (checkOut.value && checkOut.value <= checkIn.value) {
          checkOut.value = minStr;
        }
      }
    }
  }, { signal });

  document.querySelectorAll('input[name="check_in"]').forEach(input => {
    input.min = todayLocal();
  });
}

function addOneDay(dateStr) {
  const [y, m, d] = dateStr.split('-').map(Number);
  const next = new Date(y, m - 1, d + 1);
  return [
    next.getFullYear(),
    String(next.getMonth() + 1).padStart(2, '0'),
    String(next.getDate()).padStart(2, '0'),
  ].join('-');
}

function todayLocal() {
  const d = new Date();
  return [
    d.getFullYear(),
    String(d.getMonth() + 1).padStart(2, '0'),
    String(d.getDate()).padStart(2, '0'),
  ].join('-');
}
