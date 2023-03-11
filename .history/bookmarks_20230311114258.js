let bookmarks = document.getElementById('bookmarks');
const url = "./bookmarks.json"

$.getJSON(url, function(data){
    console.log(data);
});

// const fetchJson = async () => {
//     try {
//         const file = await fetch(url);
//         const response = await file.json();
//     } catch (error) {
//         console.log(error);
//     }
// };

function AddBookmark() {
    var formData = new FormData(document.querySelector('form'))
    
}