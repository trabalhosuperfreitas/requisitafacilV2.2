// Exibe ou oculta o campo setor no admin conforme o papel selecionado
(function($) {
    $(document).ready(function() {
        function toggleSectorField() {
            var role = $('#id_role').val();
            if (role === 'Almoxarife') {
                $('#id_sector').closest('.form-row, .form-group, .field-sector').hide();
            } else {
                $('#id_sector').closest('.form-row, .form-group, .field-sector').show();
            }
        }
        toggleSectorField();
        $('#id_role').change(toggleSectorField);
    });
})(django.jQuery);
