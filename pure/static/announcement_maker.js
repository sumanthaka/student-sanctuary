let announcement_url = document.currentScript.getAttribute("announcement_url")

async function del_announcement(announcement_id) {
    await fetch(announcement_url, {
        'method': 'POST',
        'body': announcement_id
    })
    location.reload()
}