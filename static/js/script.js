/**
 * Mumbai Local Development Dashboard
 * Frontend JavaScript — Chart.js Visualizations & Interactivity
 * B.Sc Data Science Student Project
 */

// Utility function to get category colors
function getCategoryColor(category) {
    if (category === "High Development") return "#16a34a"; // Green
    if (category === "Moderate Development") return "#d97706"; // Amber
    return "#dc2626"; // Red
}

// -------------------------------------------------------------
// Initialize Dashboard Charts
// -------------------------------------------------------------
function initDashboardCharts(data) {
    if (!data) return;

    // 1. Chart 1 — Development Score by Ward (Horizontal Bar Chart)
    const ctxScore = document.getElementById("chartDevScore");
    if (ctxScore) {
        const backgroundColors = data.score_ranking.categories.map(cat => getCategoryColor(cat));
        new Chart(ctxScore, {
            type: "bar",
            data: {
                labels: data.score_ranking.labels,
                datasets: [{
                    label: "Development Score (0-100)",
                    data: data.score_ranking.scores,
                    backgroundColor: backgroundColors,
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            afterLabel: function(context) {
                                return `Category: ${data.score_ranking.categories[context.dataIndex]}`;
                            }
                        }
                    }
                },
                scales: {
                    x: { min: 0, max: 100, title: { display: true, text: "Project Development Score" } },
                    y: { ticks: { font: { size: 10 } } }
                }
            }
        });
    }

    // 2. Chart 2 — Population by Ward
    const ctxPop = document.getElementById("chartPopulation");
    if (ctxPop) {
        new Chart(ctxPop, {
            type: "bar",
            data: {
                labels: data.population.labels,
                datasets: [{
                    label: "Ward Population",
                    data: data.population.values,
                    backgroundColor: "#3b82f6",
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            beforeLabel: function(context) {
                                return data.population.names[context.dataIndex];
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: "Population (Census Data)" },
                        ticks: {
                            callback: function(val) { return (val / 1000) + "k"; }
                        }
                    },
                    x: { ticks: { font: { size: 9 }, maxRotation: 45 } }
                }
            }
        });
    }

    // 3. Chart 3 — Infrastructure Coverage
    const ctxInfra = document.getElementById("chartInfrastructure");
    if (ctxInfra) {
        new Chart(ctxInfra, {
            type: "bar",
            data: {
                labels: data.infrastructure.labels,
                datasets: [
                    { label: "Water Coverage (%)", data: data.infrastructure.water, backgroundColor: "#0284c7" },
                    { label: "Drainage Coverage (%)", data: data.infrastructure.drainage, backgroundColor: "#0d9488" },
                    { label: "Waste Collection (%)", data: data.infrastructure.waste, backgroundColor: "#eab308" }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 60, max: 100, title: { display: true, text: "Coverage Percentage (%)" } },
                    x: { ticks: { font: { size: 9 }, maxRotation: 45 } }
                }
            }
        });
    }

    // 4. Chart 4 — Public Facilities
    const ctxFac = document.getElementById("chartFacilities");
    if (ctxFac) {
        new Chart(ctxFac, {
            type: "bar",
            data: {
                labels: data.facilities.labels,
                datasets: [
                    { label: "Schools", data: data.facilities.schools, backgroundColor: "#6366f1" },
                    { label: "Health Facilities", data: data.facilities.health, backgroundColor: "#ef4444" },
                    { label: "Parks & Open Spaces", data: data.facilities.parks, backgroundColor: "#22c55e" }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, title: { display: true, text: "Facility Count" } },
                    x: { ticks: { font: { size: 9 }, maxRotation: 45 } }
                }
            }
        });
    }

    // 5. Chart 5 — Development Category Distribution
    const ctxCat = document.getElementById("chartCategory");
    if (ctxCat) {
        new Chart(ctxCat, {
            type: "doughnut",
            data: {
                labels: ["High Development", "Moderate Development", "Low Development"],
                datasets: [{
                    data: [
                        data.categories["High Development"] || 0,
                        data.categories["Moderate Development"] || 0,
                        data.categories["Low Development"] || 0
                    ],
                    backgroundColor: ["#16a34a", "#d97706", "#dc2626"],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });
    }

    // 6. Chart 6 — Population Density vs Development Score
    const ctxScatter = document.getElementById("chartScatter");
    if (ctxScatter) {
        new Chart(ctxScatter, {
            type: "scatter",
            data: {
                datasets: [{
                    label: "Mumbai Wards",
                    data: data.scatter,
                    backgroundColor: "#1e3a8a",
                    borderColor: "#3b82f6",
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const pt = context.raw;
                                return `${pt.ward} — Density: ${pt.x.toLocaleString()} /sq km, Score: ${pt.y}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: "Population Density (persons / sq km)" },
                        ticks: {
                            callback: function(val) { return (val / 1000) + "k"; }
                        }
                    },
                    y: {
                        min: 30,
                        max: 100,
                        title: { display: true, text: "Development Score (0-100)" }
                    }
                }
            }
        });
    }
}

// -------------------------------------------------------------
// Ward Comparison Chart
// -------------------------------------------------------------
function initCompareChart(compData) {
    const ctx = document.getElementById("chartComparison");
    if (!ctx || !compData) return;

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: compData.labels,
            datasets: [
                {
                    label: compData.name_a,
                    data: compData.ward_a_scores,
                    backgroundColor: "#2563eb",
                    borderRadius: 4
                },
                {
                    label: compData.name_b,
                    data: compData.ward_b_scores,
                    backgroundColor: "#0d9488",
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 0, max: 100, title: { display: true, text: "Score (0 - 100)" } }
            }
        }
    });
}

// -------------------------------------------------------------
// Ward Detail Radar Chart
// -------------------------------------------------------------
function initRadarChart(radarData, wardName) {
    const ctx = document.getElementById("chartRadar");
    if (!ctx || !radarData) return;

    new Chart(ctx, {
        type: "radar",
        data: {
            labels: radarData.labels,
            datasets: [
                {
                    label: wardName,
                    data: radarData.ward_scores,
                    backgroundColor: "rgba(37, 99, 235, 0.2)",
                    borderColor: "#2563eb",
                    pointBackgroundColor: "#2563eb"
                },
                {
                    label: "Mumbai Average",
                    data: radarData.city_avg,
                    backgroundColor: "rgba(100, 116, 139, 0.2)",
                    borderColor: "#64748b",
                    pointBackgroundColor: "#64748b",
                    borderDash: [4, 4]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    min: 0,
                    max: 100,
                    ticks: { stepSize: 20 }
                }
            }
        }
    });
}

// -------------------------------------------------------------
// Client-side Table Search for Wards Page
// -------------------------------------------------------------
function setupTableSearch() {
    const searchInput = document.getElementById("wardSearchInput");
    const tableBody = document.getElementById("wardTableBody");
    if (!searchInput || !tableBody) return;

    searchInput.addEventListener("input", function() {
        const query = this.value.toLowerCase().trim();
        const rows = tableBody.getElementsByTagName("tr");
        for (let row of rows) {
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(query) ? "" : "none";
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    setupTableSearch();
});
