// Get the elements
const intro = document.querySelector('.intro');
const introImage = document.querySelector('.intro-image');
const introText = document.querySelector('.intro-text');

function switchToMainPage() {
 console.log('Nevigating to \'http://lix.pythonanywhere.com/rema\'');
  setTimeout(() => {
    window.location.href = 'http://lix.pythonanywhere.com/rema';
  }, 5000); 
};

// Event listener for when intro animation ends
intro.addEventListener('animationend', () => {
  // After the intro animation ends, trigger the switch to the main page
  switchToMainPage();
});
