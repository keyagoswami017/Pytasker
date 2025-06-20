import React, { useEffect, useState } from 'react';
import AddTask from './AddTask';


const TaskList = () => {
    const [tasks, setTasks] = useState([]);

const fetchTasks = async () => {
    const response = await fetch("http://127.0.1:5000/tasks");
    const data = await response.json();
    setTasks(data);
};

const deleteTask = async (id) => {
    const response = await fetch(`http://127.0.1:5000/tasks/${id}`, {
        method: 'DELETE'
    }); 
    if (response.ok) {
        setTasks(tasks.filter(task => task.id !== id));
    } else {
        console.error("Failed to delete task:", response.statusText);
    }
};

    useEffect(() => {
        fetchTasks();
    } , []);

    return (
        <div>
            <h1>Task List</h1>
            <AddTask onTaskAdded={fetchTasks}/>
            <ul>
                {tasks.map((task) => (
                    <li key={task.id}>
                        <strong>{task.title}</strong> : {task.description} - {task.status}
                        <button
                            onClick={() => deleteTask(task.id)}
                            style={{ marginLeft: '10px', color: 'red' }}
                        >
                            Delete
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TaskList;
