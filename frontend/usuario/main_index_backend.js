
document.addEventListener("DOMContentLoaded", () => {
    const API = "https://18.191.184.146:5000";

   // const API = "http://127.0.0.1:5000";
    const contenedor = document.getElementById("contenedor");
    const numero = document.getElementById("numero");

    const usuario = JSON.parse(localStorage.getItem("usuario"));
    if (!usuario) {
        alert("Debes iniciar sesión primero.");
        window.location.href = "registro.html";
        return;
    }

    // Cargar productos
    fetch(`${API}/api/productos`)
        .then(res => res.json())
        .then(productos => {
            contenedor.innerHTML = "";
            productos.forEach((producto, i) => {
                const card = document.createElement("div");
                card.innerHTML = `
                    <img src="${producto.urlImagen}" alt="${producto.nombre}">
                    <div class="informacion">
                        <p>${producto.nombre}</p>
                        <p class="precio">$${producto.valor}</p>
                        ${producto.existencia > 0
                            ? `<button data-id="${producto.id}">Comprar</button>`
                            : `<p class="soldOut">Sold Out</p>`
                        }
                    </div>
                `;
                contenedor.appendChild(card);
            });

            // Agregar eventos a botones de comprar
            contenedor.querySelectorAll("button[data-id]").forEach(btn => {
                btn.addEventListener("click", () => {
                    const producto_id = parseInt(btn.dataset.id);
                    agregarAlCarrito(usuario.id, producto_id);
                });
            });
        });

    function agregarAlCarrito(usuario_id, producto_id) {
        fetch(`${API}/api/carrito`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                usuario_id,
                producto_id,
                cantidad: 1
            })
        })
        .then(res => res.json())
        .then(() => {
            alert("Producto agregado al carrito");
            actualizarCarrito(usuario_id);
        })
        .catch(err => console.error("Error al agregar producto:", err));
    }

    function actualizarCarrito(usuario_id) {
        fetch(`${API}/api/carrito/${usuario_id}`)
            .then(res => res.json())
            .then(lista => {
                numero.textContent = lista.length;
                numero.classList.add("diseñoNumero");
            });
    }

    // Inicializar el contador
    actualizarCarrito(usuario.id);
});