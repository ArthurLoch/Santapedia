document.addEventListener("DOMContentLoaded", function () {

    if (typeof prayersData === "undefined") return;

    function getMaxChars() {
        const width = window.innerWidth;
        if (width <= 991) return 100;
        if (width >= 1200) return 350;
        return 175;
    }

    function truncateText(text, limit) {
        if (text.length <= limit) return text;
        let truncated = text.substring(0, limit);
        const lastSpace = truncated.lastIndexOf(" ");
        if (lastSpace > 0) truncated = truncated.substring(0, lastSpace);
        return truncated + "...";
    }

    const maxChars = getMaxChars();

    document.querySelectorAll(".collapse-btn").forEach(btn => {
        const id = btn.getAttribute("data-id");
        const textDiv = document.getElementById(`text-${id}`);

        if (!textDiv || !prayersData[id]) return;

        const fullText = prayersData[id].full.replace(/(<([^>]+)>)/gi, "");
        const shortText = truncateText(fullText, maxChars);

        textDiv.innerHTML = shortText;

        if (fullText.length <= maxChars) {
            btn.style.display = "none";
            textDiv.innerHTML = prayersData[id].full;
            return;
        }

        let expanded = false;

        btn.addEventListener("click", () => {
            expanded = !expanded;
            textDiv.innerHTML = expanded ? prayersData[id].full : shortText;
            btn.innerHTML = expanded
                ? 'Fechar oração <i class="bi bi-chevron-up"></i>'
                : 'Ler oração completa <i class="bi bi-chevron-down"></i>';
        });
    });
});
