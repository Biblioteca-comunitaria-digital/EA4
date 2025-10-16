const form = document.getElementById("registro");

form.addEventListener("submit", function(event) {
    event.preventDefault();

    const contraseña = document.getElementById("contraseña").value;
    const reingreso = document.getElementById("reingreso").value;
    const mensaje = document.getElementById("mensaje");
    
    if (contraseña === reingreso) { 
        mensaje.textContent = "✅ Registro exitoso. Redirigiendo al inicio de sesión...";
        mensaje.style.color = "green";

        setTimeout(() => {
            window.location.href = "inicio_sesion.html";
        }, 2000);

    } else {
        mensaje.textContent = "⚠️ Las contraseñas no coinciden. Intente nuevamente.";
        mensaje.style.color = "red";
    }
});
