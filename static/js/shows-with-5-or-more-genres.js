function showShowDetails() {
    const select = document.querySelector('#shows-select')
    select.addEventListener('change', (e) => {
        let showId = select.value
        document.querySelector('#table-body').innerHTML = ''
        if (showId === 'not-selected') {
            return
        }
        fetch(`/api/shows-with-5-or-more-genres/${showId}`)
            .then((response) => response.json())
            .then(json => {
                for (let row of json) {
                    const tableBody = document.querySelector('#table-body')
                    let tr = document.createElement('tr')
                    tableBody.appendChild(tr)
                    let td = document.createElement('td')
                    td.textContent = row.year
                    tr.appendChild(td)
                    td = document.createElement('td')
                    td.textContent = row.anniversary_year
                    tr.appendChild(td)
                    td = document.createElement('td')
                    td.textContent = row.seasons_count
                    tr.appendChild(td)
                    td = document.createElement('td')
                    let rating = '*'.repeat(row.rating)
                    td.textContent = rating
                    tr.appendChild(td)
                }
            })
    })
}

showShowDetails()