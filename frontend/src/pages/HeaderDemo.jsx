import React from 'react';
import Header from '../components/Header';
import '../components/Header.css';

const HeaderDemo = () => {
  return (
    <div className="header-demo-container">
      <Header />
      <div style={{ maxWidth: '800px', margin: '0 auto', padding: '0 1rem' }}>
        <p style={{ fontSize: '1.2rem', color: '#333', lineHeight: '1.6' }}>
          This is a demonstration of the beautiful header for the Todo App with Arabic text.
          The main heading "السلام عليكم" (Assalamu Alaikum) is displayed in Arabic with a welcoming subheading.
        </p>
        <div style={{ marginTop: '2rem', padding: '1.5rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
          <h3 style={{ margin: '0 0 1rem', color: '#2c3e50' }}>Implementation Details:</h3>
          <ul style={{ textAlign: 'left', paddingLeft: '1.5rem' }}>
            <li>Main heading in Arabic: "السلام عليكم" (Assalamu Alaikum)</li>
            <li>Subheading in English: "Welcome to the Advanced Task Management Application!"</li>
            <li>Visually appealing design with centered layout</li>
            <li>Readable font with nice gradient colors</li>
            <li>Welcoming emoji/hand gesture included</li>
            <li>Responsive design that works on different screen sizes</li>
            <li>RTL (right-to-left) support for Arabic text</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default HeaderDemo;