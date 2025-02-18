// carousel.js
document.addEventListener('DOMContentLoaded', function() {
    let currentSlide = 0;
    const slides = document.querySelectorAll('.carousel-item');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');

    function updateSlide() {
        const carousel = document.querySelector('.carousel-inner');
        carousel.style.transform = `translateX(-${currentSlide * 100}%)`;
    }

    if (prevButton && nextButton) {
        prevButton.addEventListener('click', () => {
            currentSlide = Math.max(currentSlide - 1, 0);
            updateSlide();
        });

        nextButton.addEventListener('click', () => {
            currentSlide = Math.min(currentSlide + 1, slides.length - 1);
            updateSlide();
        });
    }

    // Optional: Auto-sliding functionality
    function autoSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        updateSlide();
    }

    // Uncomment to enable auto-sliding
    // setInterval(autoSlide, 5000); // Changes slide every 5 seconds
});