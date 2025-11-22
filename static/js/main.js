// Theme Management
function changeTheme(themeName) {
  document.body.className = `theme-${themeName}`;
  localStorage.setItem("selectedTheme", themeName);
}

// Load saved theme
document.addEventListener("DOMContentLoaded", function () {
  const savedTheme = localStorage.getItem("selectedTheme") || "rose";
  changeTheme(savedTheme);
});

// Music Management
let isMusicPlaying = false;
const bgMusic = document.getElementById("bgMusic");
const musicToggle = document.getElementById("musicToggle");

function toggleMusic() {
  if (!isMusicPlaying) {
    bgMusic
      .play()
      .then(() => {
        isMusicPlaying = true;
        musicToggle.textContent = "🎵 Music On";
      })
      .catch((error) => {
        console.log("Audio play failed:", error);
        alert("Please interact with the page first to enable music");
      });
  } else {
    bgMusic.pause();
    isMusicPlaying = false;
    musicToggle.textContent = "🎵 Music Off";
  }
}

// Initialize music with user interaction
document.addEventListener("click", function initMusic() {
  if (!bgMusic.played) {
    musicToggle.textContent = "🎵 Music Off";
  }
  document.removeEventListener("click", initMusic);
});

// Rose Petals Density
let petalDensity = 15;

function createRosePetals() {
  const container = document.getElementById("rosePetals");
  if (!container) return;

  container.innerHTML = "";

  for (let i = 0; i < petalDensity; i++) {
    const petal = document.createElement("div");
    petal.className = "rose-petal";

    // Random properties
    const size = Math.random() * 15 + 10;
    const left = Math.random() * 100;
    const animationDuration = Math.random() * 10 + 10;
    const animationDelay = Math.random() * 5;
    const color = `hsl(${Math.random() * 20 + 330}, 70%, 60%)`;

    petal.style.width = `${size}px`;
    petal.style.height = `${size}px`;
    petal.style.left = `${left}vw`;
    petal.style.animationDuration = `${animationDuration}s`;
    petal.style.animationDelay = `${animationDelay}s`;
    petal.style.background = color;

    container.appendChild(petal);
  }
}

function makeItRainRoses() {
  petalDensity = Math.min(petalDensity + 10, 50);
  createRosePetals();
}

// Floating Compliments
const compliments = [
  "Aap bohot pyaari hain 💖",
  "Aapki smile sabse khoobsurat hai 😊",
  "Aap meri jaan hain 🌹",
  "Aapse hi mera har din behtar hota hai ✨",
  "Aapki aankhon mein sara pyaar hai 👀",
  "Aap mere sapnon ki rani hain 👑",
  "Aapki har ada dil chura leti hai 💕",
  "Aap bin meri duniya adhuri hai 🌍",
];

function createFloatingCompliments() {
  const container = document.getElementById("floatingCompliments");
  if (!container) return;

  setInterval(() => {
    if (Math.random() < 0.3) {
      // 30% chance to create new compliment
      const compliment = document.createElement("div");
      compliment.className = "floating-compliment";
      compliment.textContent =
        compliments[Math.floor(Math.random() * compliments.length)];

      // Random starting position
      compliment.style.left = `${Math.random() * 80 + 10}vw`;
      compliment.style.top = `-50px`;

      // Random animation
      const duration = Math.random() * 10 + 10;
      compliment.style.animationDuration = `${duration}s`;

      container.appendChild(compliment);

      // Remove after animation completes
      setTimeout(() => {
        compliment.remove();
      }, duration * 1000);
    }
  }, 2000);
}

// Initialize animations
document.addEventListener("DOMContentLoaded", function () {
  createRosePetals();
  createFloatingCompliments();

  // Add rose rain button if not on unlock screen
  if (!document.querySelector(".unlock-screen")) {
    const roseButton = document.createElement("button");
    roseButton.textContent = "🌹 Make it Rain Roses";
    roseButton.style.position = "fixed";
    roseButton.style.bottom = "60px";
    roseButton.style.left = "50%";
    roseButton.style.transform = "translateX(-50%)";
    roseButton.style.zIndex = "1000";
    roseButton.style.background = "var(--primary-color)";
    roseButton.style.color = "white";
    roseButton.style.border = "none";
    roseButton.style.padding = "0.5rem 1rem";
    roseButton.style.borderRadius = "20px";
    roseButton.style.cursor = "pointer";
    roseButton.onclick = makeItRainRoses;

    document.body.appendChild(roseButton);
  }
});
