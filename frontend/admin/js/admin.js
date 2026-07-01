document.addEventListener("DOMContentLoaded", function () {
    console.log("Admin JS loaded");

    // =========================
    // ACTIVE SIDEBAR MENU
    // =========================
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll(".sidebar a");

    sidebarLinks.forEach(function (link) {
        const href = link.getAttribute("href");

        if (!href) return;

        if (currentPath === href) {
            link.classList.add("active");
        }

        if (href !== "/admin/dashboard" && currentPath.startsWith(href)) {
            link.classList.add("active");
        }
    });

    // =========================
    // DELETE CONFIRMATION
    // =========================
    const deleteForms = document.querySelectorAll("form[data-confirm]");

    deleteForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const message = form.getAttribute("data-confirm") || "Yakin ingin menghapus data ini?";

            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });

    // =========================
    // AUTO HIDE ALERT
    // =========================
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-8px)";
            alert.style.transition = "0.3s ease";

            setTimeout(function () {
                alert.remove();
            }, 300);
        }, 3500);
    });

    // =========================
    // IMAGE PREVIEW BEFORE UPLOAD
    // =========================
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(function (input) {
        input.addEventListener("change", function () {
            const file = input.files[0];

            if (!file) return;

            if (!file.type.startsWith("image/")) {
                alert("File harus berupa gambar.");
                input.value = "";
                return;
            }

            const reader = new FileReader();

            reader.onload = function (event) {
                let preview = input.parentElement.querySelector(".upload-preview");

                if (!preview) {
                    preview = document.createElement("img");
                    preview.className = "upload-preview";
                    input.parentElement.appendChild(preview);
                }

                preview.src = event.target.result;
            };

            reader.readAsDataURL(file);
        });
    });

    // =========================
    // BUTTON LOADING WHEN SUBMIT
    // =========================
    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function () {
            const button = form.querySelector('button[type="submit"]');

            if (button) {
                button.dataset.originalText = button.innerText;
                button.innerText = "Memproses...";
                button.disabled = true;
            }
        });
    });
});