const addGolferForm = document.getElementById("addGolferForm");
const addGolferFields = document.getElementById("addGolferFields");
const addGolferCard = document.getElementById("addGolferCard");
const golferSavedCardEl = document.getElementById("golferSavedCard");
const golferSavedMessageEl = document.getElementById("golferSavedMessage");
const savedGolferIDEl = document.getElementById("savedGolferID");
const savedGolferNameEl = document.getElementById("savedGolferName");
const savedGolferHandicapEl = document.getElementById("savedGolferHandicap");
const savedGolferRoundsPlayedEl = document.getElementById("savedGolferRoundsPlayed");
const savedGolferRoundAvgEl = document.getElementById("savedGolferRoundAvg");
const savedGolferSeasonTotalEl = document.getElementById("savedGolferSeasonTotal");
const addAnotherGolferBtnEl = document.getElementById("addAnotherGolferBtn");
const firstNameEl = document.getElementById("firstName");
const lastNameEl = document.getElementById("lastName");
const nameCheckStatusEl = document.getElementById("nameCheckStatus");

const preExistingInformationEl = document.getElementById("preExistingInformation");
const existingInformationEl = document.getElementById("ExistingInformation");

const existingGolferModalEl = document.getElementById("existingGolferModal");
const existingGolferMessageEl = document.getElementById("existingGolferMessage");
const tryDifferentNameBtn = document.getElementById("tryDifferentNameBtn");
const proceedToRoundBtn = document.getElementById("proceedToRoundBtn");

const LOCKED_CLASS = "is-locked";
const DEBOUNCE_MS = 1000;

let debounceTimer = null;
let requestToken = 0;
let exactMatch = null;
let nameCheckEnabled = false;
let isSubmittingGolfer = false;

function normalizeInputName(value) {
    return (value || "").trim();
}

function setNameCheckStatus(text) {
    nameCheckStatusEl.textContent = text || "";
}

function toggleExistingInfo() {
    const isTrue = preExistingInformationEl.value === "True";
    const extras = document.querySelectorAll(".extra-info");
    existingInformationEl.hidden = !isTrue;
    extras.forEach(el => {
        el.hidden = !isTrue;
    });
}

function showDuplicateModal(golfer) {
    existingGolferMessageEl.textContent =
        `${golfer.firstName} ${golfer.lastName} is already in the system. Would you like to try a different name or proceed to adding a score?`;
    existingGolferModalEl.hidden = false;
}

function hideDuplicateModal() {
    existingGolferModalEl.hidden = true;
}

function lockFormForDuplicate(golfer) {
    exactMatch = golfer;
    addGolferFields.disabled = true;
    addGolferForm.querySelector("#saveGolferBtn").disabled = true;
    addGolferCard.classList.add(LOCKED_CLASS);
    showDuplicateModal(golfer);
}

function unlockForm() {
    exactMatch = null;
    addGolferFields.disabled = false;
    addGolferForm.querySelector("#saveGolferBtn").disabled = false;
    addGolferCard.classList.remove(LOCKED_CLASS);
    hideDuplicateModal();
}

function setGolferSubmitting(isSubmitting) {
    isSubmittingGolfer = isSubmitting;
    const btn = addGolferForm.querySelector("#saveGolferBtn");
    btn.disabled = isSubmitting;
    btn.textContent = isSubmitting ? "Saving..." : "Save Golfer";
}

