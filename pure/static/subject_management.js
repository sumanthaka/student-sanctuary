async function subject_management(container) {
    await fetch(subject_url)
        .then((response) => { return response.text() })
        .then((text) => {
                container.innerHTML = text
            })

    let course_list_dropdown = document.getElementById("course_list")
    let subject_list = document.getElementById("subject_list")
    let ok_subject = document.getElementById('ok_subject')

    subject_change(course_list_dropdown.value, subject_list)
    ok_subject.addEventListener('click', () => { add_subject(course_list_dropdown.value, subject_list) })
    course_list_dropdown.addEventListener('change', () => { subject_change(course_list_dropdown.value, subject_list) })
}

async function subject_change(course_value, subject_list) {
    subject_list.innerHTML = ``
    await  fetch(subject_url, {
        'method': 'POST',
        'body': [course_value, 'get']
    })
        .then((response) => { return response.json() })
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
                        'body': [course_value, subject, 'delete']
                    })
                    subject_change(course_value, subject_list)
                })
                subject_item.appendChild(delete_button)
                subject_list.appendChild(subject_item)
            }
        })
    // let add_button = document.createElement('button')
    // add_button.textContent = 'Add'
    // subject_container.appendChild(add_button)
}

async function add_subject(course_value, subject_list) {
    // let input = document.createElement('input')
    // input.type = 'text'
    // input.placeholder = 'Subject'
    // subject_container.appendChild(input)
    // let ok = document.createElement('button')
    // ok.textContent = 'OK'
    // ok.addEventListener('click', async () => {
    let subject_input = document.getElementById('subject_input')
    let subject = subject_input.value
        // let subject = input.value
    if (subject === "") {
        alert("Please enter a subject")
    } else {
        await fetch(subject_url, {
            'method': 'POST',
            'body': [course_value, subject, 'add']
        })
        subject_input.value = ""
        subject_change(course_value, subject_list)
    }
    // })
    // subject_container.appendChild(ok)
}
