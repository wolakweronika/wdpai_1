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

    const listItem = document.createElement('li');
    listItem.classList.add('team-member');  


    const info = document.createElement('div');
    info.classList.add('user-info');
    info.innerHTML = `<span class="name">${firstName} ${lastName}</span><span class="role">${role}</span>`;

    const deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-btn');  
    deleteButton.innerHTML = '🗑️';  

  
    deleteButton.addEventListener('click', function () {
        teamMembersList.removeChild(listItem);
    });

    listItem.appendChild(info);
    listItem.appendChild(deleteButton);

    teamMembersList.appendChild(listItem);
}