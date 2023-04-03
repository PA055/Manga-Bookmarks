
const getHTML = async (url) => {
    const ifr = document.createElement('iframe')
    ifr.src = url
    // ifr.display = none
    document.body.appendChild(ifr)
    ifr.addEventListener( "load", function(e) {
        var html = ifr.contentWindow.document.body.innerHTML;
        console.log(html)
    })
    
};

const fetchJson = async (url) => {
    try {
        const file = await fetch(url);
        const data = await file.json();
        
        return data

    } catch (error) {
        console.log(error);
    }
};

var data = fetchJson("./bookmarks.json");
data.then(function(d) {if (document.getElementById("bookmarks")) {createBookmarks(d)}})

function createBookmarks(data) {
    data.forEach(object => {
        parseWebsite(object)
        console.log(object)
    });
    data.forEach(object => {
        createBookmark(object);
    });
}

function parseWebsite(object) {
    var html = getHTML(object.link)
    console.log(html)
}


function createBookmark(object) {
    const parent = document.getElementById('bookmarks-ul')
    const li = document.createElement("li")
    const a = document.createElement("a")
    const title_div = document.createElement('div')
    const last = document.createElement('div')
    const lnode = document.createTextNode('Last Read: Chapter ' + object.chapter)
    const title = document.createElement('h3')
    const tnode = document.createTextNode(object.mname)
    const para = document.createElement('p')
    const pnode = document.createTextNode('Latest Chapter: Chapter ' + object.latest)

    parent.appendChild(li)
    li.appendChild(a)
    a.appendChild(title_div)
    title_div.appendChild(title)
    title.appendChild(tnode)
    title_div.appendChild(para)
    para.appendChild(pnode)
    a.appendChild(last)
    last.appendChild(lnode)

    li.classList.add("bookmark")
    a.classList.add('clearfix')
    a.href = object.latest_link
    a.target = "_blank"
    title_div.classList.add('title-div')
    title.classList.add('title')
    para.classList.add('latest')
    last.classList.add('last')
    if (object.latest > object.chapter) {
        title_div.classList.add('new-chapter')
    }

}

function AddBookmark() {
    var formData = new FormData(document.querySelector('form'));
    var existingData = fetchJson("./bookmarks.json");
    alert('1')
    existingData.then(function(d){
        var data = {mname: formData.get("mname"), link: formData.get('link'), chapter: formData.get('chapter')}
        alert('2')
        console.log(d)
        console.log(data)
        alert('3')
        d.append(data)
        alert('4')
        console.log(d)
        alert('d')
    })
    
}