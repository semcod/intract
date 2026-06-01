function login(username, password) {
    // This is a function that does login validation
    if (username === "admin" && password === "secret") {
        return { success: true, token: "admin-token" };
    }
    return { success: false, error: "Invalid credentials" };
}

function fetchUserProfile(token) {
    // This function makes a network call, which might violate contracts
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/profile", false);
    xhr.setRequestHeader("Authorization", "Bearer " + token);
    xhr.send();
    return JSON.parse(xhr.responseText);
}
