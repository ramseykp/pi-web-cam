'use strict'
// const path = require('path');

const webcamFolder = '/var/www/html/web-cam/';
const imagesFolder = [webcamFolder, 'images/'].join();
const mainDiv = document.getElementById('main-div')

let para1 = document.createElement('p');
para1.id = 'top-paragraph'
para1.innerHTML =
    'Welcome to the Oslo Web Cam. May she fill your screen with joy.';
mainDiv.appendChild(para1);

let currentImage = document.createElement('img');
currentImage.id = 'img'
currentImage.setAttribute('src', 'images/recent_image.jpg');
currentImage.className = 'center-fit';
mainDiv.appendChild(currentImage);


window.onload = function() {
  var image = document.getElementById('img');

  function updateImage() {
    image.src = image.src.split('?')[0] + '?' + new Date().getTime();
  }

  setInterval(updateImage, 60000);
}