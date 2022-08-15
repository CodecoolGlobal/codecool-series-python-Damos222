const actors = document.querySelectorAll('.actor')
for (let actor of actors) {
    actor.addEventListener('click', (e) => {
        fetch(e.target.getAttribute('data-link'))
            .then(response => response.json())
            .then(json => {
                if (e.target.children.length == 0) {
                    let currentlyOpen = document.querySelector('.roles')
                    if (currentlyOpen) {
                        currentlyOpen.parentNode.removeChild(currentlyOpen)
                    }
                    let roles = e.target.appendChild(document.createElement('ul'))
                    roles.classList.add('roles')
                    for (let item of json) {
                        let role = roles.appendChild(document.createElement('li'))
                        role.textContent = item['character_name'] + ' in ' + item['title']
                    }} else {
                    e.target.removeChild(document.querySelector('.roles'))
                }
            })
    })
}