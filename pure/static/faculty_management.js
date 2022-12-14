async function faculty_management(container) {
    await fetch(faculty_manage_url)
        .then((response) => { return response.text() })
        .then((text) => {
                container.innerHTML = text
            })
}

async function faculty_class_update(faculty_id) {
    let faculty_class = document.getElementById(faculty_id).value
    await fetch(faculty_manage_url, {
        'method': 'POST',
        'body': [faculty_id, faculty_class]
    })
}