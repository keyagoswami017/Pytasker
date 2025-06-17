import React , {useState  } from "react";

const AddTask = ({ onTaskAdded }) => {
    const [title, setTitle] = useState ("");
    const [description, setDescription] = useState ("");
    const [status, setStatus] = useState ("Pending");

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const newTask = { title, description, status };

        try{
            const response = await fetch("http://127.0.0.1:5000/tasks", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(newTask),
            });

            if(response.ok) {
                const result = await response.json();
                console.log("Task added:", result);
                onTaskAdded();
                setTitle("");
                setDescription("");
                setStatus("Pending");
            } else{
                console.error("Failed adding task:", response.statusText);
            }

        }
        catch (error) {
            console.error("Error adding task:", error);
        }
    };
    return (
        <form onSubmit={handleSubmit}>
            <h2> Add Tasks </h2>
            <div>
                <label> Title: </label>
                <input
                    value = {title}
                    onChange = {(e) => setTitle(e.target.value)}
                    required
                />
            </div>
            <div>
                <label> Description: </label>
                <input
                    value = {description}
                    onChange = {(e) => setDescription(e.target.value)}
                    required
                />
            </div>
            <div>
                <label> Status: </label>
                <select value = {status} onChange = {(e) => setStatus(e.target.value)}>
                    <option value = "Pending">Pending</option>
                    <option value = "In Progress">In Progress</option>
                    <option value = "Completed">Completed</option>
                </select>
            </div>
            <button type="submit">Add Task</button>

        </form>

    );
};

export default AddTask;