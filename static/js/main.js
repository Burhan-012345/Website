// Theme Management
let currentTheme = "rose";

function changeTheme(themeName) {
  document.body.className = `theme-${themeName}`;
  currentTheme = themeName;
  localStorage.setItem("selectedTheme", themeName);

  // Close theme menu if open
  const themeOptions = document.getElementById("themeOptions");
  if (themeOptions) {
    themeOptions.classList.remove("show");
  }

  // Update rose petals color based on theme
  updateRosePetalsColor(themeName);
}

function toggleThemeMenu() {
  const themeOptions = document.getElementById("themeOptions");
  if (themeOptions) {
    themeOptions.classList.toggle("show");
  }
}

// Close theme menu when clicking outside
document.addEventListener("click", function (event) {
  const themeOptions = document.getElementById("themeOptions");
  const themeBtn = document.querySelector(".theme-btn-floating");

  if (
    themeBtn &&
    themeOptions &&
    !themeBtn.contains(event.target) &&
    !themeOptions.contains(event.target)
  ) {
    themeOptions.classList.remove("show");
  }
});

// Load saved theme
document.addEventListener("DOMContentLoaded", function () {
  const savedTheme = localStorage.getItem("selectedTheme") || "rose";
  changeTheme(savedTheme);
});

// Music Management
let isMusicPlaying = false;
let bgMusic;

function initializeMusic() {
  bgMusic = document.getElementById("bgMusic");
  if (!bgMusic) {
    console.log("Background music element not found");
    return;
  }

  // Set initial volume
  bgMusic.volume = 0.3;

  // Update button states
  updateMusicButtons();
}

function toggleMusic() {
  if (!bgMusic) {
    initializeMusic();
  }

  if (!isMusicPlaying) {
    bgMusic
      .play()
      .then(() => {
        isMusicPlaying = true;
        updateMusicButtons();
        showNotification("Music started 🎵", "success");
      })
      .catch((error) => {
        console.log("Audio play failed:", error);
        showNotification("Please tap anywhere first to enable music", "info");
      });
  } else {
    bgMusic.pause();
    isMusicPlaying = false;
    updateMusicButtons();
    showNotification("Music paused 🔇", "info");
  }
}

function updateMusicButtons() {
  const musicToggle = document.getElementById("musicToggle");
  const musicToggleMenu = document.getElementById("musicToggleMenu");
  const musicText = document.getElementById("musicText");

  if (musicToggle) {
    musicToggle.innerHTML = isMusicPlaying
      ? '<i class="fas fa-volume-up"></i>'
      : '<i class="fas fa-volume-mute"></i>';
  }

  if (musicToggleMenu) {
    musicToggleMenu.innerHTML = isMusicPlaying
      ? '<i class="fas fa-volume-up"></i><span>Music On</span>'
      : '<i class="fas fa-volume-mute"></i><span>Music Off</span>';
  }

  if (musicText) {
    musicText.textContent = isMusicPlaying ? "Music On" : "Music Off";
  }
}

// Initialize music with user interaction
document.addEventListener("click", function initMusic() {
  initializeMusic();
  document.removeEventListener("click", initMusic);
});

// Rose Petals Management
let petalDensity = 15;

function createRosePetals() {
  const container = document.getElementById("rosePetals");
  if (!container) return;

  // Clear existing petals
  container.innerHTML = "";

  // Create new petals
  for (let i = 0; i < petalDensity; i++) {
    createSinglePetal(container, i);
  }
}

function createSinglePetal(container, index) {
  const petal = document.createElement("div");
  petal.className = "rose-petal";

  // Random properties
  const size = Math.random() * 15 + 10;
  const left = Math.random() * 100;
  const animationDuration = Math.random() * 10 + 10;
  const animationDelay = Math.random() * 5;

  petal.style.width = `${size}px`;
  petal.style.height = `${size}px`;
  petal.style.left = `${left}vw`;
  petal.style.animationDuration = `${animationDuration}s`;
  petal.style.animationDelay = `${animationDelay}s`;

  // Set color based on current theme
  updatePetalColor(petal);

  container.appendChild(petal);
}

