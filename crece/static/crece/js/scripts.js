$(document).ready(function() {
    console.log("JavaScript is loaded and running.");

    $('#new-conversation').click(function() {
        console.log("Button clicked");
        $('#newPostModal').modal('show');
    });

    $('#newPostModal .btn-close').click(function() {
        console.log("Modal close button clicked");
        $('#newPostModal').modal('hide');
    });

    $('#conversation-form').submit(function(e) {
        e.preventDefault();
        var title = $('#title').val().trim();
        var message = $('#message').val().trim();

        if (title && message) {
            $.post("{% url 'post_new' %}", {
                title: title,
                content: message,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            }).done(function(data) {
                if (data.success) {
                    var newConvo = `
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5 class="card-title">${data.title}</h5>
                                <p class="card-text">${data.content}</p>
                                <a href="/post/${data.post_id}/" class="btn btn-secondary">Ver más</a>
                            </div>
                        </div>
                    `;
                    $('#conversation-list').prepend(newConvo);
                    $('#newPostModal').modal('hide');
                    $('#conversation-form')[0].reset();  // Limpiar el formulario
                    $('#char-count-modal').text('0 / 650 caracteres');  // Restablecer el contador de caracteres
                }
            });
        }
    });

    $('#message').on('input', function() {
        var maxLength = $(this).attr('maxlength');
        var currentLength = $(this).val().length;
        $('#char-count-modal').text(currentLength + ' / ' + maxLength + ' caracteres');
    });
});
