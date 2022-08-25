function genreDataGenerator() {
    let genreSpans = document.querySelectorAll('span')
    for (let genreSpan of genreSpans) {
        genreSpan.addEventListener('click', (e) => {
            fetch(e.target.getAttribute('data-link'))
                .then(response => response.json())
                .then(json => {
                    console.log(json)
                    const tableBody = document.querySelector('tbody')
                    tableBody.innerHTML = ''
                    for (let row of json) {
                        let tableRow = document.createElement('tr')
                        tableBody.appendChild(tableRow)
                        let td = document.createElement('td')
                        td.textContent = row.title
                        tableRow.appendChild(td)
                        td = document.createElement('td')
                        td.textContent = row.rating
                        tableRow.appendChild(td)
                        td = document.createElement('td')
                        td.textContent = row.year
                        tableRow.appendChild(td)
                        td = document.createElement('td')
                        td.textContent = e.target.getAttribute('data-genre-name')
                        tableRow.appendChild(td)
                        td = document.createElement('td')
                        td.textContent = row.actors_count
                        tableRow.appendChild(td)
                    }
                })
        })
    }
}

genreDataGenerator()










