//For storing and returning the create message modal content
document.addEventListener('DOMContentLoaded', function () {
    var originalModalContent = document.querySelector("#createMessageModal .modal-body").innerHTML;

    document.getElementById('createMessageModal').addEventListener('hidden.bs.modal', function () {
        document.querySelector("#createMessageModal .modal-body").innerHTML = originalModalContent;
        htmx.process(document.querySelector("#createMessageModal .modal-body")); // Reinitialize HTMX on the new content
    });

    document.addEventListener('click', function (event) {
        if (event.target && event.target.id === 'cancel-button') {
            document.querySelector("#createMessageModal .modal-body").innerHTML = originalModalContent;
            htmx.process(document.querySelector("#createMessageModal .modal-body")); // Reinitialize HTMX on the new content
        }
    });
});