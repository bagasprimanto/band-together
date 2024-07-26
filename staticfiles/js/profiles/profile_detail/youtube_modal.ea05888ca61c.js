// For inserting the youtube video's embed URL inside the modal
var videoModal = document.getElementById('videoModal')
videoModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget // Button that triggered the modal
    var videoUrl = button.getAttribute('data-video-url') // Extract info from data-* attributes
    var modalTitle = videoModal.querySelector('.modal-title')
    var videoFrame = videoModal.querySelector('#videoFrame')

    // Update the modal's content.
    videoFrame.src = videoUrl
})

// Remove URL from videoframe src attribute when modal is dimissed
videoModal.addEventListener('hidden.bs.modal', function (event) {
    var videoFrame = videoModal.querySelector('#videoFrame')
    videoFrame.src = ''
})

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