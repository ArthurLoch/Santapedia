document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    const saintsListEl = document.querySelector("#saints-list");
  
    function renderSaintsList(month, year) {
      // Get the date
      fetch(`/ajax/saints-by-month/?month=${month}&year=${year}`)
        .then(response => {
          if (!response.ok) throw new Error("Erro na resposta: " + response.status);
          return response.json();
        })
        .then(data => {
          saintsListEl.innerHTML = ""; // clear the list
          // if don't exists saints in that month
          if (!data.saints || data.saints.length === 0) {
            if (window.currentLanguage === 'en') {
              saintsListEl.innerHTML = "<p class='text-muted text-center mb-0'>No saints are recorded this month.</p>";
              return;
            } else {
              saintsListEl.innerHTML = "<p class='text-muted text-center mb-0'>Nenhum santo registrado neste mês.</p>";
              return;
            }
            
          }
          
          // create a <a> for each saint in that month
          data.saints.forEach(saint => {
            const saintItem = document.createElement("a");
            saintItem.href = `/articles/${saint.slug}/`
            saintItem.classList.add("d-flex", "align-items-center", "mb-3");
  
            const imageHtml = saint.image
              ? `<img src="${saint.image}" alt="${saint.title}" class="rounded me-3" style="width:60px;height:60px;object-fit:cover;">`
              : `<div class="rounded bg-light d-flex align-items-center justify-content-center me-3" style="width:60px;height:60px;color:gray;"><i class="bi bi-person-fill"></i></div>`;
  

            if (window.currentLanguage === 'en') {
              
              console.log(`${saint.title}`)
              saintItem.innerHTML = `
              ${imageHtml}
              <div>
                <p class="fw-semibold text-decoration-none">
                  ${saint.title}
                </p>
                <div class="text-muted small">${new Date(2000, saint.month - 1).toLocaleString('en', { month: 'long' })} ${saint.day}</div>
              </div>
              `;

            } else {
              
              console.log(`${saint.title}`)
              saintItem.innerHTML = `
              ${imageHtml}
              <div>
                <p class="fw-semibold text-decoration-none">
                  ${saint.title}
                </p>
                <div class="text-muted small">${saint.day} de ${new Date(2000, saint.month - 1).toLocaleString('pt-BR', { month: 'long' })}</div>
              </div>
              `;

            }
            
            saintsListEl.appendChild(saintItem);
          });
        })
        .catch(err => {
          // if there is any error
          if (window.currentLanguage === 'en') {
            console.error("Error loading saints:", err);
            saintsListEl.innerHTML = "<p class='text-danger text-center'>Error loading saints for this month.</p>"
          } else {
            console.error("Erro ao carregar santos:", err);
            saintsListEl.innerHTML = "<p class='text-danger text-center'>Erro ao carregar santos deste mês.</p>"
          }
          ;
        });
    }
  
    // create the calendar
    const calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      locale: currentLanguage == 'en' ? 'en' : 'pt-br',
      timeZone: 'local',    // importante
      height: 'auto',
      headerToolbar: { left: 'prev,next today', center: 'title', right: '' },
      buttonText: currentLanguage == 'en' ? { today: 'Today' } : { today: 'Hoje' },
      events: "/ajax/calendar-data/",
      eventClick: function(info) { /* ... */ },
      eventDidMount: function(info) { /* estilo */ },
      datesSet: function(info) {
        const currentMonth = info.view.currentStart.getMonth() + 1;
        const currentYear  = info.view.currentStart.getFullYear();
        renderSaintsList(currentMonth, currentYear);
      },
      noEventsContent: currentLanguage == 'en' ? "No saints are recorded this month." : "Nenhum santo registrado neste mês."
    });
  
    calendar.render();
  
    // Load the saints of the currently month
    const viewStart = calendar.view.currentStart;
    const monthNow = viewStart.getMonth() + 1;
    const yearNow = viewStart.getFullYear();
    renderSaintsList(monthNow, yearNow);
});