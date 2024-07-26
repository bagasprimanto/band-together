// For handling report modal
document.body.addEventListener('htmx:afterSwap', function (event) {

    // Check if the swap event is from the report form submission
    if (event.detail.target.id === 'reportFormContainer') {

        // Check if there are error messages
        var hasErrors = document.querySelector('#reportFormContainer .invalid-feedback') !== null;

        // Find the modal element and hide it
        if (!hasErrors) {
            var reportModal = document.getElementById('reportModal');
            var modal = bootstrap.Modal.getInstance(reportModal);
            modal.hide();

            // Clear the form fields
            document.getElementById('reportForm').reset();
        }
    }
});