function resetGolferFormState() {
    addGolferForm.reset();
    unlockForm();
    nameCheckEnabled = false;
    toggleExistingInfo();
    setNameCheckStatus("");
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
            setNameCheckStatus("Name check is temporarily unavailable.");
            return;
        }

        if (Number(body.results) === 1 && body.golfer) {
            setNameCheckStatus("Exact match found.");
            lockFormForDuplicate(body.golfer);
            return;
        }

        unlockForm();
        if (Number(body.results) === 2) {
            setNameCheckStatus("No exact match. Similar names exist.");
        } else {
            setNameCheckStatus("No exact match found.");
        }
    } catch (error) {
        if (tokenAtRequest !== requestToken) {
            return;
        }
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
        unlockForm();
        setNameCheckStatus("");
        return;
    }

    if (exactMatch && (
        firstName.toLowerCase() !== (exactMatch.firstName || "").toLowerCase() ||
        lastName.toLowerCase() !== (exactMatch.lastName || "").toLowerCase()
    )) {
        unlockForm();
    }

    setNameCheckStatus("Checking name...");
    debounceTimer = setTimeout(() => {
        checkNameAgainstDatabase(firstName, lastName, activeToken);
    }, DEBOUNCE_MS);
}

function enableNameCheck() {
    nameCheckEnabled = true;
}

firstNameEl.addEventListener("focus", enableNameCheck, { once: true });
lastNameEl.addEventListener("focus", enableNameCheck, { once: true });
firstNameEl.addEventListener("input", queueNameCheck);
lastNameEl.addEventListener("input", queueNameCheck);
preExistingInformationEl.addEventListener("change", toggleExistingInfo);

tryDifferentNameBtn.addEventListener("click", () => {
    hideDuplicateModal();
    unlockForm();
    firstNameEl.value = "";
    lastNameEl.value = "";
    setNameCheckStatus("");
    firstNameEl.focus();
});

proceedToRoundBtn.addEventListener("click", () => {
    if (!exactMatch) {
        return;
    }

    localStorage.setItem("prefill", JSON.stringify({
        mode: "addRound",
        section: "matchFound",
        firstName: exactMatch.firstName || "",
        lastName: exactMatch.lastName || "",
        golferID: exactMatch.golferID || ""
    }));

    window.location.href = "/addRound";
});

addGolferForm.addEventListener("submit", (e) => {
    e.preventDefault();
    if (isSubmittingGolfer) {
        return;
    }
    if (exactMatch) {
        return;
    }
    const payload = Object.fromEntries(new FormData(addGolferForm));
    setGolferSubmitting(true);
    setNameCheckStatus("Saving golfer...");

    fetch("/addGolfer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
        .then(async (res) => {
            const body = await res.json().catch(() => ({}));
            if (!res.ok) {
                const msg = body.error || body.message || "Unable to save golfer.";
                throw new Error(msg);
            }
            return body;
        })
        .then((body) => {
            resetGolferFormState();
            addGolferCard.hidden = true;
            golferSavedCardEl.hidden = false;
            golferSavedMessageEl.textContent = body.message || "Golfer saved successfully.";
            savedGolferIDEl.textContent = body.golferID ?? "-";
            savedGolferNameEl.textContent = `${body.firstName || ""} ${body.lastName || ""}`.trim() || "-";
            savedGolferHandicapEl.textContent = body.handicap ?? "-";
            savedGolferRoundsPlayedEl.textContent = body.roundsPlayed ?? "-";
            savedGolferRoundAvgEl.textContent = body.roundAvg ?? "-";
            savedGolferSeasonTotalEl.textContent = body.seasonTotal ?? "-";
        })
        .catch((err) => {
            setNameCheckStatus(`Save failed: ${err.message}`);
        })
        .finally(() => {
            setGolferSubmitting(false);
        });
});

addAnotherGolferBtnEl.addEventListener("click", () => {
    golferSavedCardEl.hidden = true;
    addGolferCard.hidden = false;
    resetGolferFormState();
});

document.addEventListener("DOMContentLoaded", () => {
    const raw = localStorage.getItem("prefill");
    if (!raw) {
        return;
    }

    try {
        const pf = JSON.parse(raw);
        if (pf.mode === "addGolfer") {
            firstNameEl.value = pf.firstName || "";
            lastNameEl.value = pf.lastName || "";
        }
    } finally {
        localStorage.removeItem("prefill");
    }
});

toggleExistingInfo();
