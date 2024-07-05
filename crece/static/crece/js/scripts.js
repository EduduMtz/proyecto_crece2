$(document).ready(function() {
    let conversations = [];
    // Usa currentUser directamente, ya que se definió en la plantilla
    let editingConversationId = null;

    function renderConversations() {
        $('#conversation-list').empty();
        $('.chat').empty();
        conversations.forEach(convo => {
            let modifiedInfo = convo.modified ? `<br>Modificado el: ${convo.modified}` : '';
            $('#conversation-list').append(`<li data-chat="${convo.id}">${convo.title}</li>`);
            $('.chat').append(`
                <div id="chat-${convo.id}" class="chat-window">
                    <div class="chat-header">
                        <p>
                            Usuario: @${currentUser}<br>
                            Creado el: ${convo.created}${modifiedInfo}<br>
                            Título: ${convo.title}
                        </p>
                    </div>
                    <div class="messages">
                        <div class="message">
                            <p>${convo.message}</p>
                        </div>
                    </div>
                    <div class="input-area">
                        <div id="texto-respuesta">
                            <input type="text" id="input-${convo.id}" placeholder="Escribe un mensaje..." maxlength="650">
                            <span class="char-count-input">0 / 650 caracteres</span>
                        </div>
                        <button data-chat="${convo.id}">Enviar</button>
                    </div>
                </div>
            `);

            // Render existing responses
            convo.responses.forEach(response => {
                let responseElement = $(`
                    <div class="message">
                        <p>
                            Usuario: @${response.user}${response.isAuthor ? " (autor)" : ""}<br>
                            Enviado el: ${response.dateTime}
                        </p>
                        <div class="divider"></div>
                        <p>${response.message}</p>
                    </div>
                `);
                $('#chat-' + convo.id + ' .messages').append(responseElement);
            });

            // Add event listener for character count
            $('#input-' + convo.id).on('input', function() {
                var maxLength = $(this).attr('maxlength');
                var currentLength = $(this).val().length;
                $(this).next('.char-count-input').text(currentLength + ' / ' + maxLength + ' caracteres');
            });
        });
    }

    function openModal(title) {
        $('#modal-title').text(title);
        $('#modal').show();
    }

    function closeModal() {
        $('#modal').hide();
        $('#title').val('');
        $('#message').val('');
        $('#char-count-modal').text('0 / 650 caracteres');
        editingConversationId = null;
    }

    $('.sidebar').on('click', 'li', function() {
        var chatId = $(this).data('chat');
        $('.chat-window').hide();
        $('#chat-' + chatId).show();
        $('#edit-message').show();
    });

    $('.chat').on('click', '.input-area button', function() {
        var chatId = $(this).data('chat');
        var input = $('#input-' + chatId);
        var message = input.val().trim();
        var dateTime = new Date();
        var formattedDate = dateTime.toLocaleDateString();
        var formattedTime = dateTime.toLocaleTimeString();

        if (message) {
            var convo = conversations.find(c => c.id == chatId);
            var isAuthor = currentUser === convo.user ? " (autor)" : "";
            convo.responses.push({
                user: currentUser,
                message: message,
                dateTime: formattedDate + ' ' + formattedTime,
                isAuthor: currentUser === convo.user
            });

            var messageElement = $(`
                <div class="message">
                    <p>
                        Usuario: @${currentUser}${isAuthor}<br>
                        Enviado el: ${formattedDate} ${formattedTime}
                    </p>
                    <div class="divider"></div>
                    <p>${message}</p>
                </div>
            `);
            $('#chat-' + chatId + ' .messages').append(messageElement);
            input.val('');
            $('#chat-' + chatId + ' .messages').scrollTop($('#chat-' + chatId + ' .messages')[0].scrollHeight);
            input.next('.char-count-input').text('0 / 650 caracteres'); // Reset character count
        }
    });

    $('#create-conversation').click(function() {
        openModal('Crear Conversación');
    });

    $('#edit-message').click(function() {
        var activeChat = $('.chat-window:visible');
        var chatId = activeChat.attr('id').split('-')[1];
        var convo = conversations.find(c => c.id == chatId);
        editingConversationId = chatId;
        $('#title').val(convo.title);
        $('#message').val(convo.message);
        $('#char-count-modal').text(convo.message.length + ' / 650 caracteres'); // Update character count
        openModal('Editar Mensaje');
    });

    $('#modal .close').click(function() {
        closeModal();
    });

    $('#conversation-form').submit(function(e) {
        e.preventDefault();
        var title = $('#title').val().trim();
        var message = $('#message').val().trim();
        var dateTime = new Date();
        var formattedDate = dateTime.toLocaleDateString();
        var formattedTime = dateTime.toLocaleTimeString();

        if (editingConversationId) {
            var convo = conversations.find(c => c.id == editingConversationId);
            convo.title = title;
            convo.message = message;
            convo.modified = formattedDate + ' ' + formattedTime;
        } else {
            var newConvo = {
                id: conversations.length + 1,
                user: currentUser,
                title: title,
                message: message,
                created: formattedDate,
                responses: []
            };
            conversations.push(newConvo);
        }

        renderConversations();
        closeModal();
    });

    // Initial render
    renderConversations();

    // Character count for modal message
    $('#message').on('input', function() {
        var maxLength = $(this).attr('maxlength');
        var currentLength = $(this).val().length;
        $('#char-count-modal').text(currentLength + ' / ' + maxLength + ' caracteres');
    });
});
