document.addEventListener("DOMContentLoaded", function () {

    const countrySelect = document.getElementById("country");
    const stateSelect = document.getElementById("state");
    const citySelect = document.getElementById("city");

    function reset(select, text, disabled = true) {
        select.innerHTML = `<option value="" disabled selected>${text}</option>`;
        select.disabled = disabled;
    }

    // Initial state
    if (!countrySelect.value) {
        currentLanguage == 'en' ? reset(stateSelect, "Choose the state") : reset(stateSelect, "Escolha o estado");
        currentLanguage == 'en' ? reset(citySelect, "Choose the city") : reset(citySelect, "Escolha a cidade");
    }

    // COUNTRY → STATES
    countrySelect.addEventListener("change", function () {
        currentLanguage == 'en' ? reset(stateSelect, "Loading states...", false) : reset(stateSelect, "Carregando estados...", false);
        currentLanguage == 'en' ? reset(citySelect, "Choose the city") : reset(citySelect, "Escolha a cidade");

        fetch(`${djangoVars.getStatesUrl}?country=${this.value}`)
            .then(res => res.json())
            .then(data => {
                currentLanguage == 'en' ? reset(stateSelect, "Choose the state", false) : reset(stateSelect, "Escolha o estado", false);
                data.states.forEach(state => {
                    const opt = document.createElement("option");
                    opt.value = state.abbreviation;
                    opt.textContent = state.name;
                    stateSelect.appendChild(opt);
                });
            });
    });

    // STATE → CITIES
    stateSelect.addEventListener("change", function () {
        currentLanguage == 'en' ? reset(citySelect, "Loading cities...", false) : reset(citySelect, "Carregando cidades...", false);

        fetch(`${djangoVars.getCitiesUrl}?state=${this.value}&country=${countrySelect.value}`)
            .then(res => res.json())
            .then(data => {
                currentLanguage == 'en' ? reset(citySelect, "Choose the city", false) : reset(citySelect, "Escolha a cidade", false);
                data.cities.forEach(city => {
                    const opt = document.createElement("option");
                    opt.value = city.id;
                    opt.textContent = city.name;
                    citySelect.appendChild(opt);
                });
            });
    });

});