export function dropdownHiddenTogle() {
let element = document.querySelector(".select-selected")
element.addEventListener("click", toggle_hiddne_function);

function toggle_hiddne_function() {
    if (document.querySelector(".select-selected").textContent == "multiple_choice"){
        document.querySelector(".hidden-toggle").classList.toggle("hidden")
    }
    
 
}
}
