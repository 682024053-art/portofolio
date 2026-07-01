document.addEventListener("DOMContentLoaded", function () {
    // =========================
    // REVEAL ANIMATION
    // =========================
    const elements = document.querySelectorAll(
        ".section, .skill-card, .project-card, .timeline-item, .about-card, .contact-form"
    );

    elements.forEach(function (element) {
        element.classList.add("reveal");
    });

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }
        });
    }, {
        threshold: 0.15
    });

    elements.forEach(function (element) {
        observer.observe(element);
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
    // ACTIVE NAVBAR ON SCROLL
    // =========================
    const navLinks = document.querySelectorAll(".navbar a[href^='#']");
    const sections = document.querySelectorAll("section[id]");

    window.addEventListener("scroll", function () {
        let currentSection = "";

        sections.forEach(function (section) {
            const sectionTop = section.offsetTop - 120;

            if (window.scrollY >= sectionTop) {
                currentSection = section.getAttribute("id");
            }
        });

        navLinks.forEach(function (link) {
            link.classList.remove("active");

            if (link.getAttribute("href") === "#" + currentSection) {
                link.classList.add("active");
            }
        });
    });

    // =========================
    // SCROLL TO TOP BUTTON
    // =========================
    const scrollButton = document.createElement("button");
    scrollButton.className = "scroll-top-btn";
    scrollButton.innerHTML = "↑";
    document.body.appendChild(scrollButton);

    window.addEventListener("scroll", function () {
        if (window.scrollY > 400) {
            scrollButton.classList.add("show");
        } else {
            scrollButton.classList.remove("show");
        }
    });

    scrollButton.addEventListener("click", function () {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });
});