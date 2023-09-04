
// JavaScript para la barra de navegación dinámica
const navList = document.getElementById("nav-list");
const navItems = navList.querySelectorAll("li");
const navbar = document.getElementById("navbar");

navItems.forEach(item => {
    item.addEventListener("click", () => {
        navItems.forEach(navItem => {
            navItem.classList.remove("active");
        });
        item.classList.add("active");
    });
});

window.addEventListener("scroll", () => {
    if (window.scrollY > 0) {
        navbar.classList.add("scroll");
    } else {
        navbar.classList.remove("scroll");
    }
});


// JavaScript para el acordeón
const accordionItems = document.querySelectorAll(".accordion-item");

accordionItems.forEach(item => {
    const checkbox = item.querySelector("input[type='checkbox']");

    item.addEventListener("click", () => {
        checkbox.checked = !checkbox.checked;
    });
});