function updatePetalColor(petal) {
  const colors = {
    rose: "hsl(330, 70%, 65%)",
    midnight: "hsl(280, 60%, 55%)",
    pink: "hsl(340, 80%, 70%)",
    gold: "hsl(45, 80%, 60%)",
  };

  petal.style.background = colors[currentTheme] || colors["rose"];
}

function updateRosePetalsColor(themeName) {
  const petals = document.querySelectorAll(".rose-petal");
  const colors = {
    rose: "hsl(330, 70%, 65%)",
    midnight: "hsl(280, 60%, 55%)",
    pink: "hsl(340, 80%, 70%)",
    gold: "hsl(45, 80%, 60%)",
  };

  petals.forEach((petal) => {
    petal.style.background = colors[themeName] || colors["rose"];
  });
}

function makeItRainRoses() {
  petalDensity = Math.min(petalDensity + 10, 50);
  createRosePetals();

  // Show notification
  showNotification("More roses coming your way! 🌹", "success");

  // Create celebration effect
  createHeartAnimation("50%", "50%", 8);
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
  "Aapki aawaz meri favorite dhun hai 🎵",
  "Aap mere liye sabse khaas ho 💫",
  "Aapki muskurahat meri duniya roshan karti hai 🌟",
  "Aapke bina har pal adhura lagta hai 💔",
  "Aap meri har khushi ka sabaab hain 🎉",
  "Aapki yaadon mein kho jaata hoon 🤗",
  "Aap mere liye duaon ka jawab hain 🙏",
];

function createFloatingCompliments() {
  const container = document.getElementById("floatingCompliments");
  if (!container) return;

  // Create compliments at intervals
  setInterval(() => {
    if (Math.random() < 0.3) {
      // 30% chance to create new compliment
      createFloatingCompliment(container);
    }
  }, 3000);
}

function createFloatingCompliment(container) {
  const compliment = document.createElement("div");
  compliment.className = "floating-compliment";
  compliment.textContent =
    compliments[Math.floor(Math.random() * compliments.length)];

  // Random starting position
  const startLeft = Math.random() * 80 + 10; // 10% to 90%
  compliment.style.left = `${startLeft}vw`;
  compliment.style.top = `-50px`;

  // Random animation duration
  const duration = Math.random() * 15 + 10; // 10 to 25 seconds
  compliment.style.animationDuration = `${duration}s`;

  // Random color based on theme
  const colors = {
    rose: ["#e91e63", "#f8bbd9", "#ad1457"],
    midnight: ["#9c27b0", "#7b1fa2", "#6a1b9a"],
    pink: ["#ec407a", "#f8bbd9", "#ad1457"],
    gold: ["#ff9800", "#ffb74d", "#f57c00"],
  };

  const themeColors = colors[currentTheme] || colors["rose"];
  compliment.style.background =
    themeColors[Math.floor(Math.random() * themeColors.length)];

  container.appendChild(compliment);

  // Remove after animation completes
  setTimeout(() => {
    if (compliment.parentNode) {
      compliment.parentNode.removeChild(compliment);
    }
  }, duration * 1000);
}

// Hamburger Menu Management
function initializeMenu() {
  // Close menu when clicking on menu items
  document.querySelectorAll(".menu-item").forEach((item) => {
    item.addEventListener("click", function () {
      document.getElementById("menu-toggle").checked = false;
    });
  });

  // Close menu when clicking on overlay (outside menu content)
  const menuOverlay = document.querySelector(".menu-overlay");
  if (menuOverlay) {
    menuOverlay.addEventListener("click", function (event) {
      if (event.target === this) {
        document.getElementById("menu-toggle").checked = false;
      }
    });
  }

  // Close menu with Escape key
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      document.getElementById("menu-toggle").checked = false;
    }
  });
}

// Lock/Logout functionality
function handleLock(event) {
  if (event) {
    event.preventDefault();
  }

  // Close hamburger menu first
  document.getElementById("menu-toggle").checked = false;

  // Show confirmation with romantic message
  showLockConfirmation();
}

