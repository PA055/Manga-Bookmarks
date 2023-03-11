import './App.css';
import React from 'react'

function CrawlSites() {

}

function LikeButton() {
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

function App() {
  return (
    <>
      <LikeButton />
      <LikeButton />
    </>
  )
}
 
}

export default App;
