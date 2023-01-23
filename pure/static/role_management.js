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
    document.getElementById('cr_mail').disabled = false
    document.getElementById('cr_ok').disabled = false
    const candidate_container = document.getElementById("cr_container")
    if(course === "") {
        candidate_container.innerHTML = ''
        document.getElementById('cr_mail').disabled = true
    document.getElementById('cr_ok').disabled = true
    } else {
        let div = document.createElement('div')
        div.className = "d-md-flex flex-column flex-grow-1 justify-content-md-start"
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
                candidate_container.innerHTML = ''
                div.appendChild(name)
                div.appendChild(email)
                if(name.textContent !== "") {
                    const rem = document.createElement("a")
                    let del_image = document.createElement('img')
                    del_image.src = "../../static/delete_icon.png"
                    del_image.width = 36
                    del_image.height = 34
                    rem.appendChild(del_image)
                    // rem.textContent = '-'
                    rem.id = candidate["email"]
                    rem.addEventListener("click", () => {
                        remove_cr(rem.id, course)
                    })
                    candidate_container.appendChild(div)
                    candidate_container.appendChild(rem)
                }

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

function assign_cr_call(){
    let cr_email = document.getElementById('cr_mail')
    let course = document.getElementById("cr_course")
    assign_rep(cr_email.value, course.value)
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
