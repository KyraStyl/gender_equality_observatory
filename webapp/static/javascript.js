// Set and get current language
function set_lang(lang_code) {
    document.cookie = "lang=" + lang_code;
    location.reload();
}

function get_lang() {
    return $('html').attr('lang') || "en";
}
// #Set and get current language

// Under Construction alert
$(".underConstruction").on("click", function () {
    let greek = get_lang() === "el"

    Swal.fire({
        title: greek ? "Υπό κατασκευή!" : "Under Construction!",
        text: greek ? "Αυτή η λειτουργία δεν είναι διαθέσιμη, ακόμα. Δοκιμάστε κάτι διαφορετικό!"
            : "This functionality is not available, yet. Try something else!",
        icon: "info",
        timer: 10000,
        timerProgressBar: true,
        confirmButtonText: greek ? "ΟΚ!" : "OK!"
    })
})
// #Under Construction alert