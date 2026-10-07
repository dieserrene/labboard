fetch("/api/servers")
  .then(antwort => antwort.json())
  .then(daten => {
    const tabelle = document.getElementById("serverliste");
    daten.forEach(server => {
      const zeile = document.createElement("tr");
      zeile.innerHTML = `
        <td>${server.name}</td>
        <td>${server.hostname}</td>
        <td>${server.ip_address}</td>
        <td>${server.environment}</td>
      `;
      tabelle.appendChild(zeile);
    });
  });
