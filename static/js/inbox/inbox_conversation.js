jQuery(document).ready(function () {
    $(".chat-list a").click(function (event) {
        event.preventDefault(); // Prevent the default link behavior
        var targetUrl = $(this).attr("href");

        // Check if the current URL is exactly "/inbox/" or if the target URL is different from the current URL
        if (window.location.pathname !== targetUrl) {
            // Redirect to the target URL
            window.location.href = targetUrl;
        } else {
            // Add the showbox class to chatbox
            $(".chatbox").addClass('showbox');
        }
    });

    $(".chat-icon").click(function () {
        $(".chatbox").removeClass('showbox');
    });
});