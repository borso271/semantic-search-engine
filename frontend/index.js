let selectedAgeGroup = "low";
let selectedContentType = "pedia_article"; // Default content type

// Set age group filter and perform search
function setAgeGroup(ageGroup) {
    // Update selected age group
    selectedAgeGroup = ageGroup;

    // Update the active class on buttons
    const buttons = document.querySelectorAll(".filter-btn");
    buttons.forEach((button) => {
        if (button.innerText === ageGroup) {
            button.classList.add("active");
        } else {
            button.classList.remove("active");
        }
    });

    console.log(`Selected Age Group: ${selectedAgeGroup}`);
    // Perform search with the new age group filter
    performSearch();
}

// Set content type filter
function setContentType(contentType) {
    selectedContentType = contentType;
    console.log(`Selected Content Type: ${selectedContentType}`);
}

// Perform the search
async function performSearch() {
    const query = document.getElementById("query").value.trim();
    if (!query) {
        alert("Please enter a search query.");
        return;
    }

    try {
        // Build the request payload
        const payload = {
            query: query,
            age_group: selectedAgeGroup,
            content_type: selectedContentType,
        };

        // Send query to backend API
        const response = await fetch("http://127.0.0.1:8000/api/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Clear previous results
        const resultsContainer = document.getElementById("results");
        resultsContainer.innerHTML = "";

        // Handle no results
        if (!data.results || data.results.length === 0) {
            resultsContainer.innerHTML = "<p>No results found.</p>";
            return;
        }

        // Display results
        data.results.forEach((result) => {
            const resultItem = document.createElement("div");
            resultItem.classList.add("result-item");

            resultItem.innerHTML = `
                <div class="result-header">
                    <img src="${result.image_url}" alt="Image for ${result.title}" class="result-image">
                    <h3>${result.title} (${result.score.toFixed(2)})</h3>
                </div>
                <p>${result.description}</p>
                <p><strong>Type:</strong> ${result.type}</p>
                <a href="${result.url}" target="_blank">Read more</a>
            `;

            resultsContainer.appendChild(resultItem);
        });
    } catch (error) {
        console.error("Error fetching search results:", error);
        alert("An error occurred while fetching search results.");
    }
}


/*

let selectedAgeGroup = null;
let selectedContentType = "article"; // Default content type

// Set age group filter
function setAgeGroup(ageGroup) {
    selectedAgeGroup = ageGroup;
    console.log(`Selected Age Group: ${selectedAgeGroup}`);
}

// Set content type filter
function setContentType(contentType) {
    selectedContentType = contentType;
    console.log(`Selected Content Type: ${selectedContentType}`);
}

// Perform the search
async function performSearch() {
    const query = document.getElementById("query").value.trim();
    if (!query) {
        alert("Please enter a search query.");
        return;
    }

    try {
        // Build the request payload
        const payload = {
            query: query,
            ageGroup: selectedAgeGroup,
            contentType: selectedContentType,
        };

        // Send query to backend API
        const response = await fetch("http://127.0.0.1:8000/api/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Clear previous results
        const resultsContainer = document.getElementById("results");
        resultsContainer.innerHTML = "";

        // Handle no results
        if (!data.results || data.results.length === 0) {
            resultsContainer.innerHTML = "<p>No results found.</p>";
            return;
        }

       // Display results
    data.results.forEach((result) => {
    const resultItem = document.createElement("div");
    resultItem.classList.add("result-item");

    resultItem.innerHTML = `
        <div class="result-header">
            <img src="${result.image_url}" alt="Image for ${result.title}" class="result-image">
            <h3>${result.title} (${result.score.toFixed(2)})</h3>
        </div>
        <p>${result.description}</p>
        <p><strong>Type:</strong> ${result.type}</p>
        <a href="${result.url}" target="_blank">Read more</a>
    `;

    resultsContainer.appendChild(resultItem);
});

    } catch (error) {
        console.error("Error fetching search results:", error);
        alert("An error occurred while fetching search results.");
    }
}
*/
