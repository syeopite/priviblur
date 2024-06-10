"use strict";

let current_dropdown = null;

const control_bar_actions = document.getElementsByClassName("control-bar-action");
for (let action of control_bar_actions) {
    action.classList.remove("no-js");
    let dropdown = action.getElementsByClassName("control-bar-dropdown-menu")[0]

    action.addEventListener("click", function(e) {

        // Get the root element of the currently clicked dropdown
        // This is used to check if the element we've clicked on is apart of the currently active dropdown
        // and if so disable it (unless its part of the options)
        let target;
        if (e.target != action) {
            target = e.target.closest(".control-bar-action")
        } else {
            target = action
        }

        if (current_dropdown && current_dropdown != target) {
            current_dropdown.classList.remove("active-dropdown-menu")
        };

        if (action.classList.contains("active-dropdown-menu") && !dropdown.contains(e.target)) {
            current_dropdown = null;
            action.classList.remove("active-dropdown-menu")
        } else {
            action.classList.add("active-dropdown-menu");
            current_dropdown = action;
        };
    });
};

document.addEventListener("click", function(event) {
    if (current_dropdown && current_dropdown != event.target && !current_dropdown.contains(event.target)) {
        current_dropdown.classList.remove("active-dropdown-menu")
        current_dropdown = null;
    }
});