const url = "./bookmarks.json"

const fetchJson = async () => {
    try {
        const file = await fetch(url);
        const response = await file.json();

        console.log(response[0].link)
        createBookmarks(response);

    } catch (error) {
        console.log(error);
    }
};

fetchJson();

function createBookmarks(data) {
    document.getElementById('bookmarks').getElementsByTagName('ul');
}

function AddBookmark() {
    var formData = new FormData(document.querySelector('form'))
    console.log(formData)
    console.log(formData.get("mname") + ', ' + formData.get("link"))

}