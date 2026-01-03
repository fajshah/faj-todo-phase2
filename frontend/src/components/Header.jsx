import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="todo-header">
      <div className="header-content">
        <h1 className="main-heading">السلام عليكم</h1>
        <h2 className="sub-heading">Welcome to the Advanced Task Management Application!</h2>
        <div className="welcome-icon">👋</div>
      </div>
    </header>
  );
};

export default Header;