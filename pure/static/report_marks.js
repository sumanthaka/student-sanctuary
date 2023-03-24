let report_container = document.getElementById("report_container")
let sem_val_dropdown = document.getElementById("sem")

function report_refresh(report_url, sem_value) {
    report_container.innerHTML = ``
    try {
        get_report_req("exam_avg", report_url, sem_value)
    }
    catch (err){
        console.log("No Exams")
    }
}

function get_report_req(type, report_url, sem_value){
    fetch(report_url, {
        method: 'POST',
        'body': sem_value
    })
        .then(response => { return response.text() })
        .then(text => {
            report_container.innerHTML = text
            if(type === "exam_avg"){
                exam_report(report_url)
            } else {
                student_report(report_url, sem_value)
            }
        })
}

function exam_report(report_url){
    let exams = document.getElementById("exams")
    let graph_container = document.getElementById("graph_container")
    set_graph(exams.value, graph_container, report_url)
    exams.addEventListener('change', () => { set_graph(exams.value, graph_container, report_url) })
}

function student_report(report_url, sem_value){
    let students = document.getElementById("students")
    let graph_container = document.getElementById("graph_container")
    set_graph_student(students.value, graph_container, report_url, sem_value)
    students.addEventListener('change', () => { set_graph_student(students.value, graph_container, report_url, sem_value) })
}

async function set_graph(pid, graph_container, report_url){
    await fetch(report_url+'/'+pid)
        .then(response => { return response.json() })
        .then(json => {
            graph_container.innerHTML = json.div
            eval(json.script)
        })
}

async function set_graph_student(pid, graph_container, report_url, sem_value){
    await fetch(report_url+'/'+pid+'/'+sem_value)
        .then(response => { return response.json() })
        .then(json => {
            graph_container.innerHTML = json.div
            eval(json.script)
        })
}