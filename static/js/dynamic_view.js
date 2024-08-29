// Ensure the global variables are defined
const data = window.tableData;
const columns = window.tableColumns;

// Render the table from JSON data
function renderTable() {
    const tableBody = document.querySelector('#dataTable tbody');
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = columns.map(column => `
            <td>${item[column.key]}</td>
        `).join('');
        tableBody.appendChild(row);
    });
}

// Filter the table
function filterTable() {
    const filters = {};
    columns.forEach(column => {
        filters[column.key] = document.getElementById(`${column.key}Filter`).value.toLowerCase();
    });

    const rows = document.querySelectorAll('#dataTable tbody tr');

    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        let isVisible = true;

        columns.forEach((column, index) => {
            const cellText = cells[index].textContent.toLowerCase();
            const filterValue = filters[column.key];
            if (filterValue && !cellText.includes(filterValue)) {
                isVisible = false;
            }
        });

        row.style.display = isVisible ? '' : 'none';
    });
}

// Clear the filters
function clearForm() {
    columns.forEach(column => {
        const filterInput = document.getElementById(`${column.key}Filter`);
        if (filterInput) {
            filterInput.value = '';
        }
    });
    filterTable(); // Refresh the table after clearing filters
}

// Initial render
renderTable();
