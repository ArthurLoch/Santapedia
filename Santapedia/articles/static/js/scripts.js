document.addEventListener('DOMContentLoaded', function(){

    // Navbar items
    const search_bar = document.getElementById('search_bar');
    const search_button = document.getElementById('search_button');
    const magnifying_glass = document.getElementById('magnifying_glass');
    const logo = document.getElementById('logo');
    const menu = document.getElementById('menu');
    const list = document.getElementById('suggestions');

    // ======== THEME BUTTONS (mobile + desktop) ========
    const themeButtons = document.querySelectorAll(".theme-toggle-desktop, .theme-toggle-mobile");
    const body = document.body;

    // ========== SEARCHBAR OPEN ==========
    magnifying_glass.addEventListener('click', function() {
        if (search_bar.value === ''){
            search_bar.style.display = 'inline-block';
            search_button.style.display = 'inline-block';
            search_bar.focus();
        }
    });

    // ========== SEARCH FOCUS ==========
    search_bar.addEventListener("focus", function() {
        logo.style.display = 'none';
        menu.style.display = 'none';
        magnifying_glass.style.display = 'none';

        // Blur the right button (desktop)
        document.querySelector(".theme-toggle-desktop")?.style.setProperty("display", "none", "important");
        document.querySelector(".language-switch-desktop")?.style.setProperty("display", "none", "important");
    });

    // ========== SEARCH BLUR ==========
    search_bar.addEventListener("blur", function() {
        if (search_bar.value === ''){
            logo.style.display = 'inline-block';
            menu.style.display = 'block';
            magnifying_glass.style.display = 'inline-block';
            search_bar.style.display = 'none';
            search_button.style.display = 'none';
            
            if (window.innerWidth > 768) {
            // Display the right button (desktop)
            document.querySelector(".theme-toggle-desktop")?.classList.remove("d-none");
            document.querySelector(".theme-toggle-desktop")?.style.setProperty("display", "inline-block");

            document.querySelector(".language-switch-desktop")?.classList.remove("d-none");
            document.querySelector(".language-switch-desktop")?.style.setProperty("display", "block");
        }
    }});

    // ========== SUGGESTIONS ==========

    search_bar.addEventListener('keyup', function(){
        const query = this.value.trim();

        if (query.length === 0){
            list.style.display = 'none';
            return;
        }

        fetch(window.SEARCH_URL + "?q=" + encodeURIComponent(query))
            .then(res => res.json())
            .then(data => {
                list.innerHTML = '';
                if (data.results.length > 0) {

                    data.results.forEach(item => {
                        const link = document.createElement('a');
                        link.href = `/articles/${item.slug}/`;

                        const container = document.createElement('div');
                        container.style.display = 'flex';
                        container.style.alignItems = 'center';

                        // Image
                        if (item.image) {
                            const img = document.createElement('img');
                            img.src = item.image;
                            img.alt = item.title;
                            img.style.width = '40px';
                            img.style.height = '40px';
                            img.style.objectFit = 'cover';
                            img.style.marginRight = '8px';
                            container.appendChild(img);
                        }

                        // Texts
                        const textWrapper = document.createElement('div');
                        textWrapper.style.display = 'flex';
                        textWrapper.style.flexDirection = 'column';

                        const titleEl = document.createElement('span');
                        titleEl.textContent = item.title;
                        titleEl.style.fontWeight = 'bold';
                        textWrapper.appendChild(titleEl);

                        if (item.description) {
                            const descEl = document.createElement('span');
                            descEl.textContent = item.description;
                            descEl.style.fontSize = '0.85rem';
                            descEl.style.color = '#6c757d';
                            textWrapper.appendChild(descEl);
                        }

                        container.appendChild(textWrapper);
                        link.appendChild(container);
                        list.appendChild(link);
                    });

                    list.style.display = 'block';
                } else {
                    list.style.display = 'none';
                }
            });
    });

    // Close when click outside
    document.addEventListener('click', function(e){
        if (!search_bar.contains(e.target) && !list.contains(e.target)) {
            list.style.display = 'none';
        }
    });


    // ======== THEME SYSTEM (unificado mobile + desktop) ========

    function applySavedTheme() {
        if (localStorage.getItem('theme') === 'dark') {
            body.classList.add('dark-mode');
            themeButtons.forEach(btn => {
                btn.innerHTML = '<i class="bi bi-sun-fill"></i>';
            });
        } else {
            body.classList.remove('dark-mode');
            themeButtons.forEach(btn => {
                btn.innerHTML = '<i class="bi bi-moon-fill"></i>';
            });
        }
    }

    // Apply saved theme on load
    applySavedTheme();

    // OS preference (only if no choice saved)
    if (!localStorage.getItem('theme')) {
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            body.classList.add('dark-mode');
        }
        applySavedTheme();
    }

    // Toggle theme when clicking either button
    themeButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            body.classList.toggle("dark-mode");

            const newTheme = body.classList.contains("dark-mode") ? "dark" : "light";
            localStorage.setItem("theme", newTheme);

            applySavedTheme();
        });
    });



    const banner = document.getElementById("cookie-banner");
    const acceptBtn = document.getElementById("accept-cookies");
    const rejectBtn = document.getElementById("reject-cookies");

    const consent = localStorage.getItem("cookieConsent");

    if (!consent) {
        banner.style.display = "flex";
    }

    acceptBtn.addEventListener("click", function () {
        localStorage.setItem("cookieConsent", "accepted");
        banner.style.display = "none";
        loadGoogleAnalytics();
    });

    rejectBtn.addEventListener("click", function () {
        localStorage.setItem("cookieConsent", "rejected");
        banner.style.display = "none";
    });

    if (consent === "accepted") {
        loadGoogleAnalytics();
    }
    

    function loadGoogleAnalytics() {
    if (window.gaLoaded) return;
    window.gaLoaded = true;

    const script1 = document.createElement("script");
    script1.src = "https://www.googletagmanager.com/gtag/js?id=G-WT1L03EMBY";
    script1.async = true;

    const script2 = document.createElement("script");
    script2.innerHTML = `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-WT1L03EMBY', {
        anonymize_ip: true
        });
    `;

    document.head.appendChild(script1);
    document.head.appendChild(script2);

    }

});