// ===============================
// Sidebar Toggle
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    const sidebarBtn = document.getElementById("sidebarCollapse");
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");

    if (sidebarBtn) {

        sidebarBtn.addEventListener("click", function () {

            sidebar.classList.toggle("active");
            content.classList.toggle("active");

        });

    }

});


// ===============================
// Auto Close Alerts
// ===============================

setTimeout(function () {

    let alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        alert.style.transition = "0.5s";
        alert.style.opacity = "0";

        setTimeout(function () {

            alert.remove();

        }, 500);

    });

}, 3000);


// ===============================
// Delete Confirmation
// ===============================

function confirmDelete() {

    return confirm("Are you sure you want to delete this patient?");

}


// ===============================
// Number Validation
// ===============================

document.querySelectorAll("input[type='number']").forEach(function (input) {

    input.addEventListener("input", function () {

        if (this.value < 0) {

            this.value = 0;

        }

    });

});


// ===============================
// Phone Number Validation
// ===============================

document.querySelectorAll("input[name='phone']").forEach(function (input) {

    input.addEventListener("input", function () {

        this.value = this.value.replace(/[^0-9]/g, "");

        if (this.value.length > 10) {

            this.value = this.value.slice(0, 10);

        }

    });

});


// ===============================
// Email Validation
// ===============================

document.querySelectorAll("input[type='email']").forEach(function (email) {

    email.addEventListener("blur", function () {

        if (this.value !== "" && !this.value.includes("@")) {

            alert("Please enter a valid email address.");

            this.focus();

        }

    });

});


// ===============================
// Loading Button Effect
// ===============================

document.querySelectorAll("form").forEach(function (form) {

    form.addEventListener("submit", function () {

        let btn = this.querySelector("button[type='submit']");

        if (btn) {

            btn.disabled = true;

            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';

        }

    });

});