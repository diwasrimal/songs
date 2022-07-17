const favorites = document.querySelectorAll('.fa-heart');

let songIds = [];
document.querySelectorAll('.songId').forEach(elem => songIds.push(elem.value));

// When clicked on favorites
// Send a request to /favorites to add/remove song to/from favorites 

for (let i = 0; i < favorites.length; i++) {

  favBtn = favorites[i];

  favBtn.onclick = (e) => {

    const target = e.target;

    // Toggle favorites button on off
    target.classList.remove("hovered");
    target.classList.toggle('clicked');

    // Fetch data to /favorites
    const data = {songId : songIds[i]};

    fetch('/favorites', {
      method: 'POST', // or 'PUT'
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })

    .then(response => response.text())

    .then(text => {
      console.log('Success:', text)
    })

    .catch((error) => {
      console.error('Error:', error);
    });
  }
}
