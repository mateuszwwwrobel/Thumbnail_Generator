// Popup window for uploading images
$(document).ready(function () {
    $("#upload-image").click(function () {
        $('.ui.modal').modal('show');
    })
});



// // Instructions for handling an '/images' endpoint.
document.querySelector('#fileUpload').addEventListener("submit", (event) => handleSubmit(), false);

async function handleSubmit(event) {
    let files = event.target.files
    let formData = new FormData()
    formData.append('myFile', files[0])

    await fetch('/images/', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
        .catch(error => {
            console.error(error)
        })
}
