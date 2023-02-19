// Seek and duration
// https://css-tricks.com/lets-create-a-custom-audio-player/

const displayDuration = () => {
  document.querySelector('#duration').innerText = convertToMins(audio.duration);
}

if (audio.readyState > 0) {
  displayDuration();
}
else {
  audio.addEventListener('loadedmetadata', () => {
    displayDuration();
  });
}

// Seek 5 seconds forward/backward with arrows
window.addEventListener('keydown', e => {
  if (e.keyCode == 39) audio.currentTime += 5;
  if (e.keyCode == 37) audio.currentTime -= 5;
})

// Show current time and progress

const time = document.querySelector("#currentTime")
const progress = document.querySelector("#progress-bar")

progress.addEventListener('change', () => {
  audio.currentTime = (progress.value / 100) * audio.duration;
  document.querySelector('#focusThis').focus()
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