const copyBookmarkletElement = document.getElementById("copy-as-bookmarklet");
copyBookmarkletElement.addEventListener("click", function(e) {
    e.preventDefault()

    navigator.clipboard.writeText(e.target.href).then(function() {
    }, function(err) {
        console.log("Unable to copy settings as bookmarklet")
    });
})