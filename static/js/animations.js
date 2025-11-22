// Advanced animations for the romantic website
class RomanticAnimations {
  constructor() {
    this.init();
  }

  init() {
    this.createFloatingHearts();
    this.initSmoothScrolling();
    this.initParallaxEffects();
    this.initTypewriterEffects();
  }

  // Floating hearts animation
  createFloatingHearts() {
    setInterval(() => {
      if (Math.random() < 0.3) {
        this.createFloatingHeart();
      }
    }, 2000);
  }

  createFloatingHeart() {
    const heart = document.createElement("div");
    heart.innerHTML = "💖";
    heart.style.position = "fixed";
    heart.style.fontSize = `${Math.random() * 20 + 15}px`;
    heart.style.left = `${Math.random() * 100}vw`;
    heart.style.top = "100vh";
    heart.style.zIndex = "9999";
    heart.style.pointerEvents = "none";
    heart.style.opacity = "0.7";
    heart.style.animation = `floatHeartUp ${
      Math.random() * 10 + 10
    }s ease-in forwards`;

    document.body.appendChild(heart);

    setTimeout(() => {
      heart.remove();
    }, 15000);
  }

  // Smooth scrolling for navigation
  initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      });
    });
  }

  // Parallax effects for depth
  initParallaxEffects() {
    window.addEventListener("scroll", () => {
      const scrolled = window.pageYOffset;
      const parallaxElements = document.querySelectorAll("[data-parallax]");

      parallaxElements.forEach((element) => {
        const speed = element.dataset.parallaxSpeed || 0.5;
        element.style.transform = `translateY(${scrolled * speed}px)`;
      });
    });
  }

  // Typewriter effect for romantic messages
  initTypewriterEffects() {
    document.querySelectorAll("[data-typewriter]").forEach((element) => {
      this.typewriterEffect(element, element.textContent);
    });
  }

  typewriterEffect(element, text) {
    element.textContent = "";
    let i = 0;

    function type() {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        i++;
        setTimeout(type, 100);
      }
    }

    // Start after a delay
    setTimeout(type, 1000);
  }

  // Confetti explosion for special moments
  createConfetti() {
    const colors = ["#e91e63", "#9c27b0", "#673ab7", "#3f51b5", "#2196f3"];
    const confettiCount = 100;

    for (let i = 0; i < confettiCount; i++) {
      const confetti = document.createElement("div");
      confetti.className = "confetti";
      confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${
                  colors[Math.floor(Math.random() * colors.length)]
                };
                top: -10px;
                left: ${Math.random() * 100}vw;
                border-radius: ${Math.random() > 0.5 ? "50%" : "0"};
                animation: confettiFall ${
                  Math.random() * 3 + 2
                }s linear forwards;
                z-index: 9999;
                pointer-events: none;
            `;

      document.body.appendChild(confetti);

      setTimeout(() => confetti.remove(), 5000);
    }
  }

  // Heart trail effect
  initHeartTrail() {
    let heartTrail = [];
    const maxHearts = 10;

    document.addEventListener("mousemove", (e) => {
      if (Math.random() < 0.3) {
        const heart = document.createElement("div");
        heart.innerHTML = "💖";
        heart.style.position = "fixed";
        heart.style.left = `${e.clientX}px`;
        heart.style.top = `${e.clientY}px`;
        heart.style.fontSize = "15px";
        heart.style.pointerEvents = "none";
        heart.style.zIndex = "9999";
        heart.style.opacity = "0.7";
        heart.style.animation = "heartFade 1s ease-out forwards";

        document.body.appendChild(heart);

        heartTrail.push(heart);

        if (heartTrail.length > maxHearts) {
          const oldHeart = heartTrail.shift();
          if (oldHeart && oldHeart.parentNode) {
            oldHeart.parentNode.removeChild(oldHeart);
          }
        }

        setTimeout(() => {
          if (heart.parentNode) {
            heart.parentNode.removeChild(heart);
          }
        }, 1000);
      }
    });
  }

  // Pulse animation for important elements
  pulseElement(element) {
    element.style.animation = "pulse 2s ease-in-out";
    setTimeout(() => {
      element.style.animation = "";
    }, 2000);
  }

  // Romantic text glow effect
  initTextGlow() {
    document.querySelectorAll(".romantic-text").forEach((element) => {
      element.addEventListener("mouseenter", () => {
        element.style.textShadow = "0 0 10px var(--glow-color)";
      });

      element.addEventListener("mouseleave", () => {
        element.style.textShadow = "none";
      });
    });
  }
}

// Initialize animations when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  const animations = new RomanticAnimations();
  window.romanticAnimations = animations;

  // Add CSS for new animations
  const style = document.createElement("style");
  style.textContent = `
        @keyframes floatHeartUp {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 0.7;
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
                opacity: 0;
            }
        }

        @keyframes confettiFall {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(100vh) rotate(360deg);
                opacity: 0;
            }
        }

        @keyframes heartFade {
            0% {
                transform: scale(1) translateY(0);
                opacity: 0.7;
            }
            100% {
                transform: scale(0) translateY(-20px);
                opacity: 0;
            }
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .romantic-text {
            transition: text-shadow 0.3s ease;
        }

        .confetti {
            pointer-events: none;
        }
    `;
  document.head.appendChild(style);
});

// Special effects for specific pages
function initStarAnimations() {
  const stars = document.querySelectorAll(".star");
  stars.forEach((star, index) => {
    star.style.animationDelay = `${index * 0.5}s`;
  });
}

function initGiftAnimations() {
  const gift = document.querySelector(".gift-box");
  if (gift) {
    gift.addEventListener("click", function () {
      this.classList.toggle("open");
      if (this.classList.contains("open")) {
        // Create burst effect
        window.romanticAnimations.createConfetti();

        // Play celebration sound if available
        const audio = new Audio("static/audio/celebration.mp3");
        audio.volume = 0.3;
        audio.play().catch(() => {}); // Ignore errors
      }
    });
  }
}
