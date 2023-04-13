async function student_moderation(container) {
    await fetch(student_mod_url)
        .then((response) => {
            return response.text()
        })
        .then((text) => {
            container.innerHTML = text
        })
}

async function unsuspend_student(student_email) {
    await fetch(student_mod_url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            student_email: student_email,
            action: "unsuspend",
        }),
    })
        .then(location.reload())
}

async function delete_student(student_email) {
    await fetch(student_mod_url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            student_email: student_email,
            action: "delete",
        }),
    })
        .then(location.reload())
}

async function ban_student(student_email) {
    await fetch(student_mod_url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            student_email: student_email,
            action: "ban",
        }),
    })
        .then(location.reload())
}