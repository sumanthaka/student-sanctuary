async function feedback_result(container) {
    await fetch(result_feedback_url)
        .then((response) => { return response.text() })
        .then((text) => {
            container.innerHTML = text
        })
    let form_dropdown = document.getElementById('form_list')
    let faculty_list = document.getElementById('faculty_list')
    form_dropdown.addEventListener('change', async (event) => {
        await get_faculty(form_dropdown.value)
        await get_result_questions(form_dropdown.value)
        await get_result(form_dropdown.value, faculty_list.value)
    })
    faculty_list.addEventListener('change', async (event) => {
        await get_result(form_dropdown.value, faculty_list.value)
    })
    await get_faculty(form_dropdown.value)
    await get_result_questions(form_dropdown.value)
    await get_result(form_dropdown.value, faculty_list.value)
}

async function get_faculty(form_id) {
    let faculty_list = document.getElementById('faculty_list')
    faculty_list.innerHTML = ""
    await fetch(result_feedback_url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            'form_id': form_id,
            'type': 'get_faculty'
        })
    })
    .then(response => response.json())
    .then((json) => {
        let faculties = json.faculty
        for (let i = 0; i < faculties.length; i++) {
            let faculty = faculties[i]
            let option = document.createElement('option')
            option.value = faculty._id
            option.textContent = faculty.name
            faculty_list.appendChild(option)
        }
    })
}

async function get_result_questions(form_id) {
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

async function get_result(form_id, faculty_id) {
    await fetch(result_feedback_url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            'form_id': form_id,
            'faculty_id': faculty_id,
            'type': 'get_result'
        })
    })
        .then(response => response.json())
        .then((json) => {
            let result = json.result
            for(let i=0; i<result.length; i++) {
                let question_item = document.getElementById('question_' + i)
                if(question_item.children.length > 1) {
                    question_item.children[1].remove()
                }
                let span = document.createElement('span')
                span.style = "font-size: 1.6rem"
                span.textContent = result[i]
                question_item.appendChild(span)
            }
        })
}