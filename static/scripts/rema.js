function speakResponse(responseText) {
    var speech = new SpeechSynthesisUtterance(responseText);
    window.speechSynthesis.speak(speech);
}

function InAudio(audio, delay) {
    setTimeout(function() {
        audio.volume = 1.0
        audio.play();
    }, delay)
}

window.onload = function() {
    var outputElement = document.getElementById("output");
    if (outputElement) {
        speakResponse(outputElement.innerText);
        
    }
};