async function feedback_result(container) {
    await fetch(result_feedback_url)
        .then((response) => { return response.text() })
        .then((text) => {
            container.innerHTML = text
        })
}