async function role_management(container) {
    await fetch(role_url)
        .then(response => {
            return response.text()
        })
        .then(text => {
            container.innerHTML=text
        })
}

function create_role() {
    const role_container = document.getElementById("role_container")
    let input_role = document.createElement("input")
    input_role.type = "text"
    input_role.placeholder = "Enter role name"
    role_container.appendChild(input_role)
    let announce_make_perm = document.createElement("input")
    announce_make_perm.id = "announce_make_perm"
    announce_make_perm.type = "checkbox"
    announce_make_perm.value = "announcement_maker"
    role_container.appendChild(announce_make_perm)
    let announce_make_perm_label = document.createElement("label")
    announce_make_perm_label.setAttribute("for", "announce_make_perm")
    announce_make_perm_label.textContent = "Announcement Maker"
    role_container.appendChild(announce_make_perm_label)
    let ok_role = document.createElement("button")
    ok_role.textContent = "OK"
    ok_role.addEventListener("click", async () => {
        const role = input_role.value
        const announce_perm = announce_make_perm.checked
        if (role === "") {
            alert("Please enter role name")
        } else {
            let data = {}
            data["add_role"] = "true"
            data["role"] = role
            data["permissions"] = []
            if (announce_perm) {
                data["permissions"].push("announcement_maker")
            }
            await fetch(role_url, {
                method: "POST",
                "headers": {"Content-Type": "application/json"},
                "body": JSON.stringify(data)
            })
                .then(response => {
                    return response.text()
                })
                .then(text => {
                    container.innerHTML = text
                })
        }
    })
    role_container.appendChild(ok_role)
}

function delete_role(role_id) {
    let data = {}
    data["delete_role"] = "true"
    data["role"] = role_id
    fetch(role_url, {
        method: "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data)
    })
        .then(response => {
            return response.text()
        })
        .then(text => {
            container.innerHTML = text
        })
}

function delete_candidate(candidate_mail) {
    let data = {}
    data["delete_candidate"] = "true"
    data["email"] = candidate_mail
    fetch(role_url, {
        method: "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data)
    })
        .then(response => {
            return response.text()
        })
        .then(text => {
            container.innerHTML = text
        })
}

function assign_role(role_value) {
    let data = {}
    data["assign_role"] = "true"
    data["role"] = role_value.slice(0, -6)
    data["candidate_mail"] = document.getElementById(role_value).value
    fetch(role_url, {
        method: "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data)
    })
        .then(response => {
            return response.text()
        })
        .then(text => {
            container.innerHTML = text
        })
}
