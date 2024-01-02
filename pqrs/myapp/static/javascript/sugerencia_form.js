
$(document).ready(function() {
    $('#buscarBtn').on('click', function() {
        var cedula = $('#id_cedula_input').val();

        // Realizar solicitud AJAX al servidor para buscar la cédula del usuario
        $.ajax({
            url: '/buscar-por-cedula/' + cedula + '/',  // Ajusta la URL según tu configuración
            method: 'GET',
            success: function(response) {
                // Actualizar el valor del campo de cédula después de la búsqueda
                $('#id_cedula_input').val(response.cedula);
                
                // Mostrar el nombre y el área del usuario
                $('#nombre_usuario').val(response.nombre_usuario);
                $('#area_usuario').val(response.area_usuario);
                $('#info_usuario').show();
            },
            error: function(error) {
                console.error('Error en la búsqueda:', error);
            }
        });
    });
});
