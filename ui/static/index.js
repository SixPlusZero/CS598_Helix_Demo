
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
                inHTML += '<li><a href="#">Workflow 1</a></li>';
            }
            document.getElementById("pageSubmenu").innerHTML = inHTML;
        },
        error: function (jqXHR, textStatus, errorThrown){
            //alert("Failed");
            console.log("set workflow tab failed");
        }
    });
}