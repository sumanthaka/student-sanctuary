let get_questions_url = document.currentScript.getAttribute('get_questions_url')
let student_feedback_url = document.currentScript.getAttribute('student_feedback_url')
let form_dropdown = document.getElementById('form_list')
let faculty_list_container = document.getElementById('faculty_list_container')
let question_list = document.getElementById('questions_list')
let faculty_dropdown = document.getElementById('faculty_list')
let submit_button_container = document.getElementById('submit_container')
let submit_button = document.getElementById('submit')

get_questions(form_dropdown.value)
get_faculty(form_dropdown.value)
form_dropdown.addEventListener('change', async (event) => {
    await get_questions(form_dropdown.value)
    await get_faculty(form_dropdown.value)
})
faculty_dropdown.addEventListener('change', async (event) => { await get_faculty(form_dropdown.value) })
submit_button.addEventListener('click', async (event) => { await submit_feedback() })

async function get_questions(form_id) {
    await fetch(get_questions_url, {
        method: 'POST',
        body: form_id
    })
    .then(response => response.json())
    .then((json) => {
        let questions = json.questions
        for (let i = 0; i < questions.length; i++) {
            let question_item = document.createElement('li')
            question_item.id = "question_" + i
            question_item.className = "list-group-item d-flex justify-content-between align-items-center"
            question_item.style = "color: white;background: transparent"
            let span = document.createElement('span')
            span.style = "font-size: 1.6rem"
            span.textContent = questions[i]
            let radio_group = document.createElement('div')
            for (let j = 0; j < 5; j++) {
                let label = document.createElement('label')
                label.className = "form-check-label"
                label.textContent = j + 1
                label.style = "margin-right: 0.4em"
                radio_group.appendChild(label)
                let input = document.createElement('input')
                input.type = "radio"
                input.name = "question_" + i
                input.value = j + 1
                input.className = "form-check-input"
                input.style = "margin-right: 1em"
                input.required = true
                radio_group.appendChild(input)
            }
            question_item.appendChild(span)
            question_item.appendChild(radio_group)
            question_list.appendChild(question_item)
        }
    })
}

async function get_faculty(form_id) {
    let faculty_list = document.getElementById('faculty_list')
    faculty_list.innerHTML = ""
    await fetch(student_feedback_url, {
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
        if (faculties.length === 0) {
            try {
                document.getElementById('all_responses_submitted').remove()
            } catch (error) {}
            faculty_dropdown.style.display = 'none'
            document.getElementById('faculty_list_label').style.display = 'none'
            let h2 = document.createElement('h2')
            h2.textContent = "All responses have been submitted"
            h2.style = "color: white"
            h2.id = "all_responses_submitted"
            faculty_list_container.classList.remove("justify-content-md-end")
            faculty_list_container.classList.add("justify-content-md-center")
            faculty_list_container.appendChild(h2)
            question_list.innerHTML = ""
            submit_button.remove()
        } else {
            faculty_dropdown.style.display = 'block'
            document.getElementById('faculty_list_label').style.display = 'block'
            faculty_list_container.classList.remove("justify-content-md-center")
            faculty_list_container.classList.add("justify-content-md-end")
            submit_button_container.appendChild(submit_button)
            if (document.getElementById('all_responses_submitted')) {
                document.getElementById('all_responses_submitted').remove()
            }
        }
        for (let i = 0; i < faculties.length; i++) {
            let faculty = faculties[i]
            let option = document.createElement('option')
            option.value = faculty._id
            option.textContent = faculty.name
            faculty_list.appendChild(option)
        }
    })
}

async function submit_feedback() {
    let form_id = document.getElementById('form_list').value
    let faculty_id = document.getElementById('faculty_list').value
    let questions = document.getElementById('questions_list').children
    let answers = []
    for (let i = 0; i < questions.length; i++) {
        let question = questions[i]
        let answer = question.children[1].querySelector('input:checked').value
        answers.push(parseInt(answer))
    }
    let data = {
        form_id: form_id,
        faculty_id: faculty_id,
        answers: answers,
        'type': 'submit'
    }
    await fetch(student_feedback_url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(() => {
        alert("Feedback submitted successfully")
        location.reload()
    })
}