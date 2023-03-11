function AddBookmark() {
    var formData = new FormData(document.querySelector('form'))
    alert(formData.get('mname'))
}