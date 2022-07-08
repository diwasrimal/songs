let audio = document.querySelector("audio")

// Get all buttons
let play = document.querySelector('.fa-play')
let pause = document.querySelector('.fa-pause ')
let prev = document.querySelector('.fa-fast-backward')
let repeat = document.querySelector('.fa-repeat')
let next = document.querySelector('.fa-fast-forward')
let favorite = document.querySelector('.fa-heart')

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

document.querySelector('#currentTime').addEventListener("click", () => console.log(audio.currentTime))

// Seek

let progress = document.querySelector('#progress');
let time = document.querySelector('#currentTime')

document.querySelector('#duration').innerText = convertToMins(audio.duration)

// Show current time


progress.addEventListener('change', () => {
  audio.currentTime = (progress.value / 100) * audio.duration;
  time.innerText = convertToMins(audio.currentTime)
});

const clock = setInterval(() => {
  if (document.activeElement != progress) {
    progress.value = (audio.currentTime / audio.duration) * 100;
    time.innerText = convertToMins(audio.currentTime)
  }
}, 0);

const clock2 = setInterval(() => {
  try {
    const percent = (audio.buffered.end(0) / audio.duration) * 100;
    // document.getElementById("loadingProgress").innerText = `Loading : ${percent.toFixed(2)}%`;
    if (percent >= 100) {
      clearInterval(clock2);
    }
  }
  catch (e) {
    console.log(e)
  }
})

function hide(elem) {
  elem.style.display = 'none'
}
function show(elem) {
  elem.style.display = 'block'
}

function convertToMins(time) {
  time = Math.floor(time);

  let mins = Math.floor(time / 60);
  let secs = Math.floor(time  % 60);

  mins = (mins > 9) ? `${mins}` : `0${mins}`;
  secs = (secs > 9) ? `${secs}` : `0${secs}`;

  return  mins + ':' + secs;
}
