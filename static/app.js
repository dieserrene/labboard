fetch("/api/servers")
  .then(antwort => antwort.json())
  .then(daten => {
    document.getElementById("serverliste").textContent =
      JSON.stringify(daten, null, 2);
  });
