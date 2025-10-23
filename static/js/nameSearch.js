// static/js/nameSearch.js

const golferSerch = document.getElementById("golferSerch");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const form = document.getElementById("golferSerch");

const addRoundFormEl = document.getElementById("addRoundForm");
const statusOptionsEl = document.getElementById("statusOptions");

function showSection(id) {
    document.querySelectorAll("main > section").forEach(sec => sec.hidden = true);
    document.getElementById(id).hidden = false;
}

function populateAddForm(golfer) {
    // golfer = { golferID, firstName, lastName }
    document.getElementById("FirstName").value = golfer.firstName || "";
    document.getElementById("LastName").value = golfer.lastName || "";
    document.getElementById("GolferID").value = golfer.golferID || "";

    // now show the form section
    showSection("matchFound");
}

document.getElementById("golferSerch").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(form));

    try {
        const res = await fetch("/golferSerch", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const contentType = res.headers.get("content-type") || "";
        let body;
        try {
            body = contentType.includes("application/json")
                ? await res.json()
                : await res.text();
        } catch {
            body = await res.text().catch(() => "");
        }

        if (!res.ok) {
            const msg = (body && body.message) || (typeof body === "string" ? body : "");
            showServerError(`Error ${res.status}${msg ? `: ${msg}` : ""}`);
            return;                    // do NOT fall through
        }

        const golfer = typeof body === "string" ? JSON.parse(body) : body;
        console.log("API response:", golfer);

        switch (Number(golfer.results)) {
            case 1:
                populateAddForm(golfer);
                break;

            case 2: {
                showSection("CloseMatches");
                statusOptionsEl.textContent = "Close matches found!";
                const candidatesContainer = document.getElementById("candidateList");
                candidatesContainer.innerHTML = "";

                (golfer.candidates || []).forEach(g => {
                    const btn = document.createElement("button");
                    btn.textContent = `${g.firstName} ${g.lastName}`;
                    btn.classList.add("candidate-btn");
                    btn.addEventListener("click", () => {
                        // Use the **selected candidate**, not the whole response
                        populateAddForm(g);
                    });
                    candidatesContainer.appendChild(btn);
                });

                if (!golfer.candidates || golfer.candidates.length === 0) {
                    candidatesContainer.textContent = "No close matches.";
                }
                break;
            }

            case 3:
                showSection("noMatches"); 
                resultEl.textContent = "Would you like to add a new golfer?";
                break;

            default:
                statusEl.textContent = "Unexpected response.";
                resultEl.textContent = JSON.stringify(golfer, null, 2);
        }
    } catch (err) {
        // Only true network/JS errors should reach here
        showClientError(`Network or client error: ${String(err)}`);
    }

});

document.getElementById("holeCount").addEventListener("change", (e) => {
    const value = e.target.value;
    const extras = document.querySelectorAll(".extra-holes");

    if (value === "18") {
        extras.forEach(hole => hole.hidden = false);  // show holes 10–18
        document.getElementById("holesContainer").classList.add("eighteen-col");
    } else {
        extras.forEach(hole => hole.hidden = true);   // hide them again
        document.getElementById("holesContainer").classList.remove("eighteen-col");
    }
});

function showServerError(text) {
    // Ensure this section + element exist in your HTML:
    // <section id="ErrorDisplay" class="card" hidden>
    //   <div id="errorMessage"></div>
    // </section>
    showSection("ErrorDisplay");
    const box = document.getElementById("errorMessage") || document.getElementById("result");
    if (box) box.textContent = text;
}

function showClientError(text) {
    showSection("ErrorDisplay");
    const box = document.getElementById("errorMessage") || document.getElementById("result");
    if (box) box.textContent = text;
}