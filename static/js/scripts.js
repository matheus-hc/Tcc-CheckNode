// window.addEventListener('DOMContentLoaded', event => {

//     // Toggle the side navigation
//     const sidebarToggle = document.body.querySelector('#sidebarToggle');
//     if (sidebarToggle) {
//         // Uncomment Below to persist sidebar toggle between refreshes
//         // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
//         //     document.body.classList.toggle('sb-sidenav-toggled');
//         // }
//         sidebarToggle.addEventListener('click', event => {
//             event.preventDefault();
//             document.body.classList.toggle('sb-sidenav-toggled');
//             localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
//         });
//     }

// });

// // Toggle do menu lateral
// document.addEventListener("DOMContentLoaded", function () {
//     const toggleButton = document.getElementById("sidebarToggle");
//     const wrapper = document.getElementById("wrapper");

//     if (toggleButton && wrapper) {
//         toggleButton.addEventListener("click", function () {
//             wrapper.classList.toggle("toggled");
//         });
//     }
// });

document.addEventListener("DOMContentLoaded", function () {
    // Toggle sidebar
    const sidebarToggle = document.getElementById("sidebarToggle");
    if (sidebarToggle) {
        sidebarToggle.addEventListener("click", function (e) {
            e.preventDefault();
            document.getElementById("wrapper").classList.toggle("toggled");
        });
    }

    // Hide flash messages after 3 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function (alert) {
        setTimeout(function () {
            const alertInstance = new bootstrap.Alert(alert);
            alertInstance.close();
        }, 3000);
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const toggleMenu = document.getElementById("toggleMenu");
    const sidebar = document.getElementById("sidebarToggle");

    toggleMenu.addEventListener("click", () => {
        sidebar.classList.toggle("hidden");
    });
});


