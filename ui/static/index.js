
function setWorkflowTab() {

    $.ajax({
        url : "./wflist/",
        type: "POST",
        dataType: "text",
        data : {"csrfmiddlewaretoken": CSRF_TOKEN},
        success: function(data, textStatus, jqXHR){
            var arr = JSON.parse(data);
            var inHTML = "";
            for (i = 0; i < arr.length; i++) {
                console.log(arr[i]);
                inHTML += '<li><a href="' + './?workflow=' + arr[i] + '">' + arr[i] + '</a></li>';
            }
            document.getElementById("pageSubmenu").innerHTML = inHTML;
        },
        error: function (jqXHR, textStatus, errorThrown){
            //alert("Failed");
            console.log("set workflow tab failed");
        }
    });
}