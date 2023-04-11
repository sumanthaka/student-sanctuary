async function feedback_draft(container) {
    await fetch(draft_feedback_url)
        .then((response) => { return response.text() })
        .then((text) => {
            container.innerHTML = text
            const script = document.createElement('script')
            script.src = '/target.js'
            document.body.appendChild(script)
        })
    let form_dropdown = document.getElementById('form_list')
    if(form_dropdown.childElementCount === 0) {
        let add_question = document.getElementById('add_question')
        add_question.style = "display: none"
        let save_form = document.getElementById('save_form')
        save_form.style = "display: none"
        let delete_form = document.getElementById('delete_form')
        delete_form.style = "display: none"
        let publish_form = document.getElementById('publish_form')
        publish_form.style = "display: none"
    }
    else {
        get_draft_questions(form_dropdown.value)
    }
    form_dropdown.addEventListener('change', async (event) => { await get_draft_questions(form_dropdown.value) })

    let ok_question = document.getElementById('ok_question')
    ok_question.addEventListener('click', async (event) => {
        let question = document.getElementById('question')
        if(question.value === "") {
            alert("Question cannot be empty!")
            return
        }
        let question_list = document.getElementById('questions_list')
        let question_item = document.createElement('li')
        question_item.id = "question_" + question_list.childElementCount
        question_item.className = "list-group-item d-flex justify-content-between align-items-center"
        question_item.style = "color: white;background: transparent"
        let span = document.createElement('span')
        span.style = "font-size: 1.6rem"
        span.textContent = question.value
        question_item.appendChild(span)
        let a = document.createElement('a')
        a.style = "cursor:pointer;"
        a.onclick = () => { delete_question(question_item.id) }
        let img = document.createElement('img')
        img.src = delete_icon
        img.width = 36
        img.height = 34
        a.appendChild(img)
        question_item.appendChild(a)
        question_list.appendChild(question_item)
    })

    let save_form = document.getElementById('save_form')
    save_form.addEventListener('click', async (event) => {
        let question_list = document.getElementById('questions_list')
        let questions = []
        for(let i=0; i<question_list.childElementCount; i++) {
            questions.push(question_list.children[i].children[0].textContent)
        }
        await fetch(draft_feedback_url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'form_id': form_dropdown.value,
                'questions': questions,
                'type': 'save'
            })
        })
            .then(alert("Form saved successfully!"))
    })

    let ok_form = document.getElementById('ok_form')
    ok_form.addEventListener('click', async (event) => {
        let form_title = document.getElementById('form_name')
        if(form_title.value === "") {
            alert("Form title cannot be empty!")
            return
        }
        fetch(draft_feedback_url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'form_title': form_title.value,
                'type': 'create'
            })
        })
            .then(location.reload())
    })

    let delete_form = document.getElementById('delete_form')
    delete_form.addEventListener('click', async (event) => {
        let sure = confirm("Are you sure you want to delete this form?")
        if(!sure) return
        let form_dropdown = document.getElementById('form_list')
        fetch(draft_feedback_url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'form_id': form_dropdown.value,
                'type': 'delete'
            })
        })
            .then(location.reload())
    })

    let ok_publish_form = document.getElementById('ok_publish_form')
    ok_publish_form.addEventListener('click', async (event) => {
        let form_dropdown = document.getElementById('form_list')
        let target = []
        let target_everyone = document.getElementById('target_everyone')
        if(target_everyone.checked) {
            target.push('Everyone')
        }
        else if (document.getElementById('target_faculty').checked) {
            target.push('All Faculty')
        }
        else {
            let targeted_students = document.getElementsByName('target')
            for (let i = 0; i < targeted_students.length; i++) {
                if (targeted_students[i].checked) {
                    target.push(targeted_students[i].id.split('_')[1])
                }
            }
        }
        fetch(draft_feedback_url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'form_id': form_dropdown.value,
                'target': target,
                'type': 'publish'
            })
        })
            .then(location.reload())
    })
}

async function get_draft_questions(form_id) {
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
                let a = document.createElement('a')
                a.style = "cursor:pointer;"
                a.onclick = () => { delete_question(question_item.id) }
                let img = document.createElement('img')
                img.src = delete_icon
                img.width = 36
                img.height = 34
                a.appendChild(img)
                question_item.appendChild(a)
                question_list.appendChild(question_item)
            }
        })
}

function delete_question(id) {
    let question = document.getElementById(id)
    question.remove()
}