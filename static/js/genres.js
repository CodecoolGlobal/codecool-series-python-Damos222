let tableBody = document.querySelector('tbody')


let genreSpans = document.querySelectorAll('span')
for (let genreSpan of genreSpans) {
    genreSpan.addEventListener('click', (e) => {
        fetch(e.target.getAttribute('data-link'))
            .then(response => response.json())
            .then(json => console.log(json))
    })
}









