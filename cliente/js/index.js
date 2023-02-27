$(document).ready(function(){
});


function obtenerPalabra(){
    var palabra = document.getElementById('inputBusqueda').value.trim().toLowerCase();
    console.log(palabra)
    obtenerEnlaces(palabra);
}

function obtenerEnlaces(palabra){
    $.ajax(
        {
        type:"GET",
        datatype:"json",
        url: "http://127.0.0.1:3000/api/get-documents?palabra=" + palabra,
        success: function(data){
            console.log(data);
            mostrarEnlaces(data);
        }
        }
    )
}

function mostrarEnlaces(data){
    let contenido = "";

    if(data.length>0){
        $.each(data, function(index, currentDocument){
            contenido += '<a href="' +currentDocument.url + '">' +currentDocument.titulo +'</a> <br> <p>'+ currentDocument.contenido +'</p>'
        });
        $("#contenedorEnlaces").html(contenido);
    }
    else{
        contenido = '<h3 style="margin-left: auto; margin-right: auto;">Lo sentimos, no se ha encontrado resultados :(</h3>';
        $("#contenedorEnlaces").html(contenido);
    }

}