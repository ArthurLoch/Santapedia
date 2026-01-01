document.addEventListener('DOMContentLoaded', function() {
    // === Feast Day ===
    if (window.feastDay) {
        const monthNum = parseInt(window.feastDay.month);
        const dayNum = window.feastDay.day;
        const feast_day = document.getElementById('feast_day');

        if (feast_day && !isNaN(monthNum)) {
            const months_pt = [
                'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
            ];
            const months_en = [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ];
            if (window.currentLanguage === 'en') {
                feast_day.innerHTML = `${months_en[monthNum - 1]} ${dayNum}`;
            } else {
                feast_day.innerText = `${dayNum} de ${months_pt[monthNum - 1]}`;
            }
            
        }
    }

    // === Automatically generate a table of contents based on <h2> and <h3> tags ===
    const tocList = document.getElementById('toc-list');
    const articleContent = document.querySelector('.content');

    if (tocList && articleContent) {
        tocList.innerHTML = ''; // Clear the default index
        const headings = articleContent.querySelectorAll('h2, h3');

        headings.forEach((heading, index) => {
            // Create a unique ID for each heading if it doesn't have one
            if (!heading.id) {
                heading.id = 'section-' + index;
            }

            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#' + heading.id;
            a.textContent = heading.textContent;

            // Indent <h3> tags to show hierarchy
            if (heading.tagName.toLowerCase() === 'h3') {
                li.style.marginLeft = '1rem';
                li.style.fontSize = '0.95em';
            }

            li.appendChild(a);
            tocList.appendChild(li);
        });

        // If no headings are found, remove the 'In this article' block
        if (headings.length === 0) {
            document.querySelector('.article-index').remove();
        }
    }

    // Smooth scroll ===
    document.querySelectorAll('.article-index a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
