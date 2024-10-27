document.addEventListener("DOMContentLoaded", function () {
    const getForm = document.getElementById("getForm"); 
    const postForm = document.getElementById("userForm"); 

    if (getForm) {
        getForm.addEventListener("submit", async function (event) {
            event.preventDefault(); 
            const input = document.getElementById("getInputField").value; 

            if (!input) {
                alert("Please enter a path for the GET request.");
                return;
            }

            const url = `http://localhost:8000/${input}`; 

            try {
                document.getElementById("getResponse").textContent = "Loading...";
                const response = await fetch(url);
                
                if (!response.ok) {
                    throw new Error(`GET request failed with status ${response.status}`);
                }

                const data = await response.json();
                document.getElementById("getResponse").textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById("getResponse").textContent = "Error: " + error.message;
                console.error('Error:', error);
            }
        });
    }

    postForm.addEventListener("submit", async function (event) {
        event.preventDefault(); 
        const firstName = document.getElementById("firstName").value.trim();
        const lastName = document.getElementById("lastName").value.trim();
        const role = document.getElementById("role").value.trim();

        if (!firstName || !lastName || !role) {
            alert("Please fill in all fields.");
            return;
        }

        const data = {
            firstName: firstName,
            lastName: lastName,
            role: role
        };

        try {
            const response = await fetch("http://localhost:8000", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`POST request failed with status ${response.status}`);
            }

            const responseData = await response.json();
            const fullName = `${responseData.firstName} ${responseData.lastName}`;
            addListItem(fullName, responseData.role, responseData.id);

       
            postForm.reset();
        } catch (error) {
            console.error('Error:', error);
            alert("Failed to add user. Please try again.");
        }
    });
});
