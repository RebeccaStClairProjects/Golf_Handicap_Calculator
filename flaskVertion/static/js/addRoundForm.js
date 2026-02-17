const addRoundForm = document.getElementById("addRoundForm");
const addRoundFields = document.getElementById("addRoundFields");
const addRoundCard = document.getElementById("addRoundCard");

const firstNameEl = document.getElementById("firstName");
const lastNameEl = document.getElementById("lastName");
const golferIdEl = document.getElementById("GolferID");
const nameCheckStatusEl = document.getElementById("nameCheckStatusRound");
const saveRoundBtnEl = document.getElementById("saveRoundBtn");
const roundSavedCardEl = document.getElementById("roundSavedCard");
const roundSavedMessageEl = document.getElementById("roundSavedMessage");
const savedHandicapEl = document.getElementById("savedHandicap");
const savedScoreDifferEl = document.getElementById("savedScoreDiffer");
const savedRoundsPlayedEl = document.getElementById("savedRoundsPlayed");
const savedRoundAvgEl = document.getElementById("savedRoundAvg");
const savedSeasonTotalEl = document.getElementById("savedSeasonTotal");
const addAnotherRoundBtnEl = document.getElementById("addAnotherRoundBtn");

const holeCountEl = document.getElementById("holeCount");
const holesContainerEl = document.getElementById("holesContainer");
const corseSelectEl = document.getElementById("corseID");
const teeSelectEl = document.getElementById("teeID");
const courseDataEl = document.getElementById("courseData");

const missingGolferModalEl = document.getElementById("missingGolferModal");
const missingGolferMessageEl = document.getElementById("missingGolferMessage");
const tryDifferentRoundNameBtn = document.getElementById("tryDifferentRoundNameBtn");
const addGolferFromRoundBtn = document.getElementById("addGolferFromRoundBtn");

const LOCKED_CLASS = "is-locked";
const DEBOUNCE_MS = 1000;

let debounceTimer = null;
let requestToken = 0;
let nameCheckEnabled = false;
let missingModalKey = "";
let exactMatchGolfer = null;
let courses = [];
let isSubmittingRound = false;

function normalizeInputName(value) {
    return (value || "").trim();
}

function setNameCheckStatus(text) {
    nameCheckStatusEl.textContent = text || "";
}

function hideMissingGolferModal() {
    missingGolferModalEl.hidden = true;
}

function showMissingGolferModal(firstName, lastName) {
    const key = `${firstName.toLowerCase()}|${lastName.toLowerCase()}`;
    if (missingModalKey === key && !missingGolferModalEl.hidden) {
        return;
    }
    missingModalKey = key;
    missingGolferMessageEl.textContent =
        `${firstName} ${lastName} could not be found. Would you like to try a different name or add this golfer?`;
    missingGolferModalEl.hidden = false;
}

function lockRoundForm() {
    addRoundFields.disabled = true;
    saveRoundBtnEl.disabled = true;
    addRoundCard.classList.add(LOCKED_CLASS);
}

function unlockRoundForm() {
    addRoundFields.disabled = false;
    saveRoundBtnEl.disabled = false;
    addRoundCard.classList.remove(LOCKED_CLASS);
}

function clearGolferMatch() {
    exactMatchGolfer = null;
    golferIdEl.value = "";
}

function applyExactMatch(golfer) {
    exactMatchGolfer = golfer;
    golferIdEl.value = golfer.golferID || "";
    hideMissingGolferModal();
    unlockRoundForm();
    setNameCheckStatus("Golfer found.");
}

function applyNoExactMatch(firstName, lastName) {
    clearGolferMatch();
    lockRoundForm();
    setNameCheckStatus("Golfer not found.");
    showMissingGolferModal(firstName, lastName);
}

async function checkNameAgainstDatabase(firstName, lastName, tokenAtRequest) {
    try {
        const res = await fetch("/golferSerch", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ firstName, lastName })
        });

        if (tokenAtRequest !== requestToken) {
            return;
        }

        const body = await res.json();

        if (!res.ok) {
            clearGolferMatch();
            lockRoundForm();
            setNameCheckStatus("Name check is temporarily unavailable.");
            return;
        }

        if (Number(body.results) === 1 && body.golfer) {
            applyExactMatch(body.golfer);
            return;
        }

        applyNoExactMatch(firstName, lastName);
    } catch (error) {
        if (tokenAtRequest !== requestToken) {
            return;
        }
        clearGolferMatch();
        lockRoundForm();
        setNameCheckStatus("Name check is temporarily unavailable.");
    }
}

function queueNameCheck() {
    if (!nameCheckEnabled) {
        return;
    }

    const firstName = normalizeInputName(firstNameEl.value);
    const lastName = normalizeInputName(lastNameEl.value);

    requestToken += 1;
    const activeToken = requestToken;

    if (debounceTimer) {
        clearTimeout(debounceTimer);
    }

    if (!firstName || !lastName) {
        hideMissingGolferModal();
        unlockRoundForm();
        clearGolferMatch();
        setNameCheckStatus("");
        return;
    }

    setNameCheckStatus("Checking name...");
    debounceTimer = setTimeout(() => {
        checkNameAgainstDatabase(firstName, lastName, activeToken);
    }, DEBOUNCE_MS);
}

function enableNameCheck() {
    nameCheckEnabled = true;
}

function toggleExtraHoles() {
    const showExtras = holeCountEl.value === "18";
    const extras = document.querySelectorAll(".extra-holes");
    extras.forEach(hole => {
        hole.hidden = !showExtras;
    });
    if (showExtras) {
        holesContainerEl.classList.add("eighteen-col");
    } else {
        holesContainerEl.classList.remove("eighteen-col");
    }
}

