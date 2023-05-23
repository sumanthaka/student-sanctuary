let upload_button = document.getElementById('upload')

upload_button.addEventListener('click', () => {
    let ads_form = document.getElementById('ads_form')
    ads_form.submit()
})

function disp_image(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            let img = document.getElementById('ads_image')
            img.src = e.target.result;
        }
        reader.readAsDataURL(input.files[0])
    } else {
        let img = document.getElementById('ads_image')
        img.src = "/no-image.png"
    }
}