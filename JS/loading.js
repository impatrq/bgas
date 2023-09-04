document.addEventListener("DOMContentLoaded", function() {
    var loadingScreen = document.getElementById("loadingScreen");
    var content = document.getElementById("content");

    // Ocultar la pantalla de carga después de 2 segundos
    setTimeout(function() {
        loadingScreen.style.opacity = 0;
        setTimeout(function() {
            loadingScreen.style.display = "none";
            content.classList.remove("hidden");
        }, 500);
    }, 2000);
});
