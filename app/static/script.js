document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/companies")
        .then(response => response.json())
        .then(companies => {
            const container = document.getElementById("companies");
            companies.forEach(company => {
                const card = `
                    <div class="card my-3">
                        <div class="card-body">
                            <h5 class="card-title">${company.name}</h5>
                            <p class="card-text">${company.description.substring(0, 150)}...</p>
                            <a href="${company.website}" class="btn btn-primary" target="_blank">Visit Website</a>
                        </div>
                    </div>`;
                container.innerHTML += card;
            });
        })
        .catch(error => console.error("Error fetching companies:", error));
});