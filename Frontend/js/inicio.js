const form = document.getElementById("inicio-sesion");

form.addEventListener("submit", function(event) {
    event.preventDefault();

    const Usuario = document.getElementById("Usuario").value;
    const contraseña = document.getElementById("contraseña").value;

    const usuarioValido = "UsuarioEjemplo";
    const contraseñaValida = "123456";

    if (Usuario === usuarioValido && contraseña === contraseñaValida) {

        window.location.href = './index.html';
    } else {

    }
});
