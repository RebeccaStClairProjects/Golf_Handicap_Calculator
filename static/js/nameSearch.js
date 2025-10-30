// static/js/nameSearch.js

const golferSerch = document.getElementById("golferSerch");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const form = document.getElementById("golferSerch");

const addRoundFormEl = document.getElementById("addRoundForm");
const statusOptionsEl = document.getElementById("statusOptions");
const tryOtherOptionsEl = document.getElementById("tryOtherOptions");

const MODE = document.body.dataset.mode; // "addRound" or "addGolfer"

function showSection(id) {
    document.querySelectorAll("main > section").forEach(sec => sec.hidden = true);
    document.getElementById(id).hidden = false;
}

function populateAddForm(golfer) {
    // golfer = { golferID, firstName, lastName }
    document.getElementById("FirstName").value = golfer.firstName || "";
    document.getElementById("LastName").value = golfer.lastName || "";
    if (golfer.golferID) {
        document.getElementById("GolferID").value = golfer.golferID || "";
    }
}




const onExactMatch = {
    addRound(golfer) {
        // Prefill & show the round form
        showSection("matchFound");
        populateAddForm(golfer);
    },

    addGolfer(golfer) {
        // Tell user they already exist; offer to switch to “Add Round”
        showSection("matchFound");
        const optionsEL = document.getElementById("options")
        const box = document.getElementById("resultMessage");
        if (box) {
            box.innerHTML = `
        <p><strong>${golfer.firstName} ${golfer.lastName}</strong> is already in the system.</p>
      `;
            buildButtonAddNewRound(golfer, optionsEL)
            buildButtonTryAgain(optionsEL)
        }
    }
};

// Grab things that might not exist on every page
const holeCountEl = document.getElementById("holeCount");

// Only attach listeners when the element actually exists
if (holeCountEl) {
    holeCountEl.addEventListener("change", (e) => {
        const value = e.target.value;
        const extras = document.querySelectorAll(".extra-holes");
        if (value === "18") {
            extras.forEach(hole => hole.hidden = false);
            document.getElementById("holesContainer")?.classList.add("eighteen-col");
        } else {
            extras.forEach(hole => hole.hidden = true);
            document.getElementById("holesContainer")?.classList.remove("eighteen-col");
        }
    });
}

// Grab things that might not exist on every page
const preExistingInformationEl = document.getElementById("preExistingInformation");

// Only attach listeners when the element actually exists
if (preExistingInformationEl) {
    preExistingInformationEl.addEventListener("change", (e) => {
        const value = e.target.value;
        const extras = document.querySelectorAll(".extra-info");
        if (value === "True") {
            extras.forEach(hole => hole.hidden = false);
            document.getElementById("ExistingInformation")?.classList.add("eighteen-col");
        } else {
            extras.forEach(hole => hole.hidden = true);
            document.getElementById("ExistingInformation")?.classList.remove("eighteen-col");
        }
    });
}

const onCloseMatches = {
    addRound(candidates) {
        showSection("CloseMatches");
        statusOptionsEl.textContent = "Were you looking for one of these golfers?";
        renderCandidateButtons(candidates, g => {
            showSection("matchFound");
            populateAddForm(g);            
        });
        tryOtherOptionsEl.textContent = "If none of them are right, you can try one of the following options";        
        const optionsEL = document.getElementById("otherOptions")
        optionsEL.innerHTML = "";
        buildButtonTryAgain(optionsEL)
        buildButtonAddNewGolfer(optionsEL)
    },
    addGolfer(candidates) {
        showSection("CloseMatches");
        statusOptionsEl.textContent = "Were you looking for one of these golfers?";
        renderCandidateButtons(candidates, g => {
            showSection("matchFound");
            const optionsEL = document.getElementById("options")
            const box = document.getElementById("resultMessage");
            if (box) {
                box.innerHTML = `
        <p><strong>${g.firstName} ${g.lastName}</strong> is already in the system.</p>
      `;
                buildButtonAddNewRound(g, optionsEL)
                buildButtonTryAgain(optionsEL)
            }
        });
        tryOtherOptionsEl.textContent = "If none of them are right, you can try one of the following options";
        const optionsEL = document.getElementById("otherOptions")
        optionsEL.innerHTML = "";
        buildButtonTryAgain(optionsEL)
        buildButtonAddNewGolfer(optionsEL)
    }
};


