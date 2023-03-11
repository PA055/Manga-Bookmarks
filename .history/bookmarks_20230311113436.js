import data from "./bookmarks.json" assert { type: "json" };
let bookmarks = document.getElementById('bookmarks');
console.log(data)

function AddBookmark() {
    var formData = new FormData(document.querySelector('form'))
    
}