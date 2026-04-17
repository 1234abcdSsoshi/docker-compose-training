document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".js-confirm-delete");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            const ok = window.confirm("この日記を削除してもよろしいですか？");
            if (!ok) {
                event.preventDefault();
            }
        });
    });

    const flashMessages = document.querySelectorAll(".flash-message");
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach((message) => {
                message.style.opacity = "0";
                message.style.transition = "opacity 0.4s ease";
                setTimeout(() => {
                    message.remove();
                }, 400);
            });
        }, 3000);
    }
});