function showLockConfirmation() {
  // Create a beautiful confirmation modal
  const modal = document.createElement("div");
  modal.className = "lock-confirmation-modal";
  modal.innerHTML = `
        <div class="lock-confirmation-content">
            <div class="lock-icon">🔒</div>
            <h3>Lock Website?</h3>
            <p>Kya aap sach mein website lock karna chahte hain?</p>
            <p class="romantic-message">Yeh meri duniya aapke liye hi hai, aap hamesha welcome hain! 💖</p>
            <div class="lock-buttons">
                <button class="lock-confirm-btn" onclick="proceedWithLock()">Haan, Lock Karo</button>
                <button class="lock-cancel-btn" onclick="closeLockConfirmation()">Nahi, Yahan Raho</button>
            </div>
        </div>
    `;

  document.body.appendChild(modal);

  // Add enter key support
  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      proceedWithLock();
    } else if (event.key === "Escape") {
      closeLockConfirmation();
    }
  };

  document.addEventListener("keydown", handleKeyPress);
  modal._keyHandler = handleKeyPress;
}

function proceedWithLock() {
  // Close confirmation modal
  closeLockConfirmation();

  // Show locking animation
  showLockingAnimation();

  // Redirect to unlock page after animation
  setTimeout(() => {
    window.location.href = "/logout";
  }, 2000);
}

function closeLockConfirmation() {
  const modal = document.querySelector(".lock-confirmation-modal");
  if (modal) {
    // Remove key event listener
    if (modal._keyHandler) {
      document.removeEventListener("keydown", modal._keyHandler);
    }
    modal.remove();
  }
}

function showLockingAnimation() {
  const animation = document.createElement("div");
  animation.className = "locking-animation";
  animation.innerHTML = `
        <div class="locking-content">
            <div class="locking-heart">💖</div>
            <div class="locking-text">Locking with love...</div>
            <div class="locking-subtext">Aapki yaadon ke saath 🔒</div>
        </div>
    `;

  document.body.appendChild(animation);
}

// Notification System
function showNotification(message, type = "info") {
  // Create notification element
  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;

  // Add to page
  document.body.appendChild(notification);

  // Show notification
  setTimeout(() => {
    notification.classList.add("show");
  }, 100);

  // Auto remove after 3 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.classList.remove("show");
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    }
  }, 3000);
}