function renderCandidateButtons(candidates, onPick) {
    const list = document.getElementById("candidateList");
    if (!list) return;
    list.innerHTML = "";
    const arr = Array.isArray(candidates) ? candidates : [];
    if (arr.length === 0) {
        list.textContent = "No close matches.";
        return;
    }
    arr.forEach(g => {
        const btn = document.createElement("button");
        btn.className = "candidate-btn";
        btn.textContent = `${g.firstName} ${g.lastName}`;
        btn.addEventListener("click", () => onPick(g));
        list.appendChild(btn);
    });
}

function buildButtonAddNewGolfer(optionsEL) {
    const addNew = document.createElement("button");
    addNew.textContent = "Add New Golfer";
    addNew.classList.add("candidate-btn"); // optional styling reuse
    addNew.addEventListener("click", () => {
        // save what the next page needs
        localStorage.setItem("prefill", JSON.stringify({
            mode: "addGolfer",
            section: "noMatches",
            firstName: lastSearchData.firstName || "",
            lastName: lastSearchData.lastName || "",
        }));

        // then navigate
        window.location.href = "/addGolfer";
    });
    optionsEL.appendChild(addNew);
}
function buildButtonAddNewRound(golfer, optionsEL) {
    const addNew = document.createElement("button");
    addNew.textContent = "Add New Round";
    addNew.classList.add("candidate-btn"); // optional styling reuse
    addNew.addEventListener("click", () => {
        // save what the next page needs
        localStorage.setItem("prefill", JSON.stringify({
            mode: "addRound",
            section: "matchFound",
            firstName: golfer.firstName || "",
            lastName: golfer.lastName || "",
            golferID: golfer.golferID || "",
        }));

        // then navigate
        window.location.href = "/addRound";
    });
    optionsEL.appendChild(addNew);
}
function buildButtonTryAgain(optionsEL) {
    const tryNew = document.createElement("button");
    tryNew.textContent = "Try A New Serch";
    tryNew.classList.add("candidate-btn"); // optional styling reuse
    tryNew.addEventListener("click", () => {
        window.location.reload();  // Reaload the curent page
    });
    optionsEL.appendChild(tryNew);
}


document.addEventListener("DOMContentLoaded", () => {
    const raw = localStorage.getItem("prefill");
    if (!raw) return;

    try {
        const pf = JSON.parse(raw);
        if (pf.mode === "addGolfer") {
            // show the requested section
            showSection(pf.section || "noMatches");

            // prefill the form
            document.getElementById("FirstName").value = pf.firstName || "";
            document.getElementById("LastName").value = pf.lastName || "";
        }
        else if (pf.mode === "addRound") {
            // show the requested section
            showSection(pf.section || "matchFound");

            // prefill the form
            document.getElementById("FirstName").value = pf.firstName || "";
            document.getElementById("LastName").value = pf.lastName || "";
            document.getElementById("GolferID").value = pf.golferID || "";
        }
    } finally {
        // clear so refreshes don’t keep reapplying it
        localStorage.removeItem("prefill");
    }
});




const onNoMatch = {
    addRound() {
        showSection("noMatches");
        // optional: offer a button to navigate to Add Golfer page
        const optionsEL = document.getElementById("options")
        buildButtonTryAgain(optionsEL)
        buildButtonAddNewGolfer(optionsEL)
    },
    addGolfer() {
        showSection("noMatches");
        populateAddForm(lastSearchData);
    }
};










let lastSearchData = {};

document.getElementById("golferSerch").addEventListener("submit", async (e) => {
    e.preventDefault();

    lastSearchData = Object.fromEntries(new FormData(form));

    try {
        const res = await fetch("/golferSerch", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(lastSearchData)
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
                onExactMatch[MODE](golfer.golfer);
                break;
            case 2:
                onCloseMatches[MODE](golfer.candidates);
                break;
            case 3:
                onNoMatch[MODE]();
                break;
            default: console.error("Unexpected results:", golfer);
        }
    } catch (err) {
        // Only true network/JS errors should reach here
        showClientError(`Network or client error: ${String(err)}`);
    }

});

const holeInputs = document.querySelectorAll('.hole-score');

holeInputs.forEach(input => {
    input.addEventListener('input', () => {
        input.classList.remove('grayed-default');
    });
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