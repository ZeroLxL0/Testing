document.addEventListener('DOMContentLoaded', function() {
        const rows = document.querySelectorAll('table tbody tr');
        const currentDate = new Date();

        rows.forEach(row => {
            const fechaActuaCell = row.querySelector('input[name="fecha_actua"]');
            const fechaActua = new Date(fechaActuaCell.value);

            const diffTime = Math.abs(currentDate - fechaActua);
            const diffMonths = diffTime / (1000 * 60 * 60 * 24 * 30);

            if (diffMonths > 2) {
                row.classList.add('highlight');
            }
        });
    });