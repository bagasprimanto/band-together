// For dismissing the create message modal when cancel button is clicked
document.addEventListener('DOMContentLoaded', function () {
    var cancelButton = document.getElementById('cancel-button');
    if (cancelButton) {
        cancelButton.addEventListener('click', function () {
            var createMessageModal = bootstrap.Modal.getInstance(document.getElementById('createMessageModal'));
            createMessageModal.hide();
        });
    }
});