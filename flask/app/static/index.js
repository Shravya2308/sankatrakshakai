async function logMovies() {
    const response = await fetch("http://127.0.0.1:5000/getinfo");
    const movies = await response.json();
    console.log(movies);
  }