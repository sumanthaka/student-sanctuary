async function faculty_approval(container) {
    await fetch(approval_url)
        .then((response) => {
            return response.text()
        })
        .then((text) => {
            container.innerHTML = text
        })
}

async function approve_faculty(email, approval) {
    await fetch(approval_url, {
        'method': 'POST',
        'body': [email, approval]
    })
    faculty_approval(container)
}
