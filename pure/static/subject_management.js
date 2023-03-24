async function subject_management(container) {
    await fetch(subject_url)
        .then((response) => { return response.text() })
        .then((text) => {
                container.innerHTML = text
            })

    let sem_list_dropdown = document.getElementById("sem_list")
    let course_list_dropdown = document.getElementById("course_list")
    let subject_list = document.getElementById("subject_list")
    let ok_subject = document.getElementById('ok_subject')

    await sem_change(course_list_dropdown.value, sem_list_dropdown)
    await subject_change(sem_list_dropdown.value, course_list_dropdown.value, subject_list)
    ok_subject.addEventListener('click', () => { add_subject(sem_list_dropdown.value, course_list_dropdown.value, subject_list) })
    course_list_dropdown.addEventListener('change', async () => {
        await sem_change(course_list_dropdown.value, sem_list_dropdown)
        await subject_change(sem_list_dropdown.value, course_list_dropdown.value, subject_list)
    })
    sem_list_dropdown.addEventListener('change', async () => {
        await subject_change(sem_list_dropdown.value, course_list_dropdown.value, subject_list)
    })
}

async function sem_change(course_value, sem_list) {
    sem_list.innerHTML = ``
    await fetch(subject_url, {
        method: 'POST',
        'body': [course_value, 'get_duration']
    })
        .then((response) => {
            return response.text()
        })
        .then((sems) => {
            let sems_val = parseInt(sems)
            for(let i=1;i<=sems_val;i++){
                let sem_item = document.createElement("option")
                sem_item.value = i
                sem_item.text = "Semester " + i
                sem_list.appendChild(sem_item)
            }
        })
}

async function subject_change(sem_value, course_value, subject_list) {
    subject_list.innerHTML = ``
    await fetch(subject_url, {
        'method': 'POST',
        'body': [sem_value, course_value, 'get']
    })
        .then((response) => {
            return response.json() })
        .then((json) => {
            for (let subject of json.subjects) {
                let subject_item = document.createElement('li')
                subject_item.className = "list-group-item d-flex justify-content-between align-items-center"
                subject_item.style = "color: white;background: transparent"
                let subject_item_span = document.createElement('span')
                subject_item_span.textContent = subject
                subject_item.appendChild(subject_item_span)
                let delete_button = document.createElement('a')
                delete_button.style = "cursor: pointer;"
                let delete_icon = document.createElement('img')
                delete_icon.src = "../../static/delete_icon.png"
                delete_icon.width = 36
                delete_icon.height = 34
                delete_button.appendChild(delete_icon)
                delete_button.id = subject
                delete_button.addEventListener('click', async () => {
                    await fetch(subject_url, {
                        'method': 'POST',
                        'body': [sem_value, course_value, subject, 'delete']
                    })
                    subject_change(sem_value, course_value, subject_list)
                })
                subject_item.appendChild(delete_button)
                subject_list.appendChild(subject_item)
            }
        })
}

async function add_subject(sem_value, course_value, subject_list) {
    let subject_input = document.getElementById('subject_input')
    let subject = subject_input.value
        // let subject = input.value
    if (subject === "") {
        alert("Please enter a subject")
    } else {
        await fetch(subject_url, {
            'method': 'POST',
            'body': [subject, sem_value, course_value, 'add']
        })
        subject_input.value = ""
        subject_change(sem_value, course_value, subject_list)
    }
}
