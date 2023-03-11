let bookmarks = document.getElementById('bookmarks');

const fetchJson = async () => {
    try {
      const file = await fetch("./bookmarks.json");
      const response = await file.json();
    } catch (error) {
      console.log(error);
    }
    var data = JSON.parse(response)
    console.log(data)
};

console.log(fetchJson.data)

function AddBookmark() {
    var formData = new FormData(document.querySelector('form'))
    
}