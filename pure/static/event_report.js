let delete_event_url = document.currentScript.getAttribute('delete_event_url')
let generate_report_url = document.currentScript.getAttribute('generate_report_url')
let loading = document.getElementById('loading')

async function delete_event(event_id) {
    await fetch(delete_event_url, {
        'method': 'POST',
        'body': event_id
    })
        .then(() => {
            location.reload()
        })
}

async function generate_report(event_id) {
    let actual_id = event_id.split('_')[1]
    let div_download_report = document.getElementById('down_report')
    let generate_report_button = document.getElementById(event_id)
    generate_report_button.style.display = 'none'
    loading.style.display = 'block'
    await fetch(generate_report_url, {
        'method': 'POST',
        'body': actual_id
    })
        .then((response) => {
            return response.blob()
        })
        .then((file_blob) => {
            let hidden_a = document.createElement('a')
            hidden_a.href = URL.createObjectURL(file_blob)
            hidden_a.download = "marks_template"
            div_download_report.appendChild(hidden_a)
            hidden_a.click()
            loading.style.display = 'none'
            generate_report_button.style.display = 'block'
        })
}