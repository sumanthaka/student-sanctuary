let apply_now = document.getElementById("apply_now");

apply_fire_animation = () => {
    apply_now.classList.add("font-effect-fire-animation");
}

apply_now.addEventListener("mouseover", apply_fire_animation);
apply_now.addEventListener("focus", apply_fire_animation);
apply_now.addEventListener("mouseout",() => {
    apply_now.classList.remove("font-effect-fire-animation")
})