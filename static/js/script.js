// // Actions:

// const closeButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>remove</title>
// <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
// </svg>
// `;
// const menuButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>ellipsis-horizontal</title>
// <path d="M16 7.843c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 1.98c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 19.908c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 14.046c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 31.974c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 26.111c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// </svg>
// `;

// const actionButtons = document.querySelectorAll('.action-button');

// if (actionButtons) {
//   actionButtons.forEach(button => {
//     button.addEventListener('click', () => {
//       const buttonId = button.dataset.id;
//       let popup = document.querySelector(`.popup-${buttonId}`);
//       console.log(popup);
//       if (popup) {
//         button.innerHTML = menuButton;
//         return popup.remove();
//       }

//       const deleteUrl = button.dataset.deleteUrl;
//       const editUrl = button.dataset.editUrl;
//       button.innerHTML = closeButton;

//       popup = document.createElement('div');
//       popup.classList.add('popup');
//       popup.classList.add(`popup-${buttonId}`);
//       popup.innerHTML = `<a href="${editUrl}">Edit</a>
//       <form action="${deleteUrl}" method="delete">
//         <button type="submit">Delete</button>
//       </form>`;
//       button.insertAdjacentElement('afterend', popup);
//     });
//   });
// }

// Menu

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;


////////////////////////////    NOTIFICATIONS    ////////////////////////////

function closeNotification(closeButton) {
  const notification = closeButton.closest('.notification');

  if (notification) {
    // Add a CSS class for the fade-out effect
    notification.classList.add('fade-out');

    // Wait for the animation to finish before removing the element
    notification.addEventListener('animationend', () => {
      notification.remove();
    });
  }
}





///////////////////////////////////     TOPICS LOADING        /////////////////////////////////
document.addEventListener('DOMContentLoaded', function() {
  const loadMoreBtn = document.getElementById('load-more');
  let currentPage = 1;  // Start at page 1

  loadMoreBtn.addEventListener('click', function() {
      // Increment the page number
      currentPage++;

      // Get the current search query
      const searchQuery = document.querySelector('input[name="q"]').value;

      // Make the AJAX request
      fetch(`/topics/?q=${searchQuery}&page=${currentPage}`, {
          method: 'GET',
          headers: {
              'X-Requested-With': 'XMLHttpRequest'
          }
      })
      .then(response => response.json())
      .then(data => {
          // If there are more topics, append them to the list
          if (data.topics.length > 0) {
              const topicsList = document.querySelector('.topics__list');
              data.topics.forEach(topic => {
                  const li = document.createElement('li');
                  li.innerHTML = `<a href="/home?q=${topic.name}">${topic.name} <span>${topic.count}</span></a>`;
                  topicsList.appendChild(li);
              });

              // If there are no more topics, hide the "Load More" button
              if (!data.has_next) {
                  loadMoreBtn.style.display = 'none';
              }
          }
      })
      .catch(error => console.log(error));
  });
});



