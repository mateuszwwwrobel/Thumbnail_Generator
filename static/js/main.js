// Popup window for uploading images
$(document).ready(function () {
    $("#upload-image").click(function () {
        $('.ui.modal').modal('show');
    })
});


// Handling an '/images/' post endpoint.
document.querySelector('#fileUpload').addEventListener("submit",
    (event) => handleSubmit(), false);

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


// Handling an '/images/{dimensions}' get endpoint.
document.querySelector('#get-thumbnail').addEventListener("click",
    (event) => getThumbnail(), false);


async function getThumbnail(event) {
    let width = $("#width").val()
    let height = $("#height").val()
    let url_param = width + 'x' + height

    if (url_param === 'x'){
        document.getElementById('message').innerHTML = "Please enter dimensions."
            setTimeout(function () {
                document.getElementById("message").innerHTML = "";
            }, 4000);
        return;
    }

    await fetch('/images/' + url_param, {
        method: 'GET',
    }).then(response => response.json())
        .then(data => {
            if (data.img_url){
                document.getElementById('thumbnail-image').src = data.img_url
                document.getElementById('thumbnail-download').href = data.img_url
            }
            document.getElementById('message').innerHTML = data.message
            setTimeout(function () {
                document.getElementById("message").innerHTML = '';
            }, 4000);

        })
        .catch(error => {
            console.log(error)
        })
}

// Toggle create thumbnail

$("#get-thumbnail").click(function(){
    if ($("#width").val() === '' || $("#width").val() <= 0 ||
        $("#height").val() === '' || $("#height").val() <= 0
    ){
    }
    else{
        $("#thumbnail-container").show();
    }

});

