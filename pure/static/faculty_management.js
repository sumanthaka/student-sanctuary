async function faculty_management(container) {
    await fetch(faculty_manage_url)
        .then((response) => { return response.text() })
        .then((text) => {
                container.innerHTML = text
                manage_faculty_dropdown(document.getElementById("faculty").value)
            })
}

async function manage_faculty_dropdown(faculty_id) {
    let course_dropdown = document.getElementById("courses")
    let subject_list = document.getElementById("subjects")
    subject_list.innerHTML = ``
    await fetch(faculty_manage_url, {
        'method': 'POST',
        "headers": {"Content-Type": "application/json"},
        'body': JSON.stringify({'faculty_id': faculty_id, 'get_details': true})
    })
        .then((response) => { return response.json() })
        .then((json) => {
            course_dropdown.value = json.course_faculty
            for(let subject of json.subjects) {
                let subject_item = document.createElement('li')
                subject_item.textContent = subject[0] + ' (' + subject[1] + ')'
                subject_item.id = subject[2]
                subject_item.className = "list-group-item d-flex justify-content-between align-items-center"
                subject_item.style = "color: white;background: transparent"
                let delete_sub = document.createElement('a')
                let del_img = document.createElement('img')
                del_img.src = "/static/delete_icon.png"
                del_img.style = "width: 36px;height: 34px;cursor: pointer"
                delete_sub.appendChild(del_img)
                delete_sub.addEventListener("click", () => {
                    subject_item.remove()
                })
                subject_item.appendChild(delete_sub)
                subject_list.appendChild(subject_item)
            }
        })
}

function add_faculty_subject() {
    let subject_selection = document.getElementById("add_subject")
    let subject_id = subject_selection.value
    let subjects_list = document.getElementById("subjects").children
    for(let subject of subjects_list) {
        if(subject.id === subject_id) {
            return
        }
    }
    let subject_item = document.createElement('li')
    subject_item.textContent = subject_selection.options[subject_selection.selectedIndex].text
    subject_item.id = subject_id
    subject_item.className = "list-group-item d-flex justify-content-between align-items-center"
    subject_item.style = "color: white;background: transparent"
    let delete_sub = document.createElement('a')
    let del_img = document.createElement('img')
    del_img.src = "/static/delete_icon.png"
    del_img.style = "width: 36px;height: 34px;cursor: pointer"
    delete_sub.appendChild(del_img)
    delete_sub.addEventListener("click", () => {
                    subject_item.remove()
    })
    subject_item.appendChild(delete_sub)
    document.getElementById("subjects").appendChild(subject_item)
}


async function faculty_update() {
    let faculty_id = document.getElementById("faculty").value
    let course = document.getElementById("courses").value
    let subjects = document.getElementById("subjects").children
    let subject_ids = []
    for(let subject of subjects) {
        subject_ids.push(subject.id)
    }
    let faculty_data = {
        'faculty_id': faculty_id,
        'course': course,
        'subjects': subject_ids,
        'update': true
    }
    await fetch(faculty_manage_url, {
        'method': 'POST',
        "headers": {"Content-Type": "application/json"},
        'body': JSON.stringify(faculty_data)
    })
        .then((response) => { return response.json() })
        .then((json) => {
            if(json.status === true) {
                alert('Faculty updated successfully')
            }
        })
}