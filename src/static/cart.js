document.addEventListener("DOMContentLoaded", function () {
    loadCart();
});

function loadCart() {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let cartList = document.getElementById("cart-items");

    if (!cartList) return;

    cartList.innerHTML = "";
    cart.forEach((item, index) => {
        let listItem = document.createElement("li");
        listItem.innerHTML = `
            <strong>${item.name}</strong> - $${item.price}
            <button onclick="removeFromCart(${index})">Remove</button>
        `;
        cartList.appendChild(listItem);
    });
}

function removeFromCart(index) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart.splice(index, 1); 
    localStorage.setItem("cart", JSON.stringify(cart));
    loadCart();
}
