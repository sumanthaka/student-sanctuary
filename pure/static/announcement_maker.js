let everyone_checkbox = document.getElementById("target_everyone")
let faculty_checkbox = document.getElementById("target_faculty")
const student_checkbox = document.getElementById("target_students")

if(everyone_checkbox === null) {
    everyone_checkbox = document.createElement("input")
    everyone_checkbox.type = "checkbox"
}

if(faculty_checkbox === null) {
    faculty_checkbox = document.createElement("input")
    faculty_checkbox.type = "checkbox"
}

everyone_checkbox.addEventListener("change", () => {
    let checkboxes = document.getElementsByName("target")
    if(everyone_checkbox.checked){
        faculty_checkbox.checked = false
        student_checkbox.checked = false
        faculty_checkbox.disabled = 'true'
        student_checkbox.disabled = 'true'
        for(let i=0;i<checkboxes.length;i++){
            checkboxes[i].checked = false
            checkboxes[i].disabled = 'true'
        }
    } else {
        faculty_checkbox.disabled = false
        student_checkbox.disabled = false
        for(let i=0;i<checkboxes.length;i++){
            checkboxes[i].disabled = false
        }
    }

})

faculty_checkbox.addEventListener("change", () => {
    let checkboxes = document.getElementsByName("target")
    if(faculty_checkbox.checked){
        everyone_checkbox.checked = false
        student_checkbox.checked = false
        everyone_checkbox.disabled = 'true'
        student_checkbox.disabled = 'true'
        for(let i=0;i<checkboxes.length;i++){
            checkboxes[i].checked = false
            checkboxes[i].disabled = 'true'
        }
    } else {
        everyone_checkbox.disabled = false
        student_checkbox.disabled = false
        for(let i=0;i<checkboxes.length;i++){
            checkboxes[i].disabled = false
        }
    }

})

student_checkbox.addEventListener("change", () => {
    let checkboxes = document.getElementsByName("target")
    if(student_checkbox.checked){
        everyone_checkbox.disabled = 'true'
        faculty_checkbox.disabled = 'true'
        for(let i=0;i<checkboxes.length;i++){
            checkboxes[i].checked = 'true'
        }
    } else {
        everyone_checkbox.disabled = false
        faculty_checkbox.disabled = false
        for(let i=0;i<checkboxes.length;i++){
            checkboxes[i].checked = false
        }
    }

})
