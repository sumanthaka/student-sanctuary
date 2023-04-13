let student_moderation_url = document.currentScript.getAttribute('student_moderation_url')

async function suspend_user(student_id) {
    await fetch(student_moderation_url, {
        method: 'POST',
        'body': student_id
    })
        .then(location.reload())
}