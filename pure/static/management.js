const manager_dropdown = document.getElementById("manager")
const container = document.getElementById("container")
let course_url = document.currentScript.getAttribute("course_url")
let approval_url = document.currentScript.getAttribute("approval_url")
let role_url = document.currentScript.getAttribute("role_url")
let faculty_manage_url = document.currentScript.getAttribute("faculty_manage_url")
let subject_url = document.currentScript.getAttribute("subject_url")
let student_mod_url = document.currentScript.getAttribute("student_mod_url")

course_management(container)
manager_dropdown.addEventListener("change", () => {
    if (manager_dropdown.value === "Course") {
        course_management(container)
    } else if(manager_dropdown.value === "Approval") {
        faculty_approval(container)
    } else if(manager_dropdown.value === "Role") {
        role_management(container)
    } else if (manager_dropdown.value === "Faculty_manage") {
        faculty_management(container)
    } else if (manager_dropdown.value === "Subject") {
        subject_management(container)
    } else if (manager_dropdown.value === "Student_mod") {
        student_moderation(container)
    }
})


