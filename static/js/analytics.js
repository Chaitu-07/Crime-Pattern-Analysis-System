const data = window.analyticsData;

// =======================
// Chart Data
// =======================

const crimeLabels = data.crimeLabels;
const crimeValues = data.crimeValues;

const statusLabels = data.statusLabels;
const statusValues = data.statusValues;

const monthLabels = data.monthLabels;
const monthValues = data.monthValues;

const districtLabels = data.districtLabels;
const districtValues = data.districtValues;

// =======================
// Crime Types
// =======================

new Chart(document.getElementById("crimeChart"), {

    type: "bar",

    data: {

        labels: crimeLabels,

        datasets: [{

            label: "Crime Types",

            data: crimeValues,

            backgroundColor: "#0d6efd"

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false

    }

});

// =======================
// Crime Status
// =======================

new Chart(document.getElementById("statusChart"), {

    type: "pie",

    data: {

        labels: statusLabels,

        datasets: [{

            data: statusValues,

            backgroundColor: [

                "#198754",

                "#dc3545",

                "#ffc107",

                "#0dcaf0",

                "#6f42c1"

            ]

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false

    }

});

// =======================
// Monthly Crimes
// =======================

new Chart(document.getElementById("monthChart"), {

    type: "line",

    data: {

        labels: monthLabels,

        datasets: [{

            label: "Monthly Crimes",

            data: monthValues,

            borderColor: "#fd7e14",

            backgroundColor: "rgba(253,126,20,0.2)",

            fill: true,

            tension: 0.4

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false

    }

});

// =======================
// Top Districts
// =======================

new Chart(document.getElementById("districtChart"), {

    type: "bar",

    data: {

        labels: districtLabels,

        datasets: [{

            label: "Top Districts",

            data: districtValues,

            backgroundColor: "#dc3545"

        }]

    },

    options: {

        indexAxis: "y",

        responsive: true,

        maintainAspectRatio: false

    }

});

// =======================
// Crime Map
// =======================

const map = L.map("crimeMap").setView([20.5937, 78.9629], 5);

L.tileLayer(

    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

    {

        maxZoom: 19,

        attribution: "© OpenStreetMap"

    }

).addTo(map);

// Get locations from analyticsData
const locations = data.locations;

locations.forEach(location => {

    L.marker([location.lat, location.lng])

        .addTo(map)

        .bindPopup(

            `<b>${location.crime}</b><br>
             ${location.district}<br>
             Status: ${location.status}`

        );

});