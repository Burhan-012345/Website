let password = "";

document.addEventListener("DOMContentLoaded", function () {
  createRosePetals();

  // Add keyboard event listeners
  document.querySelectorAll(".num-key").forEach((button) => {
    button.addEventListener("click", function () {
      const key = this.getAttribute("data-key");

      if (key === "clear") {
        password = "";
        updatePasswordDisplay();
      } else if (key === "unlock") {
        attemptUnlock();
      } else if (password.length < 10) {
        password += key;

        // Auto-insert hyphens
        if (password.length === 2 || password.length === 5) {
          password += "-";
        }

        updatePasswordDisplay();
      }
    });
  });

  // Add keyboard support
  document.addEventListener("keydown", function (event) {
    if (event.key >= "0" && event.key <= "9" && password.length < 10) {
      password += event.key;

      if (password.length === 2 || password.length === 5) {
        password += "-";
      }

      updatePasswordDisplay();
    } else if (event.key === "Backspace") {
      password = password.slice(0, -1);
      updatePasswordDisplay();
    } else if (event.key === "Enter") {
      attemptUnlock();
    }
  });
});

function updatePasswordDisplay() {
  const input = document.getElementById("passwordInput");
  input.value = password;

  // Add glowing effect when typing
  input.classList.add("glow");
  setTimeout(() => input.classList.remove("glow"), 300);
}

function attemptUnlock() {
  const messageDiv = document.getElementById("unlockMessage");

  if (password === "16-09-2008") {
    messageDiv.textContent = "Mera dil khul gaya! ❤️";
    messageDiv.style.color = "#4CAF50";

    // Add celebration effects
    celebrateUnlock();

    // Send unlock request to server
    sendUnlockRequest();
  } else {
    messageDiv.textContent =
      "Yeh sahi password nahi hai. Phir se koshish karein.";
    messageDiv.style.color = "#f44336";

    // Shake animation
    const container = document.querySelector(".unlock-container");
    container.classList.add("shake");
    setTimeout(() => container.classList.remove("shake"), 500);

    // Clear password after incorrect attempt
    setTimeout(() => {
      password = "";
      updatePasswordDisplay();
      messageDiv.textContent = "";
    }, 2000);
  }
}

function sendUnlockRequest() {
  fetch("/unlock", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      password: password,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Success - redirect to loading page after celebration
        setTimeout(() => {
          window.location.href = "/loading";
        }, 2000);
      } else {
        // Server-side validation failed
        const messageDiv = document.getElementById("unlockMessage");
        messageDiv.textContent =
          data.message || "Kuch gadbad hai. Phir se koshish karein.";
        messageDiv.style.color = "#f44336";

        // Reset password
        password = "";
        updatePasswordDisplay();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      const messageDiv = document.getElementById("unlockMessage");
      messageDiv.textContent = "Network error. Phir se koshish karein.";
      messageDiv.style.color = "#f44336";
    });
}

function celebrateUnlock() {
  const container = document.querySelector(".unlock-container");

  // Create heart explosion
  for (let i = 0; i < 20; i++) {
    const heart = document.createElement("div");
    heart.innerHTML = "💖";
    heart.style.position = "absolute";
    heart.style.fontSize = "2rem";
    heart.style.left = "50%";
    heart.style.top = "50%";
    heart.style.transform = "translate(-50%, -50%)";
    heart.style.animation = `heartExplosion 1s ease-out forwards ${i * 0.1}s`;
    heart.style.zIndex = "1000";
    heart.style.pointerEvents = "none";

    container.appendChild(heart);

    // Remove hearts after animation
    setTimeout(() => {
      if (heart.parentNode) {
        heart.parentNode.removeChild(heart);
      }
    }, 1000 + i * 100);
  }

  // Add CSS for heart explosion if not already added
  if (!document.querySelector("#unlock-animations")) {
    const style = document.createElement("style");
    style.id = "unlock-animations";
    style.textContent = `
            @keyframes heartExplosion {
                0% {
                    transform: translate(-50%, -50%) scale(1);
                    opacity: 1;
                }
                100% {
                    transform: translate(
                        ${Math.random() * 200 - 100}px,
                        ${Math.random() * 200 - 100}px
                    ) scale(0);
                    opacity: 0;
                }
            }
            
            .shake {
                animation: shake 0.5s ease-in-out;
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-10px); }
                75% { transform: translateX(10px); }
            }
            
            .glow {
                box-shadow: 0 0 20px #e91e63;
                transition: box-shadow 0.3s ease;
            }
        `;
    document.head.appendChild(style);
  }
}

// Rose petals for unlock screen
function createRosePetals() {
  const container = document.getElementById("rosePetals");
  if (!container) return;

  for (let i = 0; i < 25; i++) {
    const petal = document.createElement("div");
    petal.className = "rose-petal";

    const size = Math.random() * 20 + 10;
    const left = Math.random() * 100;
    const animationDuration = Math.random() * 15 + 10;
    const animationDelay = Math.random() * 5;

    petal.style.width = `${size}px`;
    petal.style.height = `${size}px`;
    petal.style.left = `${left}vw`;
    petal.style.animationDuration = `${animationDuration}s`;
    petal.style.animationDelay = `${animationDelay}s`;
    petal.style.background = `hsl(${Math.random() * 20 + 330}, 70%, 65%)`;

    container.appendChild(petal);
  }
}
