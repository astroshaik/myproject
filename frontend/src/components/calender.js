import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CalendarTaskPage() {
    const [roomies, setRoomies] = useState([]);
    const [selectedRoomie, setSelectedRoomie] = useState('');
    const [taskType, setTaskType] = useState('');
    const [description, setDescription] = useState('');
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');

    useEffect(() => {
        axios.get('/api/roomies/')
            .then(response => setRoomies(response.data))
            .catch(error => console.error('Error fetching roomies:', error));
    }, []);

    const handleSubmit = (event) => {
        event.preventDefault();
        axios.post('/api/tasks/', { roomie: selectedRoomie, task_type: taskType, description, start_time: startTime, end_time: endTime })
            .then(response => alert('Task created successfully'))
            .catch(error => alert('Failed to create task'));
    };

    return (
        <div>
            <h1>Add New Task</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Roomie:
                    <select value={selectedRoomie} onChange={e => setSelectedRoomie(e.target.value)}>
                        {roomies.map(roomie => <option key={roomie.roomie_id} value={roomie.roomie_id}>{roomie.email}</option>)}
                    </select>
                </label>
                <label>
                    Task Type:
                    <input type="text" value={taskType} onChange={e => setTaskType(e.target.value)} />
                </label>
                <label>
                    Description:
                    <textarea value={description} onChange={e => setDescription(e.target.value)} />
                </label>
                <label>
                    Start Time:
                    <input type="datetime-local" value={startTime} onChange={e => setStartTime(e.target.value)} />
                </label>
                <label>
                    End Time:
                    <input type="datetime-local" value={endTime} onChange={e => setEndTime(e.target.value)} />
                </label>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default CalendarTaskPage;
