document.querySelectorAll('.fa').forEach(elem => {
  elem.onmouseover = e => e.target.classList.toggle('hovered');
  elem.onmouseleave = e => e.target.classList.remove('hovered');
});