let delete_url = document.currentScript.getAttribute("delete_url")
async function delete_college(college) {
    let sure = confirm("Are you sure you want to delete?")
    if (sure) {
        await fetch(delete_url, {
            'method': 'POST',
            'body': college
        })
            .then(response => {
                location.reload()
            })
    }
}