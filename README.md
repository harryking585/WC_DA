# WC_DA

WC_DA is a full-stack data application that retrieves World of Warcraft
Mythic+ character data from Blizzard's API, transforms the API response
into an application-specific data model, calculates performance metrics,
and presents the results through a lightweight web interface.

The project focuses on turning a large, deeply nested third-party API
response into concise, useful information for an end user.

## Overview

World of Warcraft's Mythic+ system consists of increasingly difficult
timed dungeon runs. Player performance can be evaluated using
information such as completed difficulty levels, whether runs were
completed within the time limit, completion times, and overall Mythic+
rating.

WC_DA allows a user to enter a character name and realm and view a
summary of that character's Mythic+ performance alongside details about
individual dungeon runs.

The application currently presents:

-   Mythic+ rating
-   Highest completed key level
-   Timed runs
-   Percentage of runs completed within the time limit
-   Average key level
-   Average dungeon completion time
-   Individual dungeon results
-   Dungeon affixes
-   Party composition

## Architecture

WC_DA separates external data retrieval and analysis from presentation.

``` text
Blizzard API
     |
     v
FastAPI Backend
     |
     |-- OAuth authentication
     |-- API requests
     |-- Data transformation
     |-- Summary metric calculations
     |
     v
Application-Specific JSON
     |
     v
JavaScript Frontend
     |
     |-- Character summary
     |-- Performance metrics
     |-- Dungeon results
     |-- Expandable run details
     |
     v
User
```

Rather than sending Blizzard's original response directly to the
browser, the backend transforms the data into a smaller structure
designed specifically for WC_DA.

This keeps third-party API structure and analytical logic out of the
presentation layer and gives the frontend a consistent data contract to
consume.

## Data Transformation

A major focus of WC_DA is transforming Blizzard's nested API responses
into data that is easier to analyze and display.

For each Mythic+ run, the backend extracts relevant information
including:

-   Dungeon
-   Keystone level
-   Completion status
-   Duration
-   Affixes
-   Party members
-   Character specialization
-   Character race
-   Equipped item level

The backend then calculates aggregate statistics across the returned
runs.

For example, the frontend receives calculated summary information in a
structure similar to:

``` json
{
  "summary": {
    "highest_key": 12,
    "timed_runs": 7,
    "total_runs": 8,
    "timed_percentage": 87.5,
    "average_key_level": 9.75,
    "average_duration_minutes": 26.84
  }
}
```

This allows the frontend to focus on presentation rather than
interpreting Blizzard's underlying data model or recalculating
analytical metrics.

## API

### Character Mythic+ Data

``` http
GET /bestruns/{realm}/{name}
```

Retrieves and analyzes Mythic+ information for the specified character.

The response is organized into three primary sections:

-   `character` --- character information and Mythic+ rating
-   `summary` --- aggregate metrics calculated by WC_DA
-   `best_runs` --- normalized information about individual Mythic+
    dungeon runs

### Dungeon Pool

``` http
GET /dungeonpool
```

Retrieves information about the current Mythic+ dungeon pool.

### Realms

``` http
GET /realms
```

Retrieves available World of Warcraft realm information.

## Frontend

The frontend provides a lightweight interface for querying and reviewing
character performance.

After submitting a character name and realm, WC_DA displays a
performance summary followed by the character's individual dungeon runs.

The primary results table keeps the most useful information immediately
visible:

  Dungeon             Level  Completed     Duration Details
  ----------------- ------- ----------- ----------- --------------
  Example Dungeon        10     Yes       24.52 min View Details

Additional information such as dungeon affixes and party composition is
available through expandable run details rather than being displayed
directly in the primary table.

This keeps the interface readable while preserving access to the
underlying run data.

## Technology

### Backend

-   Python
-   FastAPI
-   Blizzard Battle.net API
-   OAuth 2.0

### Frontend

-   JavaScript
-   HTML
-   CSS

### Development

-   Git
-   GitHub
-   REST APIs
-   JSON

## Running Locally

### 1. Clone the repository

``` bash
git clone https://github.com/harryking585/WC_DA.git
cd WC_DA
```

### 2. Configure Blizzard API credentials

WC_DA requires Blizzard API credentials to authenticate with the
Battle.net API.

Create a `.env` file in the project directory:

``` env
CLIENT_ID=your_client_id
SECRET=your_client_secret
```

Replace the placeholder values with your Blizzard API credentials.

The `.env` file contains sensitive credentials and should not be
committed to source control.

### 3. Start the FastAPI backend

From the project directory, run:

``` bash
fastapi dev grabgoodies.py
```

The development server will run locally at:

``` text
http://127.0.0.1:8000
```

### 4. Open the frontend

Open `react/index.html` in your browser.

The frontend is configured to communicate with the local FastAPI backend
at:

``` javascript
const API_BASE_URL = "http://127.0.0.1:8000";
```

## Project Goals

WC_DA began as a way to retrieve and display World of Warcraft API data
and evolved into an exercise in designing a cleaner data pipeline
between an external API, application backend, and frontend.

Development has focused on:

-   Consuming and authenticating against an external REST API
-   Navigating and transforming deeply nested JSON responses
-   Separating data processing from presentation
-   Designing an application-specific API contract
-   Calculating aggregate metrics on the backend
-   Handling API and user-input failures
-   Presenting detailed data without overwhelming the primary interface

The project intentionally keeps the frontend relatively lightweight
while placing data retrieval, normalization, and analysis
responsibilities in the backend.

## Future Improvements

Potential future improvements include:

-   Deployment of the FastAPI backend and frontend
-   Improved character and realm validation
-   More specific handling of Blizzard API errors
-   Additional context for users unfamiliar with Mythic+
-   Historical or seasonal performance comparisons where suitable data
    is available

## Data Source

Character and Mythic+ data are retrieved from Blizzard Entertainment's
World of Warcraft APIs.

WC_DA is an independent project and is not affiliated with or endorsed
by Blizzard Entertainment.
