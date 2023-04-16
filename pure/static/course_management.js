async function course_management(container) {
    await fetch(course_url)
        .then((response) => { return response.text() })
        .then((text) => {
                container.innerHTML = text
            })

    let ok_button = document.getElementById('ok')
    ok_button.addEventListener('click', () => { add_course() })

    let proceed_button = document.getElementById('proceed')
    proceed_button.addEventListener('click', () => { proceed() })
}

async function add_course() {
    const course = document.getElementById('course_input').value
    const batch_year = document.getElementById('batch_year').value
    const duration = document.getElementById("duration").value
    if (course === "") {
        alert("Please enter a course")
    } else {
        await fetch(course_url, {
            'method': 'POST',
            'body': [course,batch_year,duration, 'add']
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

async function proceed() {
    await fetch(course_url, {
        'method': 'POST',
        'body': ['proceed']
    })
        .then(alert("Semester successfully proceeded"))
    course_management(container)
}