import './App.css';
import React from 'react'

function App() {
  const [liked, setLiked] = React.useState(false);
  if (liked){
    return (
      <div>
        <button onClick={() => setLiked(false)}>Unlike</button>
        <p>You liked this</p>
      </div>
    );
  }
  return (
    <button onClick={() => setLiked(true)}>Like</button>
  );
}

export default App;
