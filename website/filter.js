// filter.js
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const products = document.querySelectorAll('.product-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            button.classList.add('active');
            
            // Get selected category
            const selectedCategory = button.getAttribute('data-category');
            
            // Filter products
            filterProducts(selectedCategory);
        });
    });

    function filterProducts(category) {
        products.forEach(product => {
            const productCategory = product.getAttribute('data-category');
            
            if (category === 'all' || category === productCategory) {
                product.classList.remove('hidden');
            } else {
                product.classList.add('hidden');
            }
        });
    }
});