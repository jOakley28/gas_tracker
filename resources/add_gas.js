// when a car is selected, get the phases for that car
function phase_by_car() {
    var phase = document.getElementById('car_id');
    //enable select phase dropdown 
    phase.disabled = false;    
    console.log(phase) 
  
    var phase = document.getElementById('car_id').value; 
    // enable the select   
    if (phase) {
        get_phase_by_car(phase, car_id);
    }
  }
  
  function get_phase_by_car(phase, car_id) {
    fetch('/api/phase/' + car_id)
        .then(response => response.json())
        .then(data => {
            console.log(phase)
            // clear out the existing options
            phase.innerHTML = '';
            // add the placeholder option 
            var option = document.createElement('option');
            option.value = '';
            option.text = 'Select phase';
            phase.appendChild(option);
  
            // add the new options
            for (var i = 0; i < data.length; i++) { 
                var option = document.createElement('option');
                option.value = data[i];
                option.text = data[i];
                phase.appendChild(option);
            }
        }
    );
  }