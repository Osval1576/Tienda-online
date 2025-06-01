
document.addEventListener("DOMContentLoaded", () => {
    //const API = "http://localhost:5000";
    const API = "https://18.191.184.146:5000";
    const usuario = JSON.parse(localStorage.getItem("usuario"));

    if (!usuario) {
        alert("Debes iniciar sesión.");
        window.location.href = "registro.html";
        return;
    }

    const contenedor = document.getElementById("historial");

    fetch(`${API}/api/ordenes/${usuario.id}`)
        .then(res => res.json())
        .then(ordenes => {
            if (!ordenes.length) {
                contenedor.innerHTML = "<p>No hay órdenes registradas.</p>";
                return;
            }

            ordenes.forEach(o => {
                const div = document.createElement("div");
                div.className = "orden";
                div.innerHTML = `
                    <h3>Orden #${o.orden_id} - ${new Date(o.fecha).toLocaleString()}</h3>
                    <ul>
                        ${o.items.map(i => `<li>${i.nombre} - ${i.cantidad} x $${i.precio_unitario}</li>`).join("")}
                    </ul>
                    <strong>Total: $${o.total}</strong>
                `;
                contenedor.appendChild(div);
            });
        })
        .catch(err => {
            console.error("Error al cargar historial:", err);
            contenedor.innerHTML = "<p>Error al cargar historial.</p>";
        });
});
