function actorsList() {
  let actorsList = document.querySelector('#actors-list')
  const dropdown = document.querySelector('#genre-select')
  const textField = document.querySelector('#text-field')

  function eventListener(element, event) {
    element.addEventListener(event, () => {
      const formData = new FormData()
      formData.append('genre', dropdown.value)
      formData.append('name', textField.value)
      actorsList.innerHTML = ''
      fetch('api/filter-actors', {
        method: 'POST',
        body: formData
      }).then(response => response.json()).then(json => {
        console.log(json)
        for (let actor of json) {
          actorsList.appendChild(document.createElement('li')).innerHTML = actor.name
        }
      })
    })
  }

  eventListener(window, 'load')
  eventListener(dropdown, 'change')
  eventListener(textField, 'input')
}

actorsList()