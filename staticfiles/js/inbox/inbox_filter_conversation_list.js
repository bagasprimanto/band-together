//For filtering the list of chatlist based on text input
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('inlineFormInputGroup');
    const conversationList = document.querySelectorAll('.chat-list .chat-item-list');

    searchInput.addEventListener('input', function () {
        const filter = searchInput.value.toLowerCase();
        conversationList.forEach(function (item) {
            const participantName = item.querySelector('.profile-display-name').innerText.toLowerCase();
            if (participantName.includes(filter)) {
                item.classList.remove('d-none');
            } else {
                item.classList.add('d-none');
            }
        });
    });
});