import React from 'react';

function AppTest() {
  return (
    <div style={{ padding: '20px', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
      <h1 style={{ color: '#000' }}>Test App - If you see this, React is working!</h1>
      <p>Current Time: {new Date().toLocaleTimeString()}</p>
      <button onClick={() => alert('Button clicked!')}>Click Me</button>
    </div>
  );
}

export default AppTest;
