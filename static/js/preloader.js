// -----------------------------------------------------  PRELOADER 
var loader = document.getElementsByClassName('preloader')[0];

    window.addEventListener('load', function() {
        setTimeout(function() {
            loader.classList.add('hidden');  
        }, 500); // Delay time
    });

