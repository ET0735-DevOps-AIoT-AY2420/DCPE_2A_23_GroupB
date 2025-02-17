// cart.js
document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productCard = button.closest('.product-card');
            const productData = {
                id: productCard.getAttribute('data-product-id'),
                name: productCard.querySelector('h3').textContent,
                price: productCard.querySelector('.product-price').textContent,
                quantity: 1
            };
            
            addToCart(productData);
            updateCartUI();
        });
    });

    function addToCart(product) {
        let cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const existingProduct = cart.find(item => item.id === product.id);
        
        if (existingProduct) {
            existingProduct.quantity += 1;
        } else {
            cart.push(product);
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    function updateCartUI() {
        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const cartCount = cart.reduce((total, item) => total + item.quantity, 0);
        
        // Update cart counter in the UI
        const cartCounter = document.querySelector('.cart-counter');
        if (cartCounter) {
            cartCounter.textContent = cartCount;
        }
    }
});