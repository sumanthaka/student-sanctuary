email: contactus.studentsanctuary@gmail.com
password: SS*CUcontactsanctuary

{% macro course_manage(courses) %}
    <ul>
        {% for course in courses %}
            <li>{{ course }}</li>
        {% endfor %}
    </ul>
    <button onclick="take_input()">Add</button>
    <button>Remove</button>
    <div id="input_container"></div>
{% endmacro %}


<script>
        manager = document.getElementById("manager")
        course_code = `{{ course_manage(courses) }}`
        manager.addEventListener("change", () => {
            console.log(manager.value)
            if(manager.value === "Course"){
                console.log("Working")
                document.getElementById("container").innerHTML=course_code
            } else if(manager.value === "Approval"){
                document.getElementById("container").innerHTML=``
            }
        })
    </script>

function take_input() {
    const container = document.getElementById("input_container")
    let input_tag = document.createElement("input")
    input_tag.type = "text"
    input_tag.id = "input_box"
    container.appendChild(input_tag)
    const ok_button = document.createElement("button")
    ok_button.addEventListener("click", ok_click)
    ok_button.textContent = "OK"
    container.appendChild(ok_button)
}

function ok_click() {
    let input_tag_rem = document.getElementById("input_box")
    const value = input_tag_rem.value
    if(value === "") {
        alert("Please enter a value")
    } else {
        input_tag_rem.remove()
        this.remove()
        return value
    }
}