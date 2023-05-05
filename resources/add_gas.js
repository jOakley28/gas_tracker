// when a car is selected, get the phases for that car
function car_selected() {
    var car = document.getElementById('car_id').value;
    if (car) {
      get_phase_by_car(car);
    }
  }
  
  function get_phase_by_car(car) {
    fetch('/api/phase/' + car)
      .then(response => response.json())
      .then(data => {
        var phase = document.getElementById('phase');
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
  
        // enable the select
        phase.disabled = false;
  
        // set the last phase in the JSON list as the default value for phase input field
        var phaseInput = document.getElementById('phase');
  
        // update the label
        var phaseLabel = document.querySelector("label[for='phase']");
        phaseLabel.innerHTML = "Life Phase: currently: " + data[data.length - 1] + "";
  
        // update the placeholder
        phaseInput.placeholder = "Leave blank to continue or enter new phase here";
      });
  }
  
  // add event listener to select car field
  document.getElementById('car_id').addEventListener('change', car_selected);
