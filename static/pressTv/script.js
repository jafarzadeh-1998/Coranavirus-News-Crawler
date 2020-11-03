function fillNews(newsData){
    news += ""
    for (let index = 0; index < newsData.length; index++)
        news += "" +newsData[index].pubdate + "</br>"+
            "<a href='" + newsData[index].link +"'>" + newsData[index].title + " </a></br>"+
            newsData[index].summary + "<hr>";
    return news
}

function getNews(pageNum) {
    $.ajax({
        method: 'GET',
        url: "/pressTv/change_news_page/"+pageNum,
        dataType: 'json',
        data: {},
        success: function (data) {
        $(".news_list").html(fillNews(data.news));
        },
        error: function (data) {
            console.log(data);
        },
    });
}


$('.nextPage').click(function(){
    console.log("FUCK");
    let pageNum = $(".pageNumber").val();
    $(".pageNumber").attr('value', parseInt(pageNum, 10)+1);
    getNews($(".pageNumber").val());
});

$('.PrevPage').click(function(){
    let pageNum = $(".pageNumber").val();
    if (pageNum != 0)
        $(".pageNumber").attr('value', parseInt(pageNum, 10)-1);
    getNews($(".pageNumber").val());
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
