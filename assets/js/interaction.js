"use strict";

let current_dropdown = null;

const control_bar_actions = document.getElementsByClassName("control-bar-action");
for (let action of control_bar_actions) {
    action.classList.remove("no-js");

    action.addEventListener("click", function(e) {
        if (current_dropdown && current_dropdown != e.target) {
            current_dropdown.classList.remove("active-dropdown-menu")
        };

        if (action.classList.contains("active-dropdown-menu")) {
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
    };
});