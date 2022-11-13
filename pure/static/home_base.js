function check_login(obj_id, url) {
    current_button = document.getElementById(obj_id)
    current_button.onclick= () => {
        location.href = url
    }
}