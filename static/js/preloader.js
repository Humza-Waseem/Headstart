// -----------------------------------------------------  PRELOADER 
var loader = document.getElementsByClassName('preloader')[0];

    window.addEventListener('load', function() {
        setTimeout(function() {
            loader.classList.add('hidden');  
        }, 1000); // Delay for 3 seconds
    });

