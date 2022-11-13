async function course_management(container) {
    await fetch(course_url)
        .then((response) => { return response.text() })
        .then((text) => {
                container.innerHTML = text
            })

    const input_container = document.getElementById('input_container')
    const add_button = document.getElementById('add')

    add_button.addEventListener('click', () => add_course(input_container, add_button))
}

function add_course(input_container, add_button) {
    add_button.disabled = true
    const input = document.createElement('input')
    input.type = 'text'
    input.placeholder = 'Course'
    input_container.appendChild(input)
    const ok = document.createElement('button')
    ok.textContent = 'OK'
    ok.addEventListener('click', async () => {
        const course = input.value
        if (course === "") {
            alert("Please enter a course")
        } else {
            await fetch(course_url, {
                'method': 'POST',
                'body': [course, 'add']
            })
            input_container.removeChild(input)
            input_container.removeChild(ok)
            add_button.disabled = false
            course_management(container)
        }
    })
    input_container.appendChild(ok)
}

async function delete_course(button_id) {
    await fetch(course_url, {
        'method': 'POST',
        'body': [button_id, 'delete']
    })
    course_management(container)
}