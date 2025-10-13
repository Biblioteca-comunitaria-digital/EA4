const form = document.getElementById("registro");

form.addEventListener("submit", function(event) {
    event.preventDefault();

    const contraseña = document.getElementById("contraseña").value;
    const reingreso = document.getElementById("reingreso").value;

    if (contraseña === reingreso) { 
        window.location.href = 'inicio_sesion.html';}
})
