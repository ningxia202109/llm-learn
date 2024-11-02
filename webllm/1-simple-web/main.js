document.addEventListener('DOMContentLoaded', () => {
    const buttonA = document.getElementById('buttonA');
    const buttonB = document.getElementById('buttonB');
    const content = document.getElementById('content');
    const infoLabel = document.getElementById('info-label');

    buttonA.addEventListener('click', showPicture);
    buttonB.addEventListener('click', showTable);

    function showPicture() {
        content.innerHTML = '<img src="https://picsum.photos/300/200" alt="Random Picture">';
        infoLabel.textContent = 'Displaying a random picture';
    }

    function showTable() {
        const tableData = [
            { name: 'John Doe', age: 30 },
            { name: 'Jane Smith', age: 25 },
            { name: 'Bob Johnson', age: 35 }
        ];

        let tableHTML = `
            <table>
                <tr>
                    <th>Name</th>
                    <th>Age</th>
                </tr>
        `;

        tableData.forEach(person => {
            tableHTML += `
                <tr>
                    <td>${person.name}</td>
                    <td>${person.age}</td>
                </tr>
            `;
        });

        tableHTML += '</table>';
        content.innerHTML = tableHTML;
        infoLabel.textContent = 'Displaying a table of names and ages';
    }
});
