document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript berhasil dimuat.");

    const deleteButtons = document.querySelectorAll(".delete-btn");
    deleteButtons.forEach(button => {
        button.addEventListener("click", event => {
            const confirmDelete = confirm("Apakah Anda yakin ingin menghapus tugas ini?");
            if (!confirmDelete) {
                event.preventDefault();
            }
        });
    });


    const taskForms = document.querySelectorAll("form");
    taskForms.forEach(form => {
        form.addEventListener("submit", event => {
            const title = form.querySelector("#title");
            const description = form.querySelector("#description");

            if (title && title.value.trim() === "") {
                alert("Judul tidak boleh kosong.");
                event.preventDefault();
            }

            if (description && description.value.trim() === "") {
                alert("Deskripsi tidak boleh kosong.");
                event.preventDefault();
            }
        });
    });

    const navLinks = document.querySelectorAll(".navbar-nav a");
    navLinks.forEach(link => {
        link.addEventListener("mouseover", () => {
            link.style.transform = "scale(1.1)";
            link.style.color = "#ffeb3b";
        });

        link.addEventListener("mouseout", () => {
            link.style.transform = "scale(1)";
            link.style.color = "";
        });
    });

    const usernameField = document.querySelector("#username");
    if (usernameField) {
        usernameField.focus();
    }
});

