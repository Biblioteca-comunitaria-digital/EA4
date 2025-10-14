const form = document.getElementById("inicio-sesion");

form.addEventListener("submit", function(event) {
    event.preventDefault();

    const Usuario = document.getElementById("Usuario").value;
    const contraseña = document.getElementById("contraseña").value;
    const mensaje = document.getElementById("mensaje");

    const usuarioValido = "UsuarioEjemplo";
    const contraseñaValida = "123456";

    if (Usuario === usuarioValido && contraseña === contraseñaValida) {
        mensaje.textContent = "✅ Inicio de sesión exitoso. Redirigiendo...";
        mensaje.style.color = "green";

        setTimeout(() => {
        window.location.href = "./index.html";
        }, 2000);
    
    } else {
        mensaje.textContent = "⚠️ Usuario o contraseña incorrectos. Intente nuevamente.";
        mensaje.style.color = "red";
    }
});
