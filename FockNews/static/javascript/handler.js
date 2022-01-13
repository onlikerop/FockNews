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


    // transit-info functions

        // Comments report
    $(".btn-report-comment").bind("click", function (event) {
        let group = event.currentTarget.getAttribute('data-bs-comment-user-group')
        let user = event.currentTarget.getAttribute('data-bs-comment-user')
        let comment = event.currentTarget.getAttribute('data-bs-comment-comment')
        $("#commrep-title").addClass(group)
        $("#commrep-title").text(user)
        $("#commrep-body").text(comment)
    })
        // Comments report modal hide event trigger
    $("#reportCommentModal").on('hide.bs.modal', function () {
       setTimeout(function (){
           $("#commrep-title").attr('class', 'card-title')
       }, 100
       )
    });


    // basic functions
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
            },
            error: function(data) {
                alert("Ошибка!");
                $("#btn-downRate").show();
            }

        });
    }

    function reportArticle(event) {
        $.ajax ({
            url: window.location.pathname + 'reportarticle/',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'type': $("#reportArticleTypes").val(),
                'comment': $("#report-input").val()
            },
            method: 'POST',
            beforeSend: function() {
                $("#"+event.currentTarget.id).hide();
                if ($("#reportArticleTypes").val() === null) {
                    alert("Выберите тип жалобы!")
                    $("#"+event.currentTarget.id).show();
                    return false
                }
            },
            success: function(data) {
                if (data.column_num  === 0) {
                    alert("Ошибка. Отправить жалобу не удалось!");
                }
                alert("Жалоба отправлена");
                location.reload();
                $("#"+event.currentTarget.id).show();
                $('#reportArticleModal').modal('hide');
            },
            error: function(data) {
                alert("Ошибка!");
                $("#"+event.currentTarget.id).show();
                $('#reportArticleModal').modal('hide');
            }

        });
    }

    function delComment(event) {
        $.ajax ({
            url: window.location.pathname + 'delcomm/' + event.currentTarget.id.split("btn-deletecomment-")[1] + '/',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            method: 'POST',
            beforeSend: function() {
                $("#"+event.currentTarget.id).hide();
            },
            success: function(data) {
                if (data.column_num === 0) {
                    alert("Ошибка. Комментарий не был удалён!");
                }
                location.reload();
            }

        });
    }

    function resComment(event) {
        $.ajax ({
            url: window.location.pathname + 'rescomm/' + event.currentTarget.id.split("btn-restorecomment-")[1] + '/',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            method: 'POST',
            beforeSend: function() {
                $("#"+event.currentTarget.id).hide();
            },
            success: function(data) {
                if (data.column_num === 0) {
                    alert("Ошибка. Комментарий не был восстановлен!");
                }
                location.reload();
            }

        });
    }

    function upRateComm(event) {
        $.ajax ({
            url: window.location.pathname + 'upratecomm/' + event.currentTarget.id.split("btn-uprate-comm-")[1] + '/',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            method: 'POST',
            beforeSend: function() {
                $("#"+event.currentTarget.id).hide();
            },
            success: function(data) {
                if (data.column_num === 0) {
                    alert("Ошибка. Изменить рейтинг не удалось!");
                }
                location.reload();
                $("#"+event.currentTarget.id).show();
            },
            error: function(data) {
                alert("Ошибка!");
                $("#"+event.currentTarget.id).show();
            }

        });
    }

    function downRateComm(event) {
        $.ajax ({
            url: window.location.pathname + 'downratecomm/' + event.currentTarget.id.split("btn-downrate-comm-")[1] + '/',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            method: 'POST',
            beforeSend: function() {
                $(event.currentTarget.id).hide();
            },
            success: function(data) {
                if (data.column_num  === 0) {
                    alert("Ошибка. Изменить рейтинг не удалось!");
                }
                location.reload();
                $(event.currentTarget.id).show();
            },
            error: function(data) {
                alert("Ошибка!");
                $(event.currentTarget.id).show();
            }

        });
    }

    function sortComm(event) {
        $.ajax ({
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            method: 'POST',
            beforeSend: function() {
                $("#"+event.currentTarget.id).hide();
            },
            success: function(data) {
                if (data.column_num  === 0) {
                    alert("Ошибка. Отсортировать не удалось!");
                }
                $("#"+event.currentTarget.id).show();
                location.href = '?sort=' + event.currentTarget.value;
            },
            error: function(data) {
                alert("Ошибка!");
                $("#"+event.currentTarget.id).show();
            }

        });
    }

    // basic binds
    $("#btn-deletearticle").bind("click", delArticle);
    $("#btn-restorearticle").bind("click", restoreArticle);
    $("#btn-publisharticle").bind("click", publishArticle);
    $("#btn-saveeditarticle").bind("click", saveEditedArticle);
    $("#btn-uprate-article").bind("click", upRate);
    $("#btn-downrate-article").bind("click", downRate);
    $(".delete-comment").bind("click", delComment);
    $(".restore-comment").bind("click", resComment);
    $(".btn-uprate-comm").bind("click", upRateComm);
    $(".btn-downrate-comm").bind("click", downRateComm);
    $("#comments-sort").bind("change", sortComm);
    $("#btn-send-report").bind("click", reportArticle)
});
