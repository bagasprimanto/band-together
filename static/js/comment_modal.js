document.addEventListener('DOMContentLoaded', function () {
    let deleteCommentModal = document.getElementById('deleteCommentModal');
    deleteCommentModal.addEventListener('show.bs.modal', function (event) {
        let button = event.relatedTarget;
        let deleteUrl = button.getAttribute('data-comment-delete-url');
        let authorImageUrl = button.getAttribute('data-comment-author-image-url');
        let authorDisplayNameLink = button.getAttribute('data-comment-author-url');
        let authorDisplayName = button.getAttribute('data-comment-author-display-name');
        let commentCreated = button.getAttribute('data-comment-created');
        let commentBody = button.getAttribute('data-comment-body');

        // Update the modal content
        let modal = deleteCommentModal;
        modal.querySelector('#modal-comment-author-picture').src = authorImageUrl;
        modal.querySelector('#modal-author-display-name').textContent = authorDisplayName;
        modal.querySelector('#modal-author-display-name-link').parentElement.href = authorDisplayNameLink;
        modal.querySelector('#modal-commment-created').textContent = ' | ' + commentCreated + ' ago';
        modal.querySelector('#modal-comment-body').textContent = commentBody;

        // Update the form action URL
        modal.querySelector('#comment-delete-form').action = deleteUrl;
    });
});