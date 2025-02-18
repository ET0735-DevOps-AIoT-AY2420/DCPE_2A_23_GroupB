// filter.js
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const subcategoryButtons = document.querySelectorAll('.subcategory-btn');
    const subcategoryGroups = document.querySelectorAll('.subcategory-group');
    const products = document.querySelectorAll('.product-card');
    const categoryLinks = document.querySelectorAll('.category-list a');

    let currentCategory = 'all';
    let currentSubcategory = null;

    // Main category filter buttons
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Update active states
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Get selected category
            currentCategory = button.getAttribute('data-category');
            currentSubcategory = null; // Reset subcategory when main category changes
            
            // Show/hide subcategories
            subcategoryGroups.forEach(group => {
                if (currentCategory === 'all') {
                    group.style.display = 'none';
                } else if (group.getAttribute('data-parent') === currentCategory) {
                    group.style.display = 'flex';
                } else {
                    group.style.display = 'none';
                }
            });

            // Reset subcategory active states
            subcategoryButtons.forEach(btn => btn.classList.remove('active'));
            
            // Filter products
            filterProducts();
        });
    });

    // Dropdown category links
    categoryLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Get selected category
            currentCategory = link.getAttribute('data-category');
            currentSubcategory = null;

            // Update filter button states
            filterButtons.forEach(btn => {
                if (btn.getAttribute('data-category') === currentCategory) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

            // Show/hide subcategories
            subcategoryGroups.forEach(group => {
                if (currentCategory === 'all') {
                    group.style.display = 'none';
                } else if (group.getAttribute('data-parent') === currentCategory) {
                    group.style.display = 'flex';
                } else {
                    group.style.display = 'none';
                }
            });

            // Reset subcategory active states
            subcategoryButtons.forEach(btn => btn.classList.remove('active'));
            
            // Filter products
            filterProducts();
        });
    });

    // Subcategory filter
    subcategoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Update active states
            subcategoryButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Get selected subcategory
            currentSubcategory = button.getAttribute('data-subcategory');
            
            // Filter products
            filterProducts();
        });
    });

    // Filter products function
    function filterProducts() {
        products.forEach(product => {
            const productCategory = product.getAttribute('data-category');
            const productSubcategory = product.getAttribute('data-subcategory');
            
            if (currentCategory === 'all') {
                product.style.display = 'block';
            } else if (currentSubcategory) {
                product.style.display = 
                    (productCategory === currentCategory && 
                     productSubcategory === currentSubcategory) ? 'block' : 'none';
            } else {
                product.style.display = 
                    (productCategory === currentCategory) ? 'block' : 'none';
            }
        });
    }

    // Initialize view
    filterProducts();
});