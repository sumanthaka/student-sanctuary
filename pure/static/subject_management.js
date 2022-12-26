async function subject_management(container) {
    await fetch(subject_url)
        .then((response) => { return response.text() })
        .then((text) => {
                container.innerHTML = text
            })

    let course_list_dropdown = document.getElementById("course_list")
    let subject_container = document.getElementById("subject_container")
    subject_change(course_list_dropdown.value, subject_container)
    course_list_dropdown.addEventListener('change', () => subject_change(course_list_dropdown.value, subject_container))
}

async function subject_change(course_value, subject_container) {
    subject_container.innerHTML = ``
    await  fetch(subject_url, {
        'method': 'POST',
        'body': [course_value, 'get']
    })
        .then((response) => { return response.json() })
        .then((json) => {
            let subject_list = document.createElement('ul')
            for (let subject of json.subjects) {
                let subject_item = document.createElement('li')
                subject_item.textContent = subject
                subject_list.appendChild(subject_item)
                let delete_button = document.createElement('button')
                delete_button.textContent = 'Delete'
                delete_button.id = subject
                delete_button.addEventListener('click', async () => {
                    await fetch(subject_url, {
                        'method': 'POST',
                        'body': [course_value, subject, 'delete']
                    })
                    subject_change(course_value, subject_container)
                })
                subject_item.appendChild(delete_button)
            }
            subject_container.appendChild(subject_list)
        })
    let add_button = document.createElement('button')
    add_button.textContent = 'Add'
    add_button.addEventListener('click', () => add_subject(course_value, subject_container))
    subject_container.appendChild(add_button)
}

function add_subject(course_value, subject_container) {
    let input = document.createElement('input')
    input.type = 'text'
    input.placeholder = 'Subject'
    subject_container.appendChild(input)
    let ok = document.createElement('button')
    ok.textContent = 'OK'
    ok.addEventListener('click', async () => {
        let subject = input.value
        if (subject === "") {
            alert("Please enter a subject")
        } else {
            await fetch(subject_url, {
                'method': 'POST',
                'body': [course_value, subject, 'add']
            })
            subject_change(course_value, subject_container)
        }
    })
    subject_container.appendChild(ok)
}
