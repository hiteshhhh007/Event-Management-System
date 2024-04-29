let body = document.querySelector('body');
let burger = document.getElementById('burger');
let sidebar = document.getElementById('sidebar');

burger.addEventListener('click', function() {
    body.classList.toggle('show-sidebar');
    sidebar.classList.toggle('sidebar__switching');
});