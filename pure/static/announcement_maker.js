const everyone_checkbox = document.getElementById("target_everyone")
const faculty_checkbox = document.getElementById("target_faculty")
const student_checkbox = document.getElementById("target_students")

everyone_checkbox.addEventListener("change", () => {
    let checkboxes = document.getElementsByName("target")
    console.log(everyone_checkbox.checked)
    if(everyone_checkbox.checked){
        faculty_checkbox.disabled = 'true'
        student_checkbox.disabled = 'true'
        for(let i=0;i<checkboxes.length;i++){
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
        everyone_checkbox.disabled = 'true'
        student_checkbox.disabled = 'true'
        for(let i=0;i<checkboxes.length;i++){
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
