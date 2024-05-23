// Get the elements
const intro = document.querySelector('.intro');
const introImage = document.querySelector('.intro-image');
const introText = document.querySelector('.intro-text');

function switchToMainPage() {
 console.log('Nevigating to \'http://127.0.0.1:5000/rema\'');
  setTimeout(() => {
    window.location.href = 'http://127.0.0.1:5000/rema';
  }, 5000); 
};

// Event listener for when intro animation ends
intro.addEventListener('animationend', () => {
  // After the intro animation ends, trigger the switch to the main page
  switchToMainPage();
});