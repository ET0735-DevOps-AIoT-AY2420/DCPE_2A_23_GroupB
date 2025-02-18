// favorites.js
document.addEventListener('DOMContentLoaded', function() {
    const favoriteButtons = document.querySelectorAll('.favorite-button');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const icon = button.querySelector('i');
            icon.classList.toggle('fas');
            icon.classList.toggle('far');
            
            // Optional: Save favorite status
            const productCard = button.closest('.product-card');
            const productId = productCard.getAttribute('data-product-id');
            toggleFavoriteStatus(productId);
        });
    });

    // Function to save favorite status (you can implement localStorage or API calls here)
    function toggleFavoriteStatus(productId) {
        // Example using localStorage
        const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        const index = favorites.indexOf(productId);
        
        if (index === -1) {
            favorites.push(productId);
        } else {
            favorites.splice(index, 1);
        }
        
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }
});