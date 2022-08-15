async function embedYtVideo() {
    let videoContainer = document.querySelector('#video-container')
    await fetch('https://www.youtube.com/oembed?url=' + videoContainer.innerHTML)
        .then(res => res.json())
        .then(json => json.html)
        .then(html => videoContainer.innerHTML = html)
    console.log(videoContainer.innerHTML)
}
embedYtVideo()
