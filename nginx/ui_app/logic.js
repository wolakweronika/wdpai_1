document.getElementById('team-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const firstName = document.getElementById('first_name').value;
    const lastName = document.getElementById('last_name').value;
    const role = document.getElementById('role').value;

    if (document.getElementById('privacy_policy').checked) {
        addTeamMember(firstName, lastName, role);
        document.getElementById('team-form').reset();
    } else {
        alert('Musisz zaakceptować politykę prywatności.');
    }
});

function addTeamMember(firstName, lastName, role) {
    const teamMembersList = document.getElementById('team-members');

    // Create a list item
    const listItem = document.createElement('li');
    listItem.classList.add('team-member');  // Updated to match the CSS class

    // Create the container for name and role
    const info = document.createElement('div');
    info.classList.add('user-info');
    info.innerHTML = `<span class="name">${firstName} ${lastName}</span><span class="role">${role}</span>`;

    // Create the delete button
    const deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-btn');  // Updated to match the CSS class
    deleteButton.innerHTML = '🗑️';  // Trash icon emoji

    // Add event listener to remove the team member on click
    deleteButton.addEventListener('click', function () {
        teamMembersList.removeChild(listItem);
    });

    // Append the info and delete button to the list item
    listItem.appendChild(info);
    listItem.appendChild(deleteButton);

    // Append the list item to the team members list
    teamMembersList.appendChild(listItem);
}