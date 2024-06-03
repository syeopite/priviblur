const setting_locale_strings = JSON.parse(document.getElementById('setting_locale_strings').textContent);

const copyBookmarkletElement = document.getElementById("copy-as-bookmarklet");
copyBookmarkletElement.addEventListener("click", function(e) {
    e.preventDefault();

    const target = e.target.closest("#copy-as-bookmarklet");
    const icons = target.getElementsByTagName("svg");
    const textElement = target.getElementsByTagName("span")[0];

    if (textElement.innerText !== setting_locale_strings.copy_as_bookmarklet_text) {
        return
    }

    const linkIcon = icons[0];
    const checkIcon = icons[1];
    const errorIcon = icons[2];

    navigator.clipboard.writeText(target.href).then(() => {
        linkIcon.style.display = "none";
        checkIcon.style.display = "unset";
        textElement.innerText = setting_locale_strings.copy_as_bookmarklet_copy_confirmed;

        setTimeout(() => {
            linkIcon.style.display = "unset";
            checkIcon.style.display = "none";
            textElement.innerText = setting_locale_strings.copy_as_bookmarklet_text;
        }, 1000)
    }).catch(() => {
        textElement.innerText = setting_locale_strings.copy_as_bookmarklet_copy_failed;
        linkIcon.style.display = "none";
        errorIcon.style.display = "unset";

        setTimeout(() => {
            linkIcon.style.display = "unset";
            errorIcon.style.display = "none";
            textElement.innerText = setting_locale_strings.copy_as_bookmarklet_text;
        }, 1000);
    });
})
