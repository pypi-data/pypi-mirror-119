/* Javascript for PrismXBlock. */
function PrismXBlock(runtime, element) {


    var lngSelect = $(element).find('#language').get(0);
    var thmSelect = $(element).find('#theme').get(0);

    var codeMirror = CodeMirror.fromTextArea(document.querySelectorAll('textarea#code-textarea')[0], {
        lineNumbers: true,
        indentWithTabs: true,
        matchBrackets: true,
        lineWrapping: true
    });

    $(element).find('.save-button').bind('click', function(){
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');

        var data = {
            display_name: $(element).find('input[name=display_name]').val(),
            code_data: codeMirror.getValue(),
            language: lngSelect.options[lngSelect.selectedIndex].value,
            theme: thmSelect.options[thmSelect.selectedIndex].value,
            maxheight: $(element).find('input[name=maxheight]').val(),

        };
        runtime.notify('save', {state: 'start'});

        $.ajax({
            url: handlerUrl,
            type: 'POST',
            data: JSON.stringify(data),
        }).done(function(response) {
            window.location.reload();
        });
    });

    $(element).find('.cancel-button').bind('click', function() {
        runtime.notify('cancel', {});
    });
}
