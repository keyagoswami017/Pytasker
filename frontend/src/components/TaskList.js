import React, { useEffect, useState } from 'react';
import AddTask from './AddTask';


const TaskList = () => {
    const [tasks, setTasks] = useState([]);

const fetchTasks = async () => {
    const response = await fetch("http://127.0.1:5000/tasks");
    const data = await response.json();
    setTasks(data);
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
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TaskList;
