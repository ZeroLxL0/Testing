


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('device-form');
    const successMessage = document.getElementById('success-message');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Evita que el formulario se envíe inmediatamente
        successMessage.style.display = 'block';
        // Aquí puedes añadir lógica para enviar el formulario usando AJAX si lo deseas
        // Si no, puedes eliminar el preventDefault y esto enviará el formulario normalmente.
    });
});