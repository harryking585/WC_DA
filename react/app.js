const API_URL = "http://127.0.0.1:8000/";

function createTable(headers, rows) {
  const table = document.createElement("table");
  table.border = "1";

  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");

  headers.forEach(h => {
    const th = document.createElement("th");
    th.textContent = h;
    headerRow.appendChild(th);
  });

  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");

  rows.forEach(rowData => {
    const tr = document.createElement("tr");

    rowData.forEach(cell => {
      const td = document.createElement("td");

      if (cell instanceof HTMLElement) {
        td.appendChild(cell);
      } else {
        td.textContent = cell;
      }

      tr.appendChild(td);
    });

    tbody.appendChild(tr);
  });

  table.appendChild(tbody);
  return table;
}

function renderBestRuns(data) {
  const container = document.getElementById("response");
  container.innerHTML = "";

  let runs = null;

  // Handle different possible shapes
  if (Array.isArray(data)) {
    runs = data;
  } else if (data && Array.isArray(data.best_runs)) {
    runs = data.best_runs;
  }

  if (!runs || !runs.length) {
    container.innerHTML = "<p>No data available</p>";
    return;
  }

  const mainHeaders = [
    "Dungeon",
    "Level",
    "Completed",
    "Duration (min)",
    "Affixes",
    "Members"
  ];

  const mainRows = runs.map(run => {
    const dungeonName = run.dungeon?.name?.en_US || "Unknown";

    const duration = (run.duration / 60000).toFixed(2);

    const completed = run.is_completed_within_time ? "Yes" : "No";

    // Affixes table
    const affixRows = run.keystone_affixes.map(a => [
      a.name.en_US
    ]);

    const affixTable = createTable(["Affix"], affixRows);

    // Members table
    const memberRows = run.members.map(m => [
      m.character.name,
      m.character.realm.slug,
      m.specialization.name.en_US,
      m.race.name.en_US,
      m.equipped_item_level
    ]);

    const memberTable = createTable(
      ["Name", "Realm", "Spec", "Race", "iLvl"],
      memberRows
    );

    return [
      dungeonName,
      run.keystone_level,
      completed,
      duration,
      affixTable,
      memberTable
    ];
  });

  const mainTable = createTable(mainHeaders, mainRows);
  container.appendChild(mainTable);
}

document.getElementById("apiForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const realm = document.getElementById("realm").value;
  const name = document.getElementById("name").value;

  fetch(`${API_URL}bestruns/${realm}/${name}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log("RAW DATA:", data);

      
      if (typeof data === "string") {
        data = JSON.parse(data);
      }

      console.log("PARSED DATA:", data);

      renderBestRuns(data);
    })
    .catch(error => {
      console.error("Error:", error);
      document.getElementById("response").textContent =
        "Failed to fetch data.";
    });
});