document.addEventListener('DOMContentLoaded', () => {
  const clearBtn = document.getElementById('clearInput');
  const outBox = document.getElementById('outBox');
  const dl = document.getElementById('dlTxt');

  if (clearBtn){
    clearBtn.addEventListener('click', () => {
      const ta = document.querySelector('form textarea[name="text"]');
      if (ta){ ta.value = ''; ta.focus(); }
    });
  }

  if (dl && outBox){
    dl.addEventListener('click', () => {
      if (!outBox.value.trim()) return;
      const blob = new Blob([outBox.value], {type: 'text/plain;charset=utf-8'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = 'swissified.txt';
      document.body.appendChild(a); a.click();
      URL.revokeObjectURL(url); a.remove();
    });
  }
});
