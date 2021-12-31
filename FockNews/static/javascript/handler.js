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
                if (data.column_num === 0) {
                    alert("Ошибка. Статья не была удалена!");
                }
                location.reload();
            }

        });
    }


    function restoreArticle(event) {
        $.ajax ({
            url: window.location.pathname + 'restore/',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            method: 'POST',
            beforeSend: function() {
                $("#btn-restorearticle").hide();
            },
            success: function(data) {
                if (data.column_num === 0) {
                    alert("Ошибка. Статья не была восстановлена!");
                }
                location.reload();
            }

        });
    }


    function publishArticle(event) {
        $.ajax ({
            url: window.location.pathname + 'publish/',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            method: 'POST',
            beforeSend: function() {
                $("#btn-publisharticle").hide();
            },
            success: function(data) {
                if (data.column_num === 0) {
                    alert("Ошибка. Статья не была восстановлена!");
                }
                location.reload();
            }

        });
    }

    function saveEditedArticle(event) {
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
                if (data.column_num === 0) {
                    alert("Ошибка. Статья не была сохранена!");
                }
                location.href = ".."
            },
            error: function(data) {
                alert("Ошибка!");
            }

        });
    }

    function upRate(event) {
        $.ajax ({
            url: window.location.pathname + 'uprate/',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            method: 'POST',
            beforeSend: function() {
                $("#btn-upRate").hide();
            },
            success: function(data) {
                if (data.column_num === 0) {
                    alert("Ошибка. Изменить рейтинг не удалось!");
                }
                location.reload();
                $("#btn-upRate").show();
                alert("Рейтинг поднят!")
            },
            error: function(data) {
                alert("Ошибка!");
                $("#btn-upRate").show();
            }

        });
    }

    function downRate(event) {
        $.ajax ({
            url: window.location.pathname + 'downrate/',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            method: 'POST',
            beforeSend: function() {
                $("#btn-downRate").hide();
            },
            success: function(data) {
                if (data.column_num  === 0) {
                    alert("Ошибка. Изменить рейтинг не удалось!");
                }
                location.reload();
                $("#btn-downRate").show();
                alert("Рейтинг опущен!")
            },
            error: function(data) {
                alert("Ошибка!");
                $("#btn-downRate").show();
            }

        });
    }

    $("#btn-deletearticle").bind("click", delArticle);
    $("#btn-restorearticle").bind("click", restoreArticle);
    $("#btn-publisharticle").bind("click", publishArticle);
    $("#btn-saveeditarticle").bind("click", saveEditedArticle);
    $("#btn-uprating").bind("click", upRate);
    $("#btn-downrating").bind("click", downRate);
});