function loadCourseData() {
    if (!courseDataEl) {
        courses = [];
        return;
    }

    try {
        const parsed = JSON.parse(courseDataEl.textContent || "[]");
        courses = Array.isArray(parsed) ? parsed : [];
    } catch (error) {
        courses = [];
    }
}

function populateTeesForSelectedCourse() {
    if (!corseSelectEl || !teeSelectEl) {
        return;
    }

    teeSelectEl.innerHTML = '<option value="">Select a tee</option>';
    const selectedCourseId = Number(corseSelectEl.value);
    if (!selectedCourseId) {
        teeSelectEl.disabled = true;
        return;
    }

    const selectedCourse = courses.find(c => Number(c.courseID) === selectedCourseId);
    const tees = selectedCourse && Array.isArray(selectedCourse.tees) ? selectedCourse.tees : [];

    tees.forEach(tee => {
        const option = document.createElement("option");
        option.value = tee.teeID;
        option.textContent = `${tee.teeColor} (Slope ${tee.teeSlope}, Rating ${tee.teeRating}, Par ${tee.teePar})`;
        teeSelectEl.appendChild(option);
    });

    teeSelectEl.disabled = tees.length === 0;
}

function setRoundSubmitting(isSubmitting) {
    isSubmittingRound = isSubmitting;
    saveRoundBtnEl.disabled = isSubmitting;
    saveRoundBtnEl.textContent = isSubmitting ? "Saving..." : "Save Round";
}

function resetRoundFormState() {
    addRoundForm.reset();
    unlockRoundForm();
    golferIdEl.value = "";
    exactMatchGolfer = null;
    nameCheckEnabled = false;
    hideMissingGolferModal();
    setNameCheckStatus("");
    document.querySelectorAll(".hole-score").forEach(input => {
        input.classList.add("grayed-default");
    });
    toggleExtraHoles();
    populateTeesForSelectedCourse();
}

firstNameEl.addEventListener("focus", enableNameCheck, { once: true });
lastNameEl.addEventListener("focus", enableNameCheck, { once: true });
firstNameEl.addEventListener("input", queueNameCheck);
lastNameEl.addEventListener("input", queueNameCheck);
holeCountEl.addEventListener("change", toggleExtraHoles);
if (corseSelectEl) {
    corseSelectEl.addEventListener("change", populateTeesForSelectedCourse);
}

tryDifferentRoundNameBtn.addEventListener("click", () => {
    hideMissingGolferModal();
    unlockRoundForm();
    firstNameEl.value = "";
    lastNameEl.value = "";
    clearGolferMatch();
    setNameCheckStatus("");
    firstNameEl.focus();
});

addGolferFromRoundBtn.addEventListener("click", () => {
    localStorage.setItem("prefill", JSON.stringify({
        mode: "addGolfer",
        firstName: normalizeInputName(firstNameEl.value),
        lastName: normalizeInputName(lastNameEl.value)
    }));
    window.location.href = "/addGolfer";
});

addRoundForm.addEventListener("submit", (e) => {
    e.preventDefault();
    if (isSubmittingRound) {
        return;
    }
    if (!golferIdEl.value) {
        setNameCheckStatus("Please enter a valid golfer name found in the system.");
        return;
    }
    if (!corseSelectEl.value) {
        setNameCheckStatus("Please select a course.");
        return;
    }
    if (!teeSelectEl.value) {
        setNameCheckStatus("Please select a tee.");
        return;
    }

    const payload = Object.fromEntries(new FormData(addRoundForm));
    setRoundSubmitting(true);
    setNameCheckStatus("Saving round...");

    fetch("/addRound", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
        .then(async (res) => {
            const body = await res.json().catch(() => ({}));
            if (!res.ok) {
                const msg = body.error || body.message || "Unable to save round.";
                throw new Error(msg);
            }
            return body;
        })
        .then((body) => {
            resetRoundFormState();
            addRoundCard.hidden = true;
            roundSavedCardEl.hidden = false;
            roundSavedMessageEl.textContent = body.message || "Round saved successfully.";
            savedHandicapEl.textContent = body.handicap ?? "-";
            savedScoreDifferEl.textContent = body.scoreDiffer ?? "-";
            savedRoundsPlayedEl.textContent = body.roundsPlayed ?? "-";
            savedRoundAvgEl.textContent = body.roundAvg ?? "-";
            savedSeasonTotalEl.textContent = body.seasonTotal ?? "-";
        })
        .catch((err) => {
            setNameCheckStatus(`Save failed: ${err.message}`);
        })
        .finally(() => {
            setRoundSubmitting(false);
        });
});

addAnotherRoundBtnEl.addEventListener("click", () => {
    roundSavedCardEl.hidden = true;
    addRoundCard.hidden = false;
    resetRoundFormState();
});

document.querySelectorAll(".hole-score").forEach(input => {
    input.addEventListener("input", () => {
        input.classList.remove("grayed-default");
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const raw = localStorage.getItem("prefill");
    if (!raw) {
        return;
    }

    try {
        const pf = JSON.parse(raw);
        if (pf.mode === "addRound") {
            firstNameEl.value = pf.firstName || "";
            lastNameEl.value = pf.lastName || "";
            golferIdEl.value = pf.golferID || "";
            if (golferIdEl.value) {
                setNameCheckStatus("Golfer found.");
            }
        }
    } finally {
        localStorage.removeItem("prefill");
    }
});

toggleExtraHoles();
hideMissingGolferModal();
loadCourseData();
populateTeesForSelectedCourse();
