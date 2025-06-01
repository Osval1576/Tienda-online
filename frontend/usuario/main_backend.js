
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formRegistro");
    if (!form) {
        console.error("Formulario de registro no encontrado (id=formRegistro)");
        return;
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const nombre = document.getElementById("nombre").value;
        const correo = document.getElementById("correo").value;
        const clave = document.getElementById("clave").value;
        const direccion = document.getElementById("direccion").value;
        const telefono = document.getElementById("telefono").value;

        const usuario = {
            nombre,
            correo,
            clave,
            direccion,
            telefono
        };

        fetch("https://18.191.184.146:5000/api/usuarios/registro", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(usuario)
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                alert("Usuario registrado correctamente");
                window.location.href = "index.html";
            }
        })
        .catch(err => {
            console.error("Error al registrar usuario:", err);
            alert("Hubo un error al registrar el usuario.");
        });
    });
});
