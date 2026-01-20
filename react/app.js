const API_URL = "http://127.0.0.1:8000/";
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
document.getElementById("apiForm").addEventListener("submit", function (event) {
  event.preventDefault(); // stop page refresh

  // Get values from form
  const realm = document.getElementById("realm").value;
  const name = document.getElementById("name").value;

  // Build data object
  const payload = {
    realm: realm,
    name: name
  };

  // Send data to API
  fetch(`${API_URL}bestruns/${realm}/${name}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      document.getElementById("response").textContent =
        JSON.stringify(data, null, 2);
    })
    .catch(error => {
      console.error("Error:", error);
      document.getElementById("response").textContent =
        "Failed to send data to API.";
    });
});