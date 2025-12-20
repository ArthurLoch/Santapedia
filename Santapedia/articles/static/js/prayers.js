// Get the screen's width 
function getMaxChars() {
    const width = window.innerWidth;
    if (width <= 991) return 100;      // smartphone
    if (width >= 1200) return 350;     // big screen
    return 175;                        // tablets and laptops
}

const maxChars = getMaxChars();

// Cut the text without break the words
function truncateText(text, limit) {
    if (text.length <= limit) return text;
    let truncated = text.substring(0, limit);
    const lastSpace = truncated.lastIndexOf(" ");
    if (lastSpace > 0) truncated = truncated.substring(0, lastSpace);
    return truncated + "...";
}

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".collapse-btn").forEach(btn => {
        // return the short or full version 
        const id = btn.getAttribute("data-id");
        const textDiv = document.getElementById(`text-${id}`);
        const fullText = prayersData[id].full.replace(/(<([^>]+)>)/gi, ""); // remove tags HTML
        const shortText = truncateText(fullText, maxChars);

        // Inicial text
        textDiv.innerHTML = shortText;

        // If the prayer already covers the entire thing, hide the button
        if (fullText.length <= maxChars) {
            btn.style.display = "none";
            textDiv.innerHTML = prayersData[id].full; // Show all
            return;
        }

        let expanded = false;

        // Toggle between summary and full text
        btn.addEventListener("click", () => {
            expanded = !expanded;
            if (expanded) {
                textDiv.innerHTML = prayersData[id].full;
                btn.innerHTML = 'Fechar oração <i class="bi bi-chevron-up"></i>';
            } else {
                textDiv.innerHTML = shortText;
                btn.innerHTML = 'Ler oração completa <i class="bi bi-chevron-down"></i>';
            }
        });
    });
});

// Automatically updates if the user resizes the window
window.addEventListener('resize', () => {
    clearTimeout(window.resizeTimeout);
    window.resizeTimeout = setTimeout(() => location.reload(), 500);
});