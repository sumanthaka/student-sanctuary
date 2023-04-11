let student_checkbox = document.getElementById('target_students')

student_checkbox.addEventListener("change", () => {
    let checkboxes = document.getElementsByName("target")
    if(student_checkbox.checked){
        for(let i=0;i<checkboxes.length;i++){
            checkboxes[i].checked = 'true'
        }
    } else {
        for(let i=0;i<checkboxes.length;i++){
            checkboxes[i].checked = false
        }
    }
})