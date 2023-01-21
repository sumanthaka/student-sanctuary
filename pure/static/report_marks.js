let report_container = document.getElementById("report_container")

function get_report_req(type, report_url){
    fetch(report_url)
        .then(response => { return response.text() })
        .then(text => {
            report_container.innerHTML = text
            if(type === "exam_avg"){
                exam_report(report_url)
            } else {
                student_report(report_url)
            }
        })
}

function exam_report(report_url){
    let exams = document.getElementById("exams")
    let graph_container = document.getElementById("graph_container")
    set_graph(exams.value, graph_container, report_url)
    exams.addEventListener('change', () => { set_graph(exams.value, graph_container, report_url) })
}

function student_report(report_url){
    let students = document.getElementById("students")
    let graph_container = document.getElementById("graph_container")
    set_graph(students.value, graph_container, report_url)
    students.addEventListener('change', () => { set_graph(students.value, graph_container, report_url) })
}

async function set_graph(pid, graph_container, report_url){
    await fetch(report_url+'/'+pid)
        .then(response => { return response.json() })
        .then(json => {
            graph_container.innerHTML = json.div
            eval(json.script)
        })
}