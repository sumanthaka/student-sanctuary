async function role_management(container) {
    await fetch(role_url)
        .then(response => {
            return response.text()
        })
        .then(text => {
            container.innerHTML=text
        })
}

async function create_role() {
    // const add_button = document.getElementById(add_button_id)
    // add_button.disabled = true
    // const role_container = document.getElementById("role_container")
    // let input_role = document.createElement("input")
    // input_role.type = "text"
    // input_role.placeholder = "Enter role name"
    // role_container.appendChild(input_role)
    // let announce_make_perm = document.createElement("input")
    // announce_make_perm.id = "announce_make_perm"
    // announce_make_perm.type = "checkbox"
    // announce_make_perm.value = "announcement_maker"
    // role_container.appendChild(announce_make_perm)
    // let announce_make_perm_label = document.createElement("label")
    // announce_make_perm_label.setAttribute("for", "announce_make_perm")
    // announce_make_perm_label.textContent = "Announcement Maker"
    // role_container.appendChild(announce_make_perm_label)
    //
    // let student_council_chat_perm = document.createElement("input")
    // student_council_chat_perm.id = "student_council_chat_perm"
    // student_council_chat_perm.type = "checkbox"
    // student_council_chat_perm.value = "student_council_chat"
    // role_container.appendChild(student_council_chat_perm)
    // let student_council_chat_label = document.createElement("label")
    // student_council_chat_label.setAttribute("for", "student_council_chat_perm")
    // student_council_chat_label.textContent = "Student Council Chat"
    // role_container.appendChild(student_council_chat_label)
    //
    // let ok_role = document.createElement("button")
    // ok_role.textContent = "OK"
    // ok_role.addEventListener("click", async () => {
    let input_role = document.getElementById('role_name_input')
    let announce_make_perm = document.getElementById('announce_make_perm')
    let student_council_chat_perm = document.getElementById('student_council_chat_perm')
    const role = input_role.value
    const announce_perm = announce_make_perm.checked
    const council_perm = student_council_chat_perm.checked
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
        if (council_perm) {
            data["permissions"].push("student_council_chat")
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
    // })
    // role_container.appendChild(ok_role)
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
    const candidate_value = document.getElementById(role_value).value
    if (candidate_value === "") {
        alert("Please type a candidate email to add")
    } else {
        let data = {}
        data["assign_role"] = "true"
        data["role"] = role_value.slice(0, -6)
        data["candidate_mail"] = candidate_value
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
}

async function display_cr(course) {
    const candidate_container = document.getElementById("cr_container")
    if(course === "") {
        candidate_container.innerHTML = ''
    } else {
        const name = document.createElement("p")
        const email = document.createElement("p")
        let candidate = {}
        await fetch(role_url + '/' + 'candidates' + '/' + course, {
            'method': 'GET'
        })
            .then(response => {
                return response.text()
            })
            .then(text => {
                candidate = JSON.parse(text)
                name.textContent = candidate["name"]
                email.textContent = candidate["email"]
                const assign_cr = document.createElement("input")
                assign_cr.type = 'email'
                assign_cr.id = "assign_cr_email"
                const cr_ok = document.createElement("button")
                cr_ok.textContent = 'OK'
                cr_ok.addEventListener("click", () => {
                    assign_rep(assign_cr.value, course)
                })
                candidate_container.innerHTML = ''
                candidate_container.appendChild(name)
                candidate_container.appendChild(email)
                if(name.textContent !== "") {
                    const rem = document.createElement("button")
                    rem.textContent = '-'
                    rem.id = candidate["email"]
                    rem.addEventListener("click", () => {
                        remove_cr(rem.id, course)
                    })
                    candidate_container.appendChild(rem)
                }
                candidate_container.appendChild(assign_cr)
                candidate_container.appendChild(cr_ok)
            })
    }
}

async function remove_cr(cr_mail, course) {
    const course_dropdown = document.getElementById('course')
    let data = {}
    data["delete_cr"] = "true"
    data["email"] = cr_mail
    await fetch(role_url+'/'+'candidates'+'/'+course, {
        method: "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data)
    })
    await display_cr(course_dropdown.value)
}

async function assign_rep(cr_email, course) {
    if(cr_email === "") {
        alert("Please enter CR email to add")
    } else {
        const course_dropdown = document.getElementById('course')
        let data= {}
        data["assign_cr"] = "true"
        data["email"] = cr_email
        await fetch(role_url+'/'+'candidates'+'/'+course, {
            'method': 'POST',
            "headers": {"Content-Type": "application/json"},
            'body': JSON.stringify(data)
        })
        // await display_cr(course_dropdown.value)
        role_management(container)
    }
}
