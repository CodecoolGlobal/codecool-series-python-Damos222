function getShowsOnRightClick() {
    const characters = document.querySelectorAll('.character')
    console.log(characters)
    for (let character of characters) {
        character.addEventListener('contextmenu', (e) => {
            e.preventDefault()
            character.innerHTML = character.getAttribute('data-character-name')
            let characterItem = e.currentTarget
            let showspan = document.createElement('span')
            let shows = e.currentTarget.getAttribute('data-shows').replace('[', '(').replace(']', ')')
            shows.replaceAll(/'/g, '')
            shows.replaceAll(/,/g, ', ')
            showspan.textContent = shows
            characterItem.appendChild(showspan)
        })
    }
}

function goToYoutubeOnLeftClick() {
    const characters = document.querySelectorAll('.character')
    console.log(characters)
    for (let character of characters) {
        character.addEventListener('click', (e) => {
            e.preventDefault()
            let name = character.getAttribute('data-character-name')
            window.open(`https://youtube.com/results?search_query=${name}`, '_blank');
        })
    }
}

getShowsOnRightClick()
goToYoutubeOnLeftClick()