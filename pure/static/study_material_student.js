let notes_url = document.currentScript.getAttribute('notes_list')
let subject_dropdown = document.getElementById('subject')
let download_icon_src = document.currentScript.getAttribute('download_icon')
get_notes(subject_dropdown.value)
subject_dropdown.addEventListener('change', () => {
    get_notes(subject_dropdown.value)
})

async function get_notes(subject_id) {
    await fetch(notes_url, {
        method: 'POST',
        'body': [subject_id, 'get']
    })
    .then(response => response.json())
    .then(data => {
        let notes = data['notes']
        let notes_list = document.getElementById("notes_list")
        notes_list.innerHTML = ""
        for (let note in notes) {
            let li = document.createElement("li")
            li.id = notes[note]['_id']
            li.className = "list-group-item d-flex justify-content-between align-items-center"
            li.style = "color: white;background: transparent"
            let span = document.createElement("span")
            span.innerHTML = notes[note]['filename']
            let download_note = document.createElement("a")
            let download_icon = document.createElement("img")
            download_icon.src = download_icon_src
            download_icon.width = 40
            download_icon.height = 36
            download_note.addEventListener("click", () => {
                fetch(notes_url, {
                    'method': "POST",
                    'body': [notes[note]['_id'], 'download']
                })
                    .then(response => response.blob())
                    .then(file_blob => {
                        let hidden_a = document.createElement('a')
                        hidden_a.href = URL.createObjectURL(file_blob)
                        hidden_a.download = notes[note]['filename']
                        notes_list.appendChild(hidden_a)
                        hidden_a.click()
                    })
            })
            download_note.style = "cursor: pointer;margin-right: 2em"
            download_note.appendChild(download_icon)
            li.appendChild(span)
            li.appendChild(download_note)
            notes_list.appendChild(li)
        }
    })
}