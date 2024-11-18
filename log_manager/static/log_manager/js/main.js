//Automatically hide a message alert after 5seconds
document.addEventListener('DOMContentLoaded', (event) => {
  setTimeout(() => {
    const alert = document.querySelector('.sys-feedback');
    if (alert) {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }
  }, 7000);
});



let openMenu = document.querySelector('.menu');
let closeMenuElements = document.querySelectorAll('.close-nav');
let sidebar = document.querySelector('.sidebar');
let main = document.querySelector('.main');


// Function to toggle the action menu
function toggleActionsMenu(event) {
  event.stopPropagation(); // Prevents the menu from closing when clicking inside
  const clickedIcon = event.target;

  // Close any other open menus
  document.querySelectorAll('.action-menu-content').forEach(menu => {
    if (menu !== clickedIcon.nextElementSibling) {
      menu.parentElement.classList.remove('show');
    }
  });

  // Toggle the visibility of the clicked menu
  clickedIcon.parentElement.classList.toggle('show');
}

// Add event listeners to each menu icon for toggling
document.querySelectorAll('.action-menu-icon').forEach(menuIcon => {
  menuIcon.addEventListener('click', toggleActionsMenu);
});

// Close the menu when clicking outside of it
window.addEventListener('click', (event) => {
  if (!event.target.closest('.action-menu-icon')) {
    document.querySelectorAll('.action-menu').forEach(menu => {
      menu.classList.remove('show');
    });
  }
});


// Function to check the screen size and show/hide sidebar
function checkScreenSize() {
  const isDesktop = window.matchMedia('(min-width: 1200px)').matches;
  if (isDesktop) {
    sidebar.style.transform = 'translateX(0)'; // Show sidebar on desktop
    main.style.marginLeft = '0'; // Reset main content position
    main.style.opacity = '1'; // Reset opacity
  } else {
    sidebar.style.transform = 'translateX(-100%)'; // Hide sidebar on mobile
  }
}

// Initial check
checkScreenSize();

// Event listeners for opening and closing the sidebar
openMenu.addEventListener('click', function () {
  if (window.innerWidth <= 1200) {
    sidebar.style.transform = 'translateX(0)'; // Slide the sidebar into view
    main.style.marginLeft = '50px'; // Shift the main content to the right
    main.style.opacity = '0.5'; // Fade the main content
  }
});

closeMenuElements.forEach(function (closeMenu) {
  closeMenu.addEventListener('click', function () {
    if (window.innerWidth <= 1200) { // Check if the device is mobile (width <= 1200px)
      sidebar.style.transform = 'translateX(-100%)'; // Slide the sidebar out of view
      main.style.marginLeft = '0'; // Reset the main content position
      main.style.opacity = '1'; // Fade the main content
    }
  });
});

// Add resize event listener
window.addEventListener('resize', checkScreenSize);


// Get the button:
let scrollTopButton = document.getElementById("scroll-top");

// When the user scrolls down 200px from the top of the document, show the button
window.onscroll = function () { scrollFunction() };

function scrollFunction() {
  if (document.body.scrollTop > 400 || document.documentElement.scrollTop > 400) {
    scrollTopButton.style.display = "block";
  } else {
    scrollTopButton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}


// Get all animation info items
const animationItems = document.querySelectorAll('.scroll-animation ');

// Function to check if an element is in the viewport
function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}


// Function to handle scroll event and add animation class
function handleScroll() {
  animationItems.forEach(item => {
    if (isInViewport(item)) {
      item.classList.add('animated');
    } else {
      item.classList.remove('animated');
    }
  });
}

// Listen for scroll events
window.addEventListener('scroll', handleScroll);

// Initial check in case elements are already in viewport on page load
handleScroll();


// Open Record modal
document.querySelectorAll('.open-modal').forEach(button => {
  button.addEventListener('click', function () {
    const recordId = this.getAttribute('data-record-id');
    document.getElementById(`recordModal-${recordId}`).style.display = 'flex';
  });
});

// Close modal when clicking the close button
document.querySelectorAll('.close-modal').forEach(button => {
  button.addEventListener('click', function () {
    const recordId = this.getAttribute('data-record-id');
    document.getElementById(`recordModal-${recordId}`).style.display = 'none';
  });
});

// Close modal when clicking outside of it
window.addEventListener('click', function (event) {
  if (event.target.classList.contains('modal')) {
    event.target.style.display = 'none';
  }
});







