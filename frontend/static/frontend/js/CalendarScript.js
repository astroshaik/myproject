document.addEventListener('DOMContentLoaded', (event) => {
  let nav = 0;
  let clicked = null;
  let events = localStorage.getItem('events') ? JSON.parse(localStorage.getItem('events')) : [];

  const calendar = document.getElementById('calendar');
  const newEventModal = document.getElementById('newEventModal');
  const deleteEventModal = document.getElementById('deleteEventModal');
  const backDrop = document.getElementById('modalBackDrop');
  const eventTypeInput = document.getElementById('eventType');
  const eventTitleInput = document.getElementById('eventTitleInput');
  const roomieIdInput = document.getElementById('roomieIdInput');
  const eventPersonInput = document.getElementById('eventPersonInput');
  const startTimeInput = document.getElementById('startTimeInput');
  const endTimeInput = document.getElementById('endTimeInput');

  const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  function openModal(date) {
    clicked = date;

    const eventForDay = events.filter(e => e.date === clicked);

    if (eventForDay.length > 0) {
      document.getElementById('eventText').innerText = eventForDay.map(e => e.title).join(', ');
      deleteEventModal.style.display = 'block';
    } else {
      newEventModal.style.display = 'block';
    }

    backDrop.style.display = 'block';
  }

  function load() {
    const dt = new Date();

    if (nav !== 0) {
      dt.setMonth(new Date().getMonth() + nav);
    }

    const day = dt.getDate();
    const month = dt.getMonth();
    const year = dt.getFullYear();

    const firstDayOfMonth = new Date(year, month, 1);
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const dateString = firstDayOfMonth.toLocaleDateString('en-us', {
      weekday: 'long',
      year: 'numeric',
      month: 'numeric',
      day: 'numeric',
    });
    const paddingDays = weekdays.indexOf(dateString.split(', ')[0]);

    document.getElementById('monthDisplay').innerText =
      `${dt.toLocaleDateString('en-us', { month: 'long' })} ${year}`;

    calendar.innerHTML = '';

    for (let i = 1; i <= paddingDays + daysInMonth; i++) {
      const daySquare = document.createElement('div');
      daySquare.classList.add('day');

      const dayString = `${month + 1}/${i - paddingDays}/${year}`;

      if (i > paddingDays) {
        daySquare.innerText = i - paddingDays;
        const eventForDay = events.filter(e => e.date === dayString);

        if (i - paddingDays === day && nav === 0) {
          daySquare.id = 'currentDay';
        }

        eventForDay.forEach(event => {
          const eventDiv = document.createElement('div');
          eventDiv.classList.add('event');
          eventDiv.classList.add(`event-${event.type}`); // Adding class for color coding
          eventDiv.innerText = event.title;
          daySquare.appendChild(eventDiv);
        });

        daySquare.addEventListener('click', () => openModal(dayString));
      } else {
        daySquare.classList.add('padding');
      }

      calendar.appendChild(daySquare);
    }
  }

  function closeModal() {
    eventTitleInput.classList.remove('error');
    roomieIdInput.classList.remove('error');
    eventPersonInput.classList.remove('error');
    startTimeInput.classList.remove('error');
    endTimeInput.classList.remove('error');

    newEventModal.style.display = 'none';
    deleteEventModal.style.display = 'none';
    backDrop.style.display = 'none';
    eventTypeInput.value = '0';
    eventTitleInput.value = '';
    roomieIdInput.value = '';
    eventPersonInput.value = '';
    startTimeInput.value = '';
    endTimeInput.value = '';

    clicked = null;
    load();
  }

  function saveEvent() {
    const title = eventTitleInput.value;
    const roomieId = roomieIdInput.value;
    const person = eventPersonInput.value;
    const startTime = startTimeInput.value;
    const endTime = endTimeInput.value;

    if (title && roomieId && person && startTime && endTime) {
      eventTitleInput.classList.remove('error');
      roomieIdInput.classList.remove('error');
      eventPersonInput.classList.remove('error');
      startTimeInput.classList.remove('error');
      endTimeInput.classList.remove('error');

      events.push({
        date: clicked,
        title,
        roomieId,
        person,
        startTime,
        endTime,
        type: eventTypeInput.value
      });

      localStorage.setItem('events', JSON.stringify(events));
      closeModal();
    } else {
      if (!title) eventTitleInput.classList.add('error');
      if (!roomieId) roomieIdInput.classList.add('error');
      if (!person) eventPersonInput.classList.add('error');
      if (!startTime) startTimeInput.classList.add('error');
      if (!endTime) endTimeInput.classList.add('error');
    }
  }

  function deleteEvent() {
    events = events.filter(e => e.date !== clicked);
    localStorage.setItem('events', JSON.stringify(events));
    closeModal();
  }

  function initButtons() {
    document.getElementById('nextButton').addEventListener('click', () => {
      nav++;
      load();
    });

    document.getElementById('backButton').addEventListener('click', () => {
      nav--;
      load();
    });

    document.getElementById('saveButton').addEventListener('click', saveEvent);
    document.getElementById('cancelButton').addEventListener('click', closeModal);
    document.getElementById('deleteButton').addEventListener('click', deleteEvent);
    document.getElementById('closeButton').addEventListener('click', closeModal);
  }

  initButtons();
  load();
});

