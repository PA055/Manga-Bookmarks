let bookmarks = document.getElementById('bookmarks');

const fetchJson = async () => {
    try {
      const file = await fetch("./bookmarks.json");
      const response = await file.json();
      var data = JSON.parse(response)
    } catch (error) {
      console.log(error);
    }
};
console.log(data)

function AddBookmark() {
    var formData = new FormData(document.querySelector('form'))
    
}