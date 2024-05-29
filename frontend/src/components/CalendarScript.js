document.addEventListener("DOMContentLoaded", function() {
    const daysContainer = document.getElementById('days');
    const monthYear = document.getElementById('monthYear');
    const prevMonth = document.getElementById('prevMonth');
    const nextMonth = document.getElementById('nextMonth');

    let date = new Date();
    let year = date.getFullYear();
    let month = date.getMonth();

    const months = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ];

    function renderCalendar() {
        console.log('Rendering Calendar');
        daysContainer.innerHTML = '';
        monthYear.textContent = `${months[month]} ${year}`;

        const firstDay = new Date(year, month, 1).getDay();
        const lastDate = new Date(year, month + 1, 0).getDate();
        const prevLastDate = new Date(year, month, 0).getDate();

        console.log(`First day: ${firstDay}, Last date: ${lastDate}, Prev last date: ${prevLastDate}`);

        for (let i = firstDay; i > 0; i--) {
            daysContainer.innerHTML += `<div class="prev-date">${prevLastDate - i + 1}</div>`;
            console.log(`Prev month day: ${prevLastDate - i + 1}`);
        }

        for (let i = 1; i <= lastDate; i++) {
            if (i === new Date().getDate() && year === new Date().getFullYear() && month === new Date().getMonth()) {
                daysContainer.innerHTML += `<div class="today">${i}</div>`;
                console.log(`Current month day (today): ${i}`);
            } else {
                daysContainer.innerHTML += `<div>${i}</div>`;
                console.log(`Current month day: ${i}`);
            }
        }

        const totalDays = daysContainer.children.length;
        const nextDays = 42 - totalDays;

        console.log(`Total days in current view: ${totalDays}, Next days to render: ${nextDays}`);

        for (let i = 1; i <= nextDays; i++) {
            daysContainer.innerHTML += `<div class="next-date">${i}</div>`;
            console.log(`Next month day: ${i}`);
        }
    }

    function navigate(direction) {
        month = direction === 'next' ? month + 1 : month - 1;
        if (month > 11) {
            month = 0;
            year++;
        } else if (month < 0) {
            month = 11;
            year--;
        }
        renderCalendar();
    }

    prevMonth.addEventListener('click', () => navigate('prev'));
    nextMonth.addEventListener('click', () => navigate('next'));

    renderCalendar();
});
