let bookmarks = document.getElementById('bookmarks');

const fetchJson = async () => {
    try {
        const file = await fetch("./bookmarks.json");
        const response = await file.json();
        const data = JSON.parse(response)
        console.log(data)
    } catch (error) {
        console.log(error);
    }
};

console.log(fetchJson())

function AddBookmark() {
    var formData = new FormData(document.querySelector('form'))
    
}