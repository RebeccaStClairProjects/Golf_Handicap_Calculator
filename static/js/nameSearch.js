// static/js/nameSearch.js

const form = document.getElementById("golferSerch");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    statusEl.textContent = "Searching…";
    resultEl.innerHTML = "";

    const data = Object.fromEntries(new FormData(form));

    try {
        const res = await fetch("/golferSerch", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!res.ok) throw new Error(`Server returned ${res.status}`);

        const golfer = await res.json();
        console.log("API response:", golfer);

        switch (Number(golfer.results)) {
            case 1:
                // Once golfer selected open the form to add new round                                             FIX ME!!! 
                statusEl.textContent = "Exact match found!";
                resultEl.innerHTML = `
          <strong>Selected Golfer:</strong><br>
          Name: ${golfer.firstName} ${golfer.lastName}<br>
          ID: ${golfer.golferID}
        `;
                break;

            case 2: {
                statusEl.textContent = "Close matches found!";
                let candidatesContainer = document.getElementById("candidateList");
                if (!candidatesContainer) {
                    candidatesContainer = document.createElement("div");
                    candidatesContainer.id = "candidateList";
                    resultEl.insertAdjacentElement("afterend", candidatesContainer);
                }
                candidatesContainer.innerHTML = "";
                (golfer.candidates || []).forEach(g => {
                    const btn = document.createElement("button");
                    btn.textContent = `${g.firstName} ${g.lastName}`;
                    btn.classList.add("candidate-btn");

                    // Once golfer selected open the form to add new round                                             FIX ME!!! 

                    btn.addEventListener("click", () => {
                        resultEl.innerHTML = `
              <strong>Selected Golfer:</strong><br>
              Name: ${g.firstName} ${g.lastName}<br>
              ID: ${g.golferID}
            `;
                    });
                    candidatesContainer.appendChild(btn);
                });
                break;
            }

            case 3:
                statusEl.textContent = "No match found.";
                resultEl.textContent = "No golfer found. Would you like to add a new golfer?";

                // Prompt the user if they want to add a new golfer                                                     FIX ME!!!
                // If yes, then poll up the form to add a new golfer                                                    FIX ME!!!

                break;

            default:
                statusEl.textContent = "Unexpected response.";
                resultEl.textContent = JSON.stringify(golfer, null, 2);
        }
    } catch (err) {
        statusEl.textContent = "Error";
        resultEl.textContent = String(err);
    }
});
