function toggleMenu(id) {
    let menu = document.getElementById('menu-' + id.toString());
    menu.classList.toggle('hidden');
}

function updateBookmarkRead(bookmark) {
    fetch('/read/' + bookmark.id.toString(), {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "latest": bookmark.latest })
    })
    bookmarks_container = document.getElementById('bookmarks-ul');
    bookmark_container = document.getElementById('bookmark-' + bookmark.id.toString());
    bookmarks_container.append(bookmark_container);
    bookmark_container.getElementsByTagName('a')[0].href = bookmark.link;
    bookmark_container.getElementsByClassName('new-chapter')[0].classList.remove('new-chapter');
    bookmark_container.getElementsByClassName('chapter')[0].innerHTML = 'Last Read: ' + bookmark.latest.toString();
}

function FilterBookmarks() {
    const input = document.getElementById('bookmarks-search');
    const filterValue = input.value.toUpperCase();
    const ul = document.getElementById('bookmarks-ul');
    const li = ul.getElementsByTagName('li');

    for (let i = 0; i < li.length; i++) {
        title = li[i].getElementsByClassName('title')[0]
        txtValue = title.innerText;
        if (txtValue.toUpperCase().indexOf(filterValue) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function createBookmark(bookmark) {
    const parent = document.getElementById('bookmarks-ul')
    const li = document.createElement("li")
    const a = document.createElement("a")
    const title_div = document.createElement('div')
    const title = document.createElement('h3')
    const tnode = document.createTextNode(bookmark.mname)
    const para = document.createElement('p')
    const pnode = document.createTextNode('Latest Chapter: Chapter ' + bookmark.latest)
    const last = document.createElement('div')
    const last_chapter = document.createElement('span')
    const lnode = document.createTextNode('Last Read: Chapter ' + bookmark.chapter)
    const settings_toggle = document.createElement('button')
    const settings_text = document.createTextNode('≡')
    const settings = document.createElement('div')
    const delete_button = document.createElement('a')
    const delete_text = document.createTextNode('Delete')
    const edit_button = document.createElement('a')
    const edit_text = document.createTextNode('Edit')

    parent.appendChild(li)
    li.appendChild(a)
    a.appendChild(title_div)
    title_div.appendChild(title)
    title.appendChild(tnode)
    title_div.appendChild(para)
    para.appendChild(pnode)
    a.appendChild(last)
    last.appendChild(last_chapter)
    last_chapter.appendChild(lnode)
    li.appendChild(settings_toggle)
    settings_toggle.appendChild(settings_text)
    li.appendChild(settings)
    settings.appendChild(delete_button)
    delete_button.appendChild(delete_text)
    settings.appendChild(edit_button)
    edit_button.appendChild(edit_text)

    li.classList.add("bookmark")
    li.classList.add("clearfix")
    li.id = "bookmark-" + bookmark.id.toString()
    a.classList.add('clearfix')
    a.addEventListener('click', () => { updateBookmarkRead(bookmark); return false; })
    a.href = bookmark.latest_link
    a.target = "_blank"
    title_div.classList.add('title-div')
    title.classList.add('title')
    para.classList.add('latest')
    last.classList.add('last')
    last_chapter.classList.add('chapter')
    settings_toggle.classList.add('menu-toggle')
    settings_toggle.addEventListener('click', () => {
        toggleMenu(bookmark.id);
        return false;
    });
    settings.classList.add('menu')
    settings.classList.add('hidden')
    settings.id = 'menu-' + bookmark.id.toString()
    delete_button.classList.add('settings')
    delete_button.href = '/delete/' + bookmark.id.toString()
    edit_button.classList.add('settings')
    edit_button.href = '/edit/' + bookmark.id.toString()

    if (bookmark.latest > bookmark.chapter) {
        title_div.classList.add('new-chapter')
    }



}


async function getBookmarks(api_url) {
    let bookmarks = await fetch(api_url)
    let json = await bookmarks.json()
    console.log(json)
    json.sort((a, b) => b.num_new_chapters - a.num_new_chapters)
    json.forEach(bookmark => {
        createBookmark(bookmark)
    });
    document.getElementById('loading').style.display = 'none'
}

getBookmarks('/api/all')
// createBookmark({id: 8, mname: "FFF Class Trashhero", link: "https://manga4life.com/manga/FFF-Class-Trashero", chapter: 142, latest: 145, latest_link: "https://manga4life.com/read-online/FFF-Class-Trashero-chapter-143-page-1.html", num_new_chapters: 3})
// document.getElementById('loading').style.display = 'none'

