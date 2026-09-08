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

function renderSummary(data) {
  const container = document.getElementById("response");

  const character = data?.character;
  const summary = data?.summary;

  if (!character || !summary) {
    return;
  }

  const heading = document.createElement("h2");
  heading.textContent = `${character.name} - ${character.realm}`;

  const rating = document.createElement("p");
  rating.textContent = `Mythic+ Rating: ${character.mythic_rating}`;

  const summaryTable = createTable(
    [
      "Highest Key",
      "Timed Runs",
      "Timed %",
      "Average Key",
      "Average Duration"
    ],
    [[
      summary.highest_key,
      `${summary.timed_runs} / ${summary.total_runs}`,
      `${summary.timed_percentage}%`,
      summary.average_key_level,
      `${summary.average_duration_minutes} min`
    ]]
  );

  container.appendChild(heading);
  container.appendChild(rating);
  container.appendChild(summaryTable);
}

function renderBestRuns(data) {
  const container = document.getElementById("response");
  container.innerHTML = "";

  renderSummary(data);

  const runs = data?.best_runs;

  if (!runs || !runs.length) {
    container.innerHTML += "<p>No run data available</p>";
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
    const completed = run.completed_within_time ? "Yes" : "No";

    // Affixes table
    const affixRows = run.affixes.map(affix => [
      affix
    ]);

    const affixTable = createTable(["Affix"], affixRows);

    // Members table
    const memberRows = run.members.map(member => [
      member.name,
      member.realm,
      member.specialization,
      member.race,
      member.item_level
    ]);

    const memberTable = createTable(
      ["Name", "Realm", "Spec", "Race", "iLvl"],
      memberRows
    );

    return [
      run.dungeon,
      run.keystone_level,
      completed,
      run.duration_minutes.toFixed(2),
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

      renderBestRuns(data);
    })
    .catch(error => {
      console.error("Error:", error);
      document.getElementById("response").textContent =
        "Failed to fetch data.";
    });
});