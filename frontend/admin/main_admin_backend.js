
document.addEventListener("DOMContentLoaded", () => {
    const usuario = JSON.parse(localStorage.getItem("usuario"));
    if (!usuario || usuario.rol !== "admin") {
        alert("Acceso denegado. Solo para administradores.");
        window.location.href = "index.html";
        return;
    }

    const API = "http://localhost:5000";
    const form = document.getElementById("formProducto");
    const lista = document.getElementById("adminLista");

    if (!form || !lista) {
        console.error("Formulario o lista no encontrada en admin.html");
        return;
    }

    function cargarProductos() {
        fetch(`${API}/api/productos`)
            .then(res => res.json())
            .then(data => {
                lista.innerHTML = "";
                data.forEach(p => {
                    const div = document.createElement("div");
                    div.innerHTML = `
                        <img src="${p.urlImagen}" alt="${p.nombre}" width="60">
                        <strong>${p.nombre}</strong>
                        <span>$${p.valor}</span>
                        <span>Stock: ${p.existencia}</span>
                    `;
                    lista.appendChild(div);
                });
            });
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const nuevoProducto = {
            nombre: document.getElementById("nombre").value,
            valor: parseFloat(document.getElementById("valor").value),
            existencia: parseInt(document.getElementById("existencia").value),
            urlImagen: document.getElementById("urlImagen").value
        };

        fetch(`${API}/api/productos`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(nuevoProducto)
        })
        .then(res => res.json())
        .then(data => {
            alert("Producto creado con éxito");
            form.reset();
            cargarProductos();
        })
        .catch(err => {
            console.error("Error al crear producto:", err);
            alert("Error al crear producto");
        });
    });

    cargarProductos();
});
