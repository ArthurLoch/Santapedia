document.addEventListener("DOMContentLoaded", function () {
    if (typeof prayersData === "undefined") return;

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
