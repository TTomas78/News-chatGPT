
const getNewsButton = document.getElementById("getNews");
getNewsButton.addEventListener("click", getNews);
const configurationButton = document.getElementById("configImage");
configurationButton.addEventListener("click", DisplayConfigMenu);
const getOneNewsButton = document.getElementById("getOneNews");
getOneNewsButton.addEventListener("click", DisplayGetOneNewsMenu);
const getOneNewsButtonConfirmed = document.getElementById('getOneNewsConfirmed')
getOneNewsButtonConfirmed.addEventListener("click",function(event) {
  event.preventDefault();
  getOneNews();
});


function getNews(){
//data validation:
wordsNumber = document.getElementById('wordsNumber')
language = document.getElementById('language')
softLimit = document.getElementById('softLimit')
if (softLimit.checked) {
  softLimit.value = true;
} else {
  softLimit.value = false;
}
if (wordsNumber.value == "" || language.value == "" || softLimit.value == ""){
  alert("Complete los campos del menu configuracion")
  return
}

var spinner = document.querySelector('.contenedor-spinner');
spinner.style.display = 'flex';
chrome.runtime.sendMessage({name: "getAll",wordsNumber: wordsNumber.value, language: language.value, softLimit: softLimit.value},(data) => {
   spinner.style.display = 'none';

  // Actualizar la UI del popup con los datos recibidos de background.js
  // Obtener la lista en la que mostraremos los datos
    const myList = document.getElementById("NewsList");

    // Vaciar la lista por si tenía elementos previos
    myList.innerHTML = "";

      data.news.forEach(function(data) {
        myList.appendChild(generateHTMLElements(data))
        });
        //hacer que se abra en una nueva pestaña
     

})};

function getOneNews(){
  //data validation:
  wordsNumber = document.getElementById('wordsNumber')
  language = document.getElementById('language')
  softLimit = document.getElementById('softLimit')
  link = document.getElementById('newsLink')
  if (softLimit.checked) {
    softLimit.value = true;
  } else {
    softLimit.value = false;
  }
  if (wordsNumber.value == "" || language.value == "" || softLimit.value == ""|| newsLink.value == ""){
    alert("Complete los campos del menu configuracion y el link de la noticia")
    return
  }
  
  var spinner = document.querySelector('.contenedor-spinner');
  spinner.style.display = 'flex';
  chrome.runtime.sendMessage({name: "getOne",wordsNumber: wordsNumber.value, language: language.value, softLimit: softLimit.value, link: newsLink.value},(data) => {
  spinner.style.display = 'none';
// Actualizar la UI del popup con los datos recibidos de background.js
// Obtener la lista en la que mostraremos los datos
  const myList = document.getElementById("NewsList");

  // Vaciar la lista por si tenía elementos previos
  myList.innerHTML = "";
  if (data.error != undefined){
    alert(data.error)
  } else {
    myList.appendChild(generateHTMLElements(data))
  }
    DisplayGetOneNewsMenu();
  }
  )};

function generateHTMLElements(data){
  console.log(data.title)
  const title = document.createElement("h3");
  title.textContent = data.title;
  const text = document.createElement("p");
  text.textContent = data.summary;
  const link = document.createElement("a");
  link.href = data.link;
  link.className = "newsURL";
  link.textContent = "Leer mas";
  const parent = document.createElement("div");
  const hr = document.createElement("hr");
  parent.appendChild(title);
  parent.appendChild(text);
  parent.appendChild(link);
  parent.appendChild(hr);
  //hacer que se abra en una nueva pestaña
  link.addEventListener('click', function(event) {
    event.preventDefault(); // Evita la acción por defecto del enlace
    window.open(data.link, '_blank'); // Abre el enlace en una ventana externa
  })
  return parent
};

function DisplayConfigMenu() {
  var menu = document.getElementById("menu-config");
  if (menu.style.display === "none") {
    menu.style.display = "block";
  } else {
    menu.style.display = "none";
  }
}
function DisplayGetOneNewsMenu() {
  var menu = document.getElementById("news-link");
  if (menu.style.display === "none") {
    menu.style.display = "block";
  } else {
    menu.style.display = "none";
  }
}