async function feedback_open(container) {
    await fetch(open_feedback_url)
        .then((response) => { return response.text() })
        .then((text) => {
            container.innerHTML = text
        })
    let form_dropdown = document.getElementById('form_list')
    get_published_questions(form_dropdown.value)
    form_dropdown.addEventListener('change', async (event) => { await get_published_questions(form_dropdown.value) })
}

async function get_published_questions(form_id) {
    let question_list = document.getElementById('questions_list')
    question_list.innerHTML = ""
    await fetch(get_questions_url, {
        method: 'POST',
        'body': form_id
    })
        .then((response) => { return response.json() })
        .then((json) => {
            let questions = json.questions
            for(let i=0; i<questions.length; i++) {
                let question_item = document.createElement('li')
                question_item.id = "question_" + i
                question_item.className = "list-group-item d-flex justify-content-between align-items-center"
                question_item.style = "color: white;background: transparent"
                let span = document.createElement('span')
                span.style = "font-size: 1.6rem"
                span.textContent = questions[i]
                question_item.appendChild(span)
                question_list.appendChild(question_item)
            }
        })
}