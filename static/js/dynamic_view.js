// Ensure the global variables are defined
const data = window.tableData;
const columns = window.tableColumns;

// Render the table from JSON data
function renderTable() {
    const tableBody = document.querySelector('#dataTable tbody');
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            {% for column in columns %}
            <td>${item['{{ column.key }}']}</td>
            {% endfor %}
        `;
        tableBody.appendChild(row);
    });
}

// Filter the table
function filterTable() {
    const filters = {};
    {% for column in columns %}
    filters['{{ column.key }}'] = document.getElementById('{{ column.key }}Filter').value.toLowerCase();
    {% endfor %}

    const rows = document.querySelectorAll('#dataTable tbody tr');

    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        let isVisible = true;

        {% for column in columns %}
        const cellText = cells[{{ loop.index0 }}].textContent.toLowerCase();
        const filterValue = filters['{{ column.key }}'];
        if (filterValue && !cellText.includes(filterValue)) {
            isVisible = false;
        }
        {% endfor %}

        row.style.display = isVisible ? '' : 'none';
    });
}

// Clear the filters
function clearForm() {
    {% for column in columns %}
    const filterInput = document.getElementById('{{ column.key }}Filter');
    if (filterInput) {
        filterInput.value = '';
    }
    {% endfor %}
    filterTable(); // Refresh the table after clearing filters
}

// Initial render
renderTable();