// Add notification styles dynamically
function addNotificationStyles() {
  if (!document.querySelector("#notification-styles")) {
    const style = document.createElement("style");
    style.id = "notification-styles";
    style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--card-bg);
                color: var(--text-color);
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                border-left: 4px solid var(--primary-color);
                transform: translateX(400px);
                transition: transform 0.3s ease;
                z-index: 10000;
                max-width: 300px;
            }
            
            .notification.show {
                transform: translateX(0);
            }
            
            .notification-success {
                border-left-color: #4CAF50;
            }
            
            .notification-info {
                border-left-color: #2196F3;
            }
            
            .notification-warning {
                border-left-color: #FF9800;
            }
            
            .notification-error {
                border-left-color: #f44336;
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
            }
            
            .notification-message {
                flex: 1;
            }
            
            .notification-close {
                background: none;
                border: none;
                color: var(--text-color);
                font-size: 1.2rem;
                cursor: pointer;
                padding: 0;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .notification-close:hover {
                color: var(--primary-color);
            }
        `;
    document.head.appendChild(style);
  }
}

// Add lock confirmation styles
function addLockConfirmationStyles() {
  if (!document.querySelector("#lock-confirmation-styles")) {
    const style = document.createElement("style");
    style.id = "lock-confirmation-styles";
    style.textContent = `
            .lock-confirmation-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                backdrop-filter: blur(10px);
                animation: fadeIn 0.3s ease;
            }
            
            .lock-confirmation-content {
                background: var(--card-bg);
                padding: 2rem;
                border-radius: 20px;
                text-align: center;
                max-width: 400px;
                width: 90%;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                border: 2px solid var(--primary-color);
                animation: scaleIn 0.3s ease;
            }
            
            .lock-icon {
                font-size: 4rem;
                margin-bottom: 1rem;
                animation: pulse 2s infinite;
            }
            
            .lock-confirmation-content h3 {
                color: var(--primary-color);
                margin-bottom: 1rem;
                font-family: 'Dancing Script', cursive;
                font-size: 2rem;
            }
            
            .lock-confirmation-content p {
                color: var(--text-color);
                margin-bottom: 1rem;
                line-height: 1.5;
            }
            
            .romantic-message {
                font-style: italic;
                color: var(--accent-color);
                font-size: 0.9rem;
                margin-bottom: 1.5rem;
            }
            
            .lock-buttons {
                display: flex;
                gap: 1rem;
                margin-top: 1.5rem;
                justify-content: center;
            }
            
            .lock-confirm-btn, .lock-cancel-btn {
                padding: 0.8rem 1.5rem;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1rem;
                transition: all 0.3s ease;
                font-weight: 500;
            }
            
            .lock-confirm-btn {
                background: var(--primary-color);
                color: white;
            }
            
            .lock-confirm-btn:hover {
                background: var(--accent-color);
                transform: scale(1.05);
            }
            
            .lock-cancel-btn {
                background: rgba(255,255,255,0.1);
                color: var(--text-color);
                border: 1px solid rgba(255,255,255,0.2);
            }
            
            .lock-cancel-btn:hover {
                background: rgba(255,255,255,0.2);
                transform: scale(1.05);
            }
            
            .locking-animation {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.9);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                backdrop-filter: blur(10px);
            }
            
            .locking-content {
                text-align: center;
                color: white;
            }
            
            .locking-heart {
                font-size: 4rem;
                animation: heartbeat 1s ease-in-out infinite;
                margin-bottom: 1rem;
            }
            
            .locking-text {
                font-family: 'Dancing Script', cursive;
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }
            
            .locking-subtext {
                font-size: 1rem;
                opacity: 0.8;
            }
            
            @keyframes heartbeat {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.2); }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes scaleIn {
                from { transform: scale(0.8); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }
        `;
    document.head.appendChild(style);
  }
}

// Heart Animation Creator
function createHeartAnimation(x = "50%", y = "50%", count = 5) {
  for (let i = 0; i < count; i++) {
    setTimeout(() => {
      const heart = document.createElement("div");
      heart.innerHTML = "💖";
      heart.style.cssText = `
                position: fixed;
                font-size: ${Math.random() * 20 + 15}px;
                left: ${x};
                top: ${y};
                animation: heartFloat 3s ease-in forwards;
                pointer-events: none;
                z-index: 9999;
                opacity: 0.8;
            `;

      document.body.appendChild(heart);

      setTimeout(() => {
        if (heart.parentNode) {
          heart.parentNode.removeChild(heart);
        }
      }, 3000);
    }, i * 200);
  }
}

// Add heart animation styles
function addHeartAnimationStyles() {
  if (!document.querySelector("#heart-animation-styles")) {
    const style = document.createElement("style");
    style.id = "heart-animation-styles";
    style.textContent = `
            @keyframes heartFloat {
                0% {
                    transform: translate(-50%, -50%) scale(1) rotate(0deg);
                    opacity: 0.8;
                }
                100% {
                    transform: translate(
                        ${Math.random() * 200 - 100}px,
                        -100vh
                    ) scale(0) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
    document.head.appendChild(style);
  }
}

// Page Loader
function showPageLoader() {
  const loader = document.createElement("div");
  loader.id = "page-loader";
  loader.innerHTML = `
        <div class="loader-content">
            <div class="loader-heart">💖</div>
            <div class="loader-text">Loading love...</div>
        </div>
    `;

  document.body.appendChild(loader);

  return loader;
}

function hidePageLoader() {
  const loader = document.getElementById("page-loader");
  if (loader) {
    loader.remove();
  }
}

// Add loader styles
function addLoaderStyles() {
  if (!document.querySelector("#loader-styles")) {
    const style = document.createElement("style");
    style.id = "loader-styles";
    style.textContent = `
            #page-loader {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                backdrop-filter: blur(10px);
            }
            
            .loader-content {
                text-align: center;
                color: white;
            }
            
            .loader-heart {
                font-size: 4rem;
                animation: heartbeat 1.5s ease-in-out infinite;
                margin-bottom: 1rem;
            }
            
            .loader-text {
                font-family: 'Dancing Script', cursive;
                font-size: 1.5rem;
            }
        `;
    document.head.appendChild(style);
  }
}

// Smooth Page Transitions
function navigateTo(url) {
  const loader = showPageLoader();

  setTimeout(() => {
    window.location.href = url;
  }, 500);
}

// Initialize all features when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  console.log("💖 Romantic Website Initialized");

  // Initialize core features
  initializeMusic();
  initializeMenu();

  // Create visual effects
  createRosePetals();
  createFloatingCompliments();

  // Add necessary styles
  addNotificationStyles();
  addHeartAnimationStyles();
  addLoaderStyles();
  addLockConfirmationStyles();

  // Add rose rain button if not on unlock screen
  if (!document.querySelector(".unlock-screen")) {
    const roseButton = document.createElement("button");
    roseButton.className = "rose-rain-btn";
    roseButton.innerHTML = "🌹 Make it Rain Roses";
    roseButton.onclick = makeItRainRoses;

    // Add styles for the button
    if (!document.querySelector("#rose-rain-btn-styles")) {
      const style = document.createElement("style");
      style.id = "rose-rain-btn-styles";
      style.textContent = `
                .rose-rain-btn {
                    position: fixed;
                    bottom: 80px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: var(--primary-color);
                    color: white;
                    border: none;
                    padding: 0.8rem 1.5rem;
                    border-radius: 25px;
                    cursor: pointer;
                    font-size: 1rem;
                    z-index: 1000;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    transition: all 0.3s ease;
                }
                
                .rose-rain-btn:hover {
                    transform: translateX(-50%) scale(1.1);
                    background: var(--accent-color);
                }
            `;
      document.head.appendChild(style);
    }

    document.body.appendChild(roseButton);
  }

  // Add click effects for romantic interactions
  document.addEventListener("click", function (event) {
    // Only create hearts on certain areas, not on interactive elements
    if (
      !event.target.closest("button") &&
      !event.target.closest("a") &&
      !event.target.closest("input") &&
      !event.target.closest(".menu-overlay")
    ) {
      createHeartAnimation(`${event.clientX}px`, `${event.clientY}px`, 1);
    }
  });

  // Show welcome notification
  setTimeout(() => {
    if (!document.querySelector(".unlock-screen")) {
      showNotification("Welcome to our romantic world! 💖", "info");
    }
  }, 1000);
});

