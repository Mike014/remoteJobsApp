from flask import Blueprint, jsonify, render_template_string
from app import db
from sqlalchemy import text

bp = Blueprint('routes', __name__)

# Route principale per UI
@bp.route('/', methods=['GET'])
def ui():
    # HTML con JavaScript per caricare i dati dinamicamente
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Remote Jobs API</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container my-5">
            <h1 class="text-center">Remote Jobs API</h1>
            <p class="text-center">Esplora le aziende remote disponibili.</p>
            <div id="companies"></div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Carica le aziende dall'API
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
                                        <p class="card-text">${company.description ? company.description.substring(0, 150) + "..." : "No description available."}</p>
                                        ${company.website 
                                            ? `<a href="${company.website}" class="btn btn-primary" target="_blank">Visit Website</a>` 
                                            : `<p class="text-muted">Website not available</p>`}
                                    </div>
                                </div>`;
                            container.innerHTML += card;
                        });
                    })
                    .catch(error => {
                        console.error("Error fetching companies:", error);
                        const container = document.getElementById("companies");
                        container.innerHTML = `<p class="text-danger">Error loading companies. Please try again later.</p>`;
                    });
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

# API per ottenere l'elenco delle aziende
@bp.route('/api/companies', methods=['GET'])
def get_companies():
    # Query SQL per ottenere le aziende
    query = text("SELECT id, name, description, website, tech_stack FROM companies")
    results = db.session.execute(query).fetchall()

    # Converti i risultati in un elenco di dizionari
    companies = [
        {
            "id": row.id,
            "name": row.name,
            "description": row.description or "No description provided.",
            "website": row.website,
            "tech_stack": row.tech_stack or "No tech stack provided.",
        }
        for row in results
    ]

    return jsonify(companies)