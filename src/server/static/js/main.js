'use strict mode'

let static = document.getElementById('checkStatic');
let staticSettings = document.getElementById('staticSettings')
static.addEventListener('change', function() {
    if (static.checked == false) {
        staticSettings.setAttribute('style', 'display:none')
    } else {
        staticSettings.removeAttribute('style');
    }
});

let nightmode = document.getElementById('checkNightmode');
let nightmodeSettings = document.getElementById('nightmodeSettings')
nightmode.addEventListener('change', function() {
    if (nightmode.checked == false) {
        nightmodeSettings.setAttribute('style', 'display:none')
    } else {
        nightmodeSettings.removeAttribute('style');
    }
});

let output = document.getElementById('output');
var xhr = new XMLHttpRequest();
xhr.open('GET', 'http://localhost:5000/stream');
xhr.send();

setInterval(function() {
    output.textContent = xhr.responseText;
}, 1000);

let expert = document.getElementById('expert')
let expertTrigger = document.getElementById('showExpert');
expertTrigger.addEventListener('change', e => {
    if (expertTrigger.checked == true) {
        expert.style.removeProperty('display');
    } else {
        expert.style.setProperty('display','none')
    }
});

