let draft_button = document.getElementById("draft")
let open_button = document.getElementById("open")
let result_button = document.getElementById("result")
let container = document.getElementById("form_container")
let draft_feedback_url = document.currentScript.getAttribute("draft_feedback_url")
let open_feedback_url = document.currentScript.getAttribute("open_feedback_url")
let result_feedback_url = document.currentScript.getAttribute("result_feedback_url")
let get_questions_url = document.currentScript.getAttribute("get_questions_url")
let delete_icon = document.currentScript.getAttribute("delete_icon")
feedback_draft(container)

draft_button.addEventListener("click", () => {
    feedback_draft(container)
})

open_button.addEventListener("click", () => {
    feedback_open(container)
})

result_button.addEventListener("click", () => {
    feedback_result(container)
})