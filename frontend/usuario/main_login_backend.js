
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formLogin");

    if (!form) {
        console.error("Formulario de login no encontrado");
        return;
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const correo = document.getElementById("correo").value;
        const clave = document.getElementById("clave").value;

        fetch("https://18.191.184.146:5000/api/usuarios/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ correo, clave })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                localStorage.setItem("usuario", JSON.stringify(data));
                alert("Sesión iniciada correctamente");
                window.location.href = "index.html";
            }
        })
        .catch(err => {
            console.error("Error en login:", err);
            alert("Error al iniciar sesión");
        });
    });
});
