document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form"); // Assuming there's only one form on the page
    const submitButton = form.querySelector("input[type='submit']");
    let formIsChanged = false;

    initFormHash(form); // Initialize the form hash

    form.addEventListener("input", function () {
        formIsChanged = formChanged(form); // Check if form is changed on any input
    });

    submitButton.addEventListener("click", function () {
        // Temporarily disable the beforeunload event when the form is being submitted
        window.removeEventListener("beforeunload", beforeUnloadHandler);
    });

    window.addEventListener("beforeunload", beforeUnloadHandler);

    function beforeUnloadHandler(e) {
        if (formIsChanged) {
            const confirmationMessage = 'You have unsaved changes. Are you sure you want to leave this page?';
            e.returnValue = confirmationMessage; // Standard for most browsers
            return confirmationMessage;          // Standard for most modern browsers
        }
    }
});

function initFormHash(form) {
    form.setAttribute("data-initial-hash", getFormHash(form));
}

function getFormHash(form) {
    const formValues = {};

    form.querySelectorAll("input, textarea, select").forEach(input => {
        const inputType = input.getAttribute("type");
        const inputName = input.getAttribute("name");

        if (inputType === "hidden" || !inputName) return;

        if (inputType === "checkbox" || inputType === "radio") {
            formValues[inputName] = input.checked;
        } else {
            formValues[inputName] = input.value;
        }
    });

    return JSON.stringify(formValues);
}

function formChanged(form) {
    return (form.getAttribute("data-initial-hash") !== getFormHash(form));
}      