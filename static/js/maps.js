// Create map
const map = L.map('map').setView([-1.286389, 36.817223], 13);

// Load map tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Marker
L.marker([-1.286389, 36.817223])
    .addTo(map)
    .bindPopup("Nairobi, Kenya")
    .openPopup();