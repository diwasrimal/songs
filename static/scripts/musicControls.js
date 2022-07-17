let audio = document.querySelector("audio")

// Get all buttons
let play = document.querySelector('.fa-play')
let pause = document.querySelector('.fa-pause ')
let prev = document.querySelector('.fa-fast-backward')
let repeat = document.querySelector('.fa-repeat')
let next = document.querySelector('.fa-fast-forward')

// Controls

play.addEventListener('click', () => {
  audio.play()
  hide(play)
  show(pause)
})

pause.addEventListener('click', () => {
  audio.pause()
  hide(pause)
  show(play)
})

repeat.addEventListener('click', () => audio.currentTime = 0 )
prev.addEventListener('click', () => document.querySelector("#playPrev").submit())
next.addEventListener('click', () => document.querySelector("#playNext").submit())


// Show lyrics if wanted
let lyricsDiv = document.querySelector('#lyrics-div');
document.querySelector('#lyrics-shower').addEventListener('click', () => {
  if (lyricsDiv.style.display == 'none') {
    show(lyricsDiv);
  }
  else {
    hide(lyricsDiv);
  }
});

function hide(elem) {
  elem.style.display = 'none';
}
function show(elem) {
  elem.style.display = 'block';
}

function convertToMins(time) {
  time = Math.floor(time);

  let mins = Math.floor(time / 60);
  let secs = Math.floor(time  % 60);

  mins = (mins > 9) ? `${mins}` : `0${mins}`;
  secs = (secs > 9) ? `${secs}` : `0${secs}`;

  return  mins + ':' + secs;
}