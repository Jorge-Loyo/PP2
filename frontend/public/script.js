// Transición de index.html a login.html
document.getElementById("enter-btn")?.addEventListener("click", function() {
    window.location.href = "login.html";
});

// Validación de login (simplificada)
document.getElementById("login-form")?.addEventListener("submit", function(e) {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    if (username === "admin" && password === "1234") { // Credenciales de ejemplo
        window.location.href = "main.html";
    } else {
        alert("Usuario o contraseña incorrectos");
    }
});
document.getElementById('logout-btn').addEventListener('click', function(e) {
    e.preventDefault();
    
    // Animación de desvanecimiento
    document.querySelector('.dashboard').style.animation = 'fadeOut 0.5s forwards';
    
    setTimeout(() => {
        window.location.href = 'login.html';
    }, 500); // Coincide con la duración de la animación
});



// Navegación entre pestañas en main.html
document.querySelectorAll(".menu a").forEach(link => {
    link.addEventListener("click", function(e) {
        e.preventDefault();
        // Oculta todos los contenidos
        document.querySelectorAll(".tab-content").forEach(tab => {
            tab.style.display = "none";
        });
        // Muestra el contenido seleccionado
        const target = this.getAttribute("href").substring(1);
        document.getElementById(target).style.display = "block";
        
        // Actualiza el menú activo
        document.querySelectorAll(".menu a").forEach(a => {
            a.classList.remove("active");
        });
        this.classList.add("active");
    });
});