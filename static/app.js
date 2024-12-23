document.addEventListener('DOMContentLoaded', () => {
    // Fetch the autocomplete data for Departure Place
    fetch('/get_places?type=departure')
        .then((response) => response.json())
        .then((data) => {
            $("#departure-place").autocomplete({
                source: data,
                minLength: 1, // Minimum characters to trigger autocomplete
                autoFocus: true, // Highlight the first item
                delay: 200 // Delay for fetching suggestions
            });
        });

    // Fetch the autocomplete data for Arrival Place
    fetch('/get_places?type=arrival')
        .then((response) => response.json())
        .then((data) => {
            $("#arrival-place").autocomplete({
                source: data,
                minLength: 1, // Minimum characters to trigger autocomplete
                autoFocus: true, // Highlight the first item
                delay: 200 // Delay for fetching suggestions
            });
        });

    // Handle form submission
    document.getElementById('flight-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const flightNumber = document.getElementById('flight-number').value;
        const departureDate = document.getElementById('departure-date').value;
        const departurePlace = document.getElementById('departure-place').value;
        const arrivalPlace = document.getElementById('arrival-place').value;

        // Send data to the backend
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                flight_number: flightNumber,
                departure_date: departureDate,
                departure_place: departurePlace,
                arrival_place: arrivalPlace
            })
        });

        const data = await response.json();

        // Debugging: Log the backend response
        console.log("Backend Response:", data);

        // Populate the table with flight details
        document.getElementById('td-flight-number').textContent = data.flight_number;
        document.getElementById('td-airline').textContent = data.airline;
        document.getElementById('td-airplane').textContent = data.airplane;
        document.getElementById('td-departure-time').textContent = data.departure_time;
        document.getElementById('td-arrival-time').textContent = data.arrival_time;
        document.getElementById('td-origin').textContent = data.origin;
        document.getElementById('td-destination').textContent = data.destination;
        document.getElementById('td-ranking').textContent = data.ranking || "Not Available";
        document.getElementById('td-arrival-delay').textContent = data.predicted_arrival_delay || "Not Available";
        document.getElementById('td-flight-delay').textContent = data.flight_delay || "Not Available";


        // Show the table
        document.getElementById('flight-details').style.display = 'block';
    });
});
