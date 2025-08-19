var map = L.map('map').setView([20, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('update', function(data) {
  // Clear map markers
  map.eachLayer(function (layer) {
    if (layer instanceof L.Marker) {
      map.removeLayer(layer);
    }
  });

  // Update map
  data.positions.forEach(function(pos) {
    L.marker([pos.lat, pos.lon])
      .bindPopup("Aircraft ID: " + pos.id + "<br>Altitude: " + pos.alt + " m")
      .addTo(map);
  });

  // Update collision table
  var collisionTable = document.getElementById("collision-table").getElementsByTagName('tbody')[0];
  collisionTable.innerHTML = '';
  data.collisions.forEach(function(collision) {
    var row = collisionTable.insertRow();
    row.insertCell(0).innerHTML = collision.aircraft1;
    row.insertCell(1).innerHTML = collision.aircraft2;
    row.insertCell(2).innerHTML = collision.distance;
    row.insertCell(3).innerHTML = collision.altitude_diff;
    row.insertCell(4).innerHTML = collision.time_to_collision;
  });

  // Update flight details
  var flightTable = document.getElementById("flight-details").getElementsByTagName('tbody')[0];
  flightTable.innerHTML = '';
  data.positions.forEach(function(pos) {
    var row = flightTable.insertRow();
    row.insertCell(0).innerHTML = pos.id;
    row.insertCell(1).innerHTML = pos.lat;
    row.insertCell(2).innerHTML = pos.lon;
    row.insertCell(3).innerHTML = pos.alt;
    row.insertCell(4).innerHTML = pos.velocity;
    row.insertCell(5).innerHTML = pos.course;
  });
});
