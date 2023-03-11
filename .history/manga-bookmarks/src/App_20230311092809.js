import './App.css';
import React from 'react'

function App() {
  const [liked, setLiked] = React.useState(false);
  if (liked){
  
  }
  return (
    <button onClick={() => setLiked(true)}>Like</button>
  );
}

export default App;
