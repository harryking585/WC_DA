const API_URL = "http://127.0.0.1:8000/";


function renderTable(data) {
  const container = document.getElementById("response");
  container.innerHTML = "";

  // Handle empty data
  if (!data || (Array.isArray(data) && data.length === 0)) {
    container.innerHTML = "<p>No data available</p>";
    return;
  }

  // If it's not an array, make it one
  if (!Array.isArray(data)) {
    data = [data];
  }

  const table = document.createElement("table");
  table.border = "1";

  const headers = Object.keys(data[0]);

  // Header
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");

  headers.forEach(key => {
    const th = document.createElement("th");
    th.textContent = key;
    headerRow.appendChild(th);
  });

  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Body
  const tbody = document.createElement("tbody");

  data.forEach(rowObj => {
    const row = document.createElement("tr");

    headers.forEach(key => {
      const td = document.createElement("td");

      // Handle nested objects nicely
      const value = rowObj[key];
      td.textContent =
        typeof value === "object" ? JSON.stringify(value) : value;

      row.appendChild(td);
    });

    tbody.appendChild(row);
  });

  table.appendChild(tbody);
  container.appendChild(table);
}                  


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
      // console.log("Hello, World!");
      // const bestruns = JSON.parse(data);
      // console.log("LENGTH OF PARSED API DATA" + bestruns.length);
      const parsedData = JSON.parse(data);
      const meatyData = JSON.parse(parsedData[1]);

      renderTable(meatyData);
        //JSON.parse(data);
    })
    .catch(error => {
      console.error("Error:", error);
      document.getElementById("response").textContent =
        "Failed to send data to API.";
    });
});