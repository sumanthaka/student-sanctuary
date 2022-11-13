const college_dropdown = document.getElementById("college")
const course_dropdown = document.getElementById("course")

college_dropdown.addEventListener('change', async () => {
    college = college_dropdown.value
    await fetch('/course_options/' + college)
        .then(response => response.json())
        .then(data => {
            course_dropdown.innerHTML = ''
            for(let i=0;i<data.length;i++){
                let option = document.createElement("option")
                option.value = data[i]
                option.textContent = data[i]
                course_dropdown.appendChild(option)
            }
        })
})
