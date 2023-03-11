import logo from './logo.svg';
import './App.css';

function App() {
  const setLiked = false
  return (
    <button onClick={() => setLiked(true)}>Like</button>
  );
}

export default App;
