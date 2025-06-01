
document.addEventListener("DOMContentLoaded", () => {
    const API = "http://localhost:5000";
    const usuario = JSON.parse(localStorage.getItem("usuario"));

    if (!usuario) {
        alert("Debes iniciar sesión.");
        window.location.href = "registro.html";
        return;
    }

    const contenedor = document.getElementById("checkoutContenido");
    const totalElemento = document.getElementById("checkoutTotal");
    const btnFinalizar = document.getElementById("finalizarBtn");

    let productos = [];

    fetch(`${API}/api/carrito/${usuario.id}`)
        .then(res => res.json())
        .then(data => {
            productos = data;
            let total = 0;
            contenedor.innerHTML = "";
            data.forEach(item => {
                const fila = document.createElement("div");
                fila.className = "item-checkout";
                fila.innerHTML = `
                    <img src="${item.urlImagen}" alt="${item.nombre}" width="50">
                    <span>${item.nombre}</span>
                    <span>$${item.precio} x ${item.cantidad}</span>
                `;
                contenedor.appendChild(fila);
                total += item.precio * item.cantidad;
            });
            totalElemento.textContent = `Total: $${total}`;
        });

    btnFinalizar.addEventListener("click", () => {
        const items = productos.map(p => ({
            producto_id: p.producto_id,
            cantidad: p.cantidad,
            precio_unitario: p.precio
        }));

        fetch(`${API}/api/ordenes`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                usuario_id: usuario.id,
                items
            })
        })
        .then(res => res.json())
        .then(() => {
            alert("Compra finalizada con éxito");
            window.location.href = "index.html";
        })
        .catch(err => {
            console.error("Error al finalizar compra:", err);
            alert("Error al procesar tu compra");
        });
    });
});
