/**
 * Created by pf on 17-6-1.
 */
function choiceCate(docu) {
    $('#arti_category').text(docu.text())
}
function ajaxPost(url, data) {
    $.ajax({
        url: url,
        data: data,
        type: 'post',
        dataType: 'json',
        beforeSend: function (xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (success) {
            console.log(success);
            console.log("success打印日志："+success['data']);
        },
        complete: function () {
            console.log("complete打印日志：")
        },
        error: function (er) {
            console.log("error打印日志：");
            console.log(er.status)
        }
    });
}

function delHtmlTag(str) {
    return str.replace(/<[^>]+>/g, "");//去掉所有的html标记
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