//////////////////////////    ADD BOOKMARKS   ////////////////////////////
function toggleBookmark(roomId) {
  // Get the checkbox input element and the SVG element for the bookmark icon
  var checkbox = document.getElementById('bookmark-toggle-' + roomId);
  var bookmarkIcon = document.querySelector(`#bookmark-toggle-${roomId} + div .bookmark-icon`);
  
  // Send AJAX request to add/remove the bookmark
  fetch(`/add-bookmark/${roomId}/`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')  // CSRF token for security
      },
      body: JSON.stringify({
          bookmarked: checkbox.checked // Send whether the checkbox is checked
      })
  })
  .then(response => response.json())
  .then(data => {
      // Optionally handle the response, e.g. update UI or show a message
      alert(data.message);  // Example of showing the response message
      checkbox.checked = data.bookmarked;  // Update the checkbox based on the response

      // Toggle the 'bookmarked' class on the icon based on the response
      if (data.bookmarked) {
          bookmarkIcon.classList.add('bookmarked');
      } else {
          bookmarkIcon.classList.remove('bookmarked');
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

// Helper function to get CSRF token from cookies (needed for POST requests in Django)
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

//*=////////////////////////  Message sending     ////////////////////////////
document.addEventListener('DOMContentLoaded', () => {
  const messageInput = document.getElementById('messageInput');
  const sendButton = document.getElementById('sendButton');

  messageInput.addEventListener('input', () => {
    if (messageInput.value.trim() === '') {
      sendButton.disabled = true; // Disable the button if input is empty
    } else {
      sendButton.disabled = false; // Enable the button if input has content
    }
  });
});


//*=//////////////////    THeme CHANGE FROM BUTTON ///////////////////////  
// document.querySelectorAll('.colorPallete button').forEach(button => {
//   button.addEventListener('click', () => {
//     // Get the background color of the child div
//     const color = button.querySelector('.colorPallete__item').style.backgroundColor;

//     // Apply the color to the theme
//     document.body.style.backgroundColor = color;
//     document.body.classList.add('theme'); // Optional: Add theme class for styling
//   });
// });

document.addEventListener('DOMContentLoaded', () => {
  const backgrounds = [
    'url("/static/images/1.jpg")',
    'url("/static/images/2.jpg")',
    'url("/static/images/3.jpg")',
    'url("/static/images/4.jpg")',
    'url("/static/images/5.jpg")',
    'url("/static/images/6.jpg")',
  ];
  

  document.querySelectorAll('.colorPallete button').forEach((button, index) => {
    button.addEventListener('click', () => {
      console.log(`Button ${index + 1} clicked`);

      const body = document.body;

      // Remove existing styles
      // body.style.backgroundColor = '';
      body.style.backgroundImage = '';

      // Apply new background
      const background = backgrounds[index];
      console.log(`Applying background: ${background}`);
      body.style.backgroundImage = background;
      body.style.backgroundSize = 'cover';
      body.style.backgroundPosition = 'center';
    });
  });
});





////////////////////// ?Light and dark mode  //////////////////
// Select the toggle button and body element
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Check localStorage for saved theme preference
if (localStorage.getItem('theme') === 'dark') {
  body.classList.add('dark-theme');
  themeToggle.checked = true;
}

// Add event listener to toggle button
themeToggle.addEventListener('change', () => {
  if (themeToggle.checked) {
    body.classList.add('dark-theme');
    localStorage.setItem('theme', 'dark');
  } else {
    body.classList.remove('dark-theme');
    localStorage.setItem('theme', 'light');
  }
});



////////////////////// ?SENDING MESSAGE //////////////////
function sendMessage(event) {
  event.preventDefault();  // Prevent form submission

  // Get the send button and add the 'loading' class to show the spinner
  const sendButton = document.querySelector('.send-button');
  sendButton.classList.add('loading');

  // Simulate message sending process
  setTimeout(function() {
    sendButton.classList.remove('loading'); // Remove the loading spinner
    document.querySelector('.room__message form').submit(); // Submit the form after the animation
  }, 2000); // Simulate a 2-second sending delay (adjust as needed)
}

// Check if Enter is pressed
function checkEnter(event) {
  if (event.key === 'Enter') {
    sendMessage(event);
  }
}

// Add event listener to the send button for regular click
document.querySelector('.send-button').addEventListener('click', sendMessage);

// Add event listener to the input field to handle 'Enter' key press
document.querySelector('.message-input').addEventListener('keydown', checkEnter);




//@@//////////////////////    FAQ    ////////////////////////
function toggleAnswer(index) {
  const answer = document.getElementById(`answer-${index}`);
  const sign = document.querySelectorAll(".toggle-sign")[index];

  if (answer.classList.contains("show")) {
      answer.classList.remove("show");
      sign.textContent = "+";
  } else {
      answer.classList.add("show");
      sign.textContent = "-";
  }
}





