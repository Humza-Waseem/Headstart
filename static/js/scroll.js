// -----------------------------------------------    SCROLL TO TOP BUTTON
// Get the button element
const scrollToTopButton = document.getElementById('scrollToTop');

// Show or hide the button on scroll
window.addEventListener('scroll', () => {
    // Check if the user has scrolled down more than 150vh
    if (window.scrollY > window.innerHeight * 1.5) {
        scrollToTopButton.style.display = 'flex'; // Show the button
    } else {
        scrollToTopButton.style.display = 'none'; // Hide the button
    }
});

// Smoothly scroll to the top when the button is clicked
scrollToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0, // Scroll to the very top of the page
        behavior: 'smooth', // Smooth scrolling
    });
});
