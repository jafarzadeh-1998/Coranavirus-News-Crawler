function changeTab(tab) {
    if (tab == "table"){
        $(".home").removeClass("active");
        $("#home").attr("style", "display: none;");
        $("#table").attr("style", "display: block;");
        $(".table").addClass("active");
    }else if(tab == "home"){
        $("#home").attr("style", "display: block;");
        $("#table").attr("style", "display: none;");
        $(".table").removeClass("active");
        $(".home").addClass("active");
    }
    return
}

$(".home").click(function(){
    changeTab("home");
});

$(".table").click(function(){
    changeTab("table");
    $.ajax({
        method: 'GET',
        url: "/worldometers/get_table/",
        dataType: 'json',
        data: {},
        success: function (data) {
            table = "<table style='border: 1px solid black;'><thead><tr>";
            for(let index=0; index < data.head.length; index++ ){
                table += "<th>"+data.head[index] + "</th>";
            }
            table += "</tr></thead><tbody>";
            console.log(data.body);
            for(let rowIndex=0; rowIndex < data.body.length ;rowIndex++){
                row = data.body[rowIndex];
                table += "<tr>";
                for (let colIndex = 0; colIndex < row.columns.length; colIndex++)
                    table += "<td>" + row.columns[colIndex] + "</td>";
                table += "</tr>";
            }
            table += "</tbody></table>";
            $("#table").html(table);
        },
        error: function (data) {
            console.log(data);
        },
    });
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