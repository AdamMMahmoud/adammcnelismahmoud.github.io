// Typing animation functionality
const words = ["data science.", "machine learning.", "problem solving.", "numerical analysis."];
let wordIndex = 0;
let isDeleting = false;
let typingSpeed = 150; // typing speed in milliseconds
let deleteSpeed = 100;
const typingContainer = document.getElementById("typingContainer");

function typeWriter() {
    if (wordIndex < words.length) {
        let currentWord = words[wordIndex];
        let currentText = typingContainer.innerText;

        if (!isDeleting) {
            // Typing the word
            typingContainer.innerText = currentWord.substring(0, currentText.length + 1);

            if (currentText === currentWord) {
                // Pause at the end of a word before deleting
                setTimeout(() => {
                    isDeleting = true;
                }, 1000);
            }
        } else {
            // Deleting the word
            typingContainer.innerText = currentWord.substring(0, currentText.length - 1);

            if (currentText === "") {
                // Move to the next word
                wordIndex = (wordIndex + 1) % words.length;
                isDeleting = false;
            }
        }
    }
    setTimeout(typeWriter, isDeleting ? deleteSpeed : typingSpeed);
}

// Smooth scrolling functionality
document.querySelectorAll("nav a").forEach((link) => {
    link.addEventListener("click", (event) => {
        event.preventDefault();
        const targetId = event.target.getAttribute("href").substring(1);
        const targetElement = document.getElementById(targetId);

        if (targetElement) {
            const headerOffset = document.querySelector("header").offsetHeight;
            const elementPosition = targetElement.offsetTop;
            const offsetPosition = elementPosition - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: "smooth",
            });
        }
    });
});

// Initialize typing animation
typeWriter();
