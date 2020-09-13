$(document).ready(function () {
     // CSRF code
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');


    function delArticle(event) {
        $.ajax ({
            url: window.location.pathname + 'delete/',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            method: 'POST',
            beforeSend: function() {
                $("#btn-deletearticle").hide();
            },
            success: function(data) {
                if (data.column_num == 0) {
                    alert("Ошибка. Статья не была удалена!");
                }
                location.reload();
            }

        });
    }

    function saveEditedArticle(event) {
        alert($("#title-input").val() + "\n" + $("#body-input").val() + "\n" + $("#tags-input").val());
        $.ajax ({
            url: window.location.pathname + 'save/',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'title': $("#title-input").val(),
                'body': $("#body-input").val(),
                'tags': $("#tags-input").val()
            },
            method: 'POST',
            beforeSend: function() {
                $("#btn-saveeditarticle").hide();
            },
            success: function(data) {
                if (data.column_num == 0) {
                    alert("Ошибка. Статья не была сохранена!");
                }
                location.href = ".."
            },
            error: function(data) {
                alert("Ошибка!");
            }

        });
    }

    $("#btn-deletearticle").bind("click", delArticle);
    $("#btn-saveeditarticle").bind("click", saveEditedArticle);
});
