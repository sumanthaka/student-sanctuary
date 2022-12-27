async function subjects(upload_url) {
    let download_button = document.getElementById('download')
    download_button.disabled = true
    let div_down_template = document.getElementById('down_template')
    await fetch(upload_url, {
        'method': 'POST',
        'body': ['add']
    })
        .then((response) => {
            return response.blob()
        })
        .then((file_blob) => {
            let hidden_a = document.createElement('a')
            hidden_a.href = URL.createObjectURL(file_blob)
            hidden_a.download = "marks_template"
            div_down_template.appendChild(hidden_a)
            hidden_a.click()
        })
        .then(() => {
            fetch(upload_url, {
                'method': 'POST',
                'body': ['delete', document.cookie]
            })
        })
    download_button.disabled = false
}