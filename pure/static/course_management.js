async function course_management(container) {
    await fetch(course_url)
        .then((response) => { return response.text() })
        .then((text) => {
                container.innerHTML = text
            })

    let ok_button = document.getElementById('ok')
    ok_button.addEventListener('click', () => { add_course() })
}

async function add_course() {
    const course = document.getElementById('course_input').value
    if (course === "") {
        alert("Please enter a course")
    } else {
        await fetch(course_url, {
            'method': 'POST',
            'body': [course, 'add']
        })
        course_management(container)
    }
}

async function delete_course(button_id) {
    await fetch(course_url, {
        'method': 'POST',
        'body': [button_id, 'delete']
    })
    course_management(container)
}