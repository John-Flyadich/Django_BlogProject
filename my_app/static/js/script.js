// Canvas script
let camera
let scene
let renderer
let material
let mouseX = 0
let mouseY = 0
let windowHalfX = window.innerWidth / 2
let windowHalfY = window.innerHeight / 2

init()
animate()

function init() {
  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 5, 2000)
  camera.position.z = 500

  scene = new THREE.Scene()
  scene.fog = new THREE.FogExp2(0x0000ff, 0.001)

  const geometry = new THREE.BufferGeometry()
  const vertices = []
  const size = 2000

  for (let i = 0; i < 20000; i++) {
    const x = (Math.random() * size + Math.random() * size) / 2 - size / 2
    const y = (Math.random() * size + Math.random() * size) / 2 - size / 2
    const z = (Math.random() * size + Math.random() * size) / 2 - size / 2

    vertices.push(x, y, z)
  }

  geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3))

  material = new THREE.PointsMaterial({
    size: 2,
    color: 0xffffff,
  })

  const particles = new THREE.Points(geometry, material)
  scene.add(particles)

  renderer = new THREE.WebGLRenderer()
  renderer.setPixelRatio(window.devicePixelRatio)
  renderer.setSize(window.innerWidth, window.innerHeight)
  document.body.appendChild(renderer.domElement)

  document.body.style.touchAction = 'none'
  document.body.addEventListener('pointermove', onPointerMove)
  window.addEventListener('resize', onWindowResize)
}

function onWindowResize() {
  windowHalfX = window.innerWidth / 2
  windowHalfY = window.innerHeight / 2

  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}

function onPointerMove(event) {
  mouseX = event.clientX - windowHalfX
  mouseY = event.clientY - windowHalfY
}

function animate() {
  requestAnimationFrame(animate)
  render()
}

function render() {
  camera.position.x += (mouseX * 2 - camera.position.x) * 0.02
  camera.position.y += (-mouseY * 2 - camera.position.y) * 0.02
  camera.lookAt(scene.position)
  renderer.render(scene, camera)
  scene.rotation.x += 0.001
  scene.rotation.y += 0.002
}




// Изменение цвета заголовка при прокрутке
$(document).ready(function () {
  $(window).scroll(function () {
    var scrollTop = $(this).scrollTop();

    if (scrollTop > 1000) {
      $('header').addClass('scrolled');
    }
    if (scrollTop === 0) {
      $('header').removeClass('scrolled');
    }
  });
});


// Скрытие заголовка при прокрутке
var prevScrollPos = $(window).scrollTop();
var header = $("header"); // Замените "header" на селектор своего заголовка
var scrollThreshold = 100; // Пороговое значение прокрутки вниз для скрытия заголовка

$(window).scroll(function () {
  var currentScrollPos = $(window).scrollTop();

  if (prevScrollPos > currentScrollPos) {
    header.css("top", "0"); // Показать заголовок при прокрутке вверх
  } else {
    // Скрыть заголовок только при прокрутке на указанное количество пикселей
    if (currentScrollPos > scrollThreshold) {
      header.css("top", "-100px"); // Скрыть заголовок
    }
  }

  prevScrollPos = currentScrollPos;
});



// попап кнопка
$(document).ready(function() {
  $("#showPopupButton").click(function() {
    $("#popup").fadeIn();
    $("#overlay").fadeIn();
    $("body").css("overflow", "hidden");
  });

  $("#closePopupButton").click(function() {
    $("#popup").fadeOut();
    $("#overlay").fadeOut();
    $("body").css("overflow", "auto");
  });
});

























