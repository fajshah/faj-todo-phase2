import React from 'react';
import TaskForm from '../components/TaskForm';
import TaskList from '../components/TaskList';

const Dashboard = () => {
  const handleTaskSubmit = async (taskData) => {
    try {
      // In a real implementation, this would send the task data to the backend API
      // const response = await fetch('/api/v1/tasks', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(taskData),
      // });
      
      console.log('Creating task with data:', taskData);
      // Refresh the task list after successful creation
      // fetchTasks(); // This would be a function to refresh the task list
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  return (
    <div className="dashboard">
      <header>
        <h1>Advanced Task Manager</h1>
      </header>
      
      <main>
        <section className="task-creation">
          <h2>Create New Task</h2>
          <TaskForm onSubmit={handleTaskSubmit} />
        </section>
        
        <section className="task-list-section">
          <TaskList />
        </section>
      </main>
    </div>
  );
};

export default Dashboard;