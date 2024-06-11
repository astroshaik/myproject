document.addEventListener('DOMContentLoaded', (event) => {
  let nav = 0;
  let clicked = null;
  let events = localStorage.getItem('events') ? JSON.parse(localStorage.getItem('events')) : [];
  let selectedEvent = null;

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
  const saveButton = document.getElementById('saveButton');
  const deleteButton = document.getElementById('deleteButton');
  const closeButton = document.getElementById('closeButton');
  const editButton = document.getElementById('editButton');

  const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  function openModal(date, event = null) {
    clicked = date;
    selectedEvent = event;

    if (event) {
      document.getElementById('eventDetails').innerText = `
        Title: ${event.title}
        Roomie ID: ${event.roomieId}
        Person: ${event.person}
        Start Time: ${event.startTime}
        End Time: ${event.endTime}
        Type: ${event.type === '0' ? 'Chore' : event.type === '1' ? 'Visitor' : 'Reservation'}
      `;
      deleteEventModal.style.display = 'block';
    } else {
      eventTypeInput.value = '0';
      eventTitleInput.value = '';
      roomieIdInput.value = '';
      eventPersonInput.value = '';
      startTimeInput.value = '';
      endTimeInput.value = '';
      saveButton.textContent = 'Save';
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
          eventDiv.innerText = event.title;
          eventDiv.addEventListener('click', (e) => {
            e.stopPropagation();
            openModal(dayString, event);
          });
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
    newEventModal.style.display = 'none';
    deleteEventModal.style.display = 'none';
    backDrop.style.display = 'none';
    saveButton.textContent = 'Save';

    eventTitleInput.classList.remove('error');
    roomieIdInput.classList.remove('error');
    eventPersonInput.classList.remove('error');
    startTimeInput.classList.remove('error');
    endTimeInput.classList.remove('error');

    clicked = null;
    selectedEvent = null;
    load();
  }

  function saveEvent() {
    if (eventTitleInput.value && roomieIdInput.value && eventPersonInput.value && startTimeInput.value && endTimeInput.value) {
      const newEvent = {
        date: clicked,
        title: eventTitleInput.value,
        roomieId: roomieIdInput.value,
        person: eventPersonInput.value,
        startTime: startTimeInput.value,
        endTime: endTimeInput.value,
        type: eventTypeInput.value
      };

      if (selectedEvent) {
        const existingEventIndex = events.findIndex(e => e === selectedEvent);
        events[existingEventIndex] = newEvent;
      } else {
        events.push(newEvent);
      }

      localStorage.setItem('events', JSON.stringify(events));
      closeModal();
    } else {
      if (!eventTitleInput.value) eventTitleInput.classList.add('error');
      if (!roomieIdInput.value) roomieIdInput.classList.add('error');
      if (!eventPersonInput.value) eventPersonInput.classList.add('error');
      if (!startTimeInput.value) startTimeInput.classList.add('error');
      if (!endTimeInput.value) endTimeInput.classList.add('error');
    }
  }

  function deleteEvent() {
    if (selectedEvent) {
      events = events.filter(e => e !== selectedEvent);
      localStorage.setItem('events', JSON.stringify(events));
      closeModal();
    }
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

    saveButton.addEventListener('click', saveEvent);
    deleteButton.addEventListener('click', deleteEvent);
    document.getElementById('cancelButton').addEventListener('click', closeModal);
    closeButton.addEventListener('click', closeModal);
    editButton.addEventListener('click', () => {
      if (selectedEvent) {
        eventTypeInput.value = selectedEvent.type;
        eventTitleInput.value = selectedEvent.title;
        roomieIdInput.value = selectedEvent.roomieId;
        eventPersonInput.value = selectedEvent.person;
        startTimeInput.value = selectedEvent.startTime;
        endTimeInput.value = selectedEvent.endTime;
        newEventModal.style.display = 'block';
        deleteEventModal.style.display = 'none';
      }
    });
  }

  initButtons();
  load();
});
