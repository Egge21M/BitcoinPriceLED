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