// Utility function to check if element is in viewport
function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <=
      (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

// Scroll animations
function initializeScrollAnimations() {
  const animatedElements = document.querySelectorAll(".fade-in-up");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animated");
        }
      });
    },
    { threshold: 0.1 }
  );

  animatedElements.forEach((element) => {
    observer.observe(element);
  });
}

// Add scroll animation styles
function addScrollAnimationStyles() {
  if (!document.querySelector("#scroll-animation-styles")) {
    const style = document.createElement("style");
    style.id = "scroll-animation-styles";
    style.textContent = `
            .fade-in-up {
                opacity: 0;
                transform: translateY(30px);
                transition: all 0.6s ease;
            }
            
            .fade-in-up.animated {
                opacity: 1;
                transform: translateY(0);
            }
        `;
    document.head.appendChild(style);
  }
}

// Initialize scroll animations when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initializeScrollAnimations);
} else {
  initializeScrollAnimations();
}

// Add scroll animation styles
addScrollAnimationStyles();

// Export functions for global access
window.changeTheme = changeTheme;
window.toggleThemeMenu = toggleThemeMenu;
window.toggleMusic = toggleMusic;
window.makeItRainRoses = makeItRainRoses;
window.createHeartAnimation = createHeartAnimation;
window.showNotification = showNotification;
window.navigateTo = navigateTo;
window.handleLock = handleLock;
window.proceedWithLock = proceedWithLock;
window.closeLockConfirmation = closeLockConfirmation;

console.log("💝 Romantic Website JavaScript loaded successfully!");
