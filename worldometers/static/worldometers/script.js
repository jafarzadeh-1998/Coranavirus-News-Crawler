function changeTab(tab) {
    if (tab == "table"){
        $("#home").attr("style", "display: none;");
        $("#table").attr("style", "display: block;");
        $("#news").attr("style", "display: none;");
        $(".home").removeClass("active");
        $(".news").removeClass("active");
        $(".table").addClass("active");
    }else if(tab == "home"){
        $("#home").attr("style", "display: block;");
        $("#table").attr("style", "display: none;");
        $("#news").attr("style", "display: none;");
        $(".table").removeClass("active");
        $(".news").removeClass("active");
        $(".home").addClass("active");
    }else if(tab == "news"){
        $("#news").attr("style", "display: block;");
        $("#home").attr("style", "display: none;");
        $("#table").attr("style", "display: none;");
        $(".home").removeClass("active");
        $(".table").removeClass("active");
        $(".news").addClass("active");
    }

    return
}

$(".home").click(function(){
    changeTab("home");
});

function buildTable(data) {
    table = "<table style='border: 1px solid black;'><thead><tr>";
            for(let index=0; index < data.head.length; index++ ){
                table += "<th class='sort_by true' style='border: 1px solid black;'>"+data.head[index] + "</th>";
            }
            table += "</tr></thead><tbody>";
            console.log(data.body);
            for(let rowIndex=0; rowIndex < data.body.length ;rowIndex++){
                row = data.body[rowIndex];
                table += "<tr>";
                for (let colIndex = 0; colIndex < row.columns.length; colIndex++){
                    if (rowIndex%2 == 0)
                        table += "<td style='border: 1px solid black; background-color:#E0E0E0;'>" + row.columns[colIndex] + "</td>";
                    else
                        table += "<td style='border: 1px solid black;'>" + row.columns[colIndex] + "</td>";
                }
                table += "</tr>";
            }
            table += "</tbody></table>";
    return table
}

$(".table").click(function(){
    changeTab("table");
    $.ajax({
        method: 'GET',
        url: "/worldometers/get_table/",
        dataType: 'json',
        data: {},
        success: function (data) {
            table = buildTable(data);
            $("#table").html(table);
            sort();
        },
        error: function (data) {
            console.log(data);
        },
    });
});

function sort() {
    $('.sort_by').click(function(){
        console.log($(this).text());
        let is_dec = $(this).hasClass('true')
        console.log(is_dec);
        $.ajax({
            method: 'GET',
            url: "/worldometers/get_sorted_table/",
            dataType: 'json',
            data: {"sort_by":$(this).text(),
                   "is_dec": is_dec},
            success: function (data) {
                table = buildTable(data);
                $("#table").html(table);
                $(this).toggleClass("true");
                // if (is_dec){
                //     console.log("FUCKING INC");
                //     $(this).attr("class", "sort_by False");
                // }
                // else {
                //     console.log("FUCKING DEC");
                //     $(this).attr("class", "sort_by True");
                //     // $(this).removeClass("False");
                //     // $(this).addClass("True");
                // }

                sort();
            },
            error: function (data) {
                console.log(data);
            },
        });
    });    
}


function fillNews(newsData) {
    news = "<div class='news' ><table>";
   for (let index = 0; index < newsData.length; index++){
        news += "<tr class='class_ul'><td style='background-color:";
        if (index%2 == 0)
            news += "#C0C0C0;'>";
        else
            news += "#FFFFFF;'>";
        news += "<li>" + newsData[index].title + "<a href='"+ newsData[index].countrySrc + "'> "+
                newsData[index].countryName+"</a>\t";
        for (let source_index = 0; source_index < newsData[index].newsSources.length; source_index++)
            news += "<a style='font-size:12px;' href='"+ newsData[index].newsSources[source_index] + "'>original News link</a> - ";
        news += "</li></td></tr>";
    }

   news += "</table></div>";
   return news
}
function getNews(pageNum) {
    $.ajax({
        method: 'GET',
        url: "/worldometers/top_news/"+pageNum,
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

$(".news").click(function(){
    changeTab("news");
    getNews(0);
});

$('.nextPage').click(function(){
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