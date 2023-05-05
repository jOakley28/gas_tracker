const calculateButton = document.getElementById('calculate_button');
const carIdSelect = document.getElementById('car_id');
const tripLengthInput = document.getElementById('trip_length');
const resultsDiv = document.getElementById('results');

const calculateTripCost = () => {
  const carId = carIdSelect.value;
  const tripLength = tripLengthInput.value;
  if (!carId || !tripLength) {
    alert('Please select a car and enter a trip length');
    return;
  }

  fetch(`/api/trip_cost/${tripLength}/${carId}`)
    .then(response => response.json())
    .then(data => {
      const resultText = `Trip cost: $${data}`;
      resultsDiv.innerText = resultText;
    })
    .catch(error => {
      alert('An error occurred while calculating the trip cost.');
      console.error(error);
    });
};

calculateButton.addEventListener('click', calculateTripCost);

tripLengthInput.addEventListener('keyup', (event) => {
  if (event.key === 'Enter') {
    calculateTripCost();
  }
});
