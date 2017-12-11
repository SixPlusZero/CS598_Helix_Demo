
function setWorkflowTab() {
    $.ajax({
        url : "/ui/wflist/",
        type: "POST",
        dataType: "text",
        data : {"csrfmiddlewaretoken": CSRF_TOKEN},
        success: function(data, textStatus, jqXHR){
            var arr = JSON.parse(data);
            var inHTML = "";
            if (arr.length == 0) {
                inHTML += '<li> Not available </li>';
                return;
            }
            for (i = 0; i < arr.length; i++) {
                console.log(arr[i]);
                inHTML += '<li><a href="' + '/ui/?workflow=' + arr[i] + '">' + arr[i] + '</a></li>';
            }
            document.getElementById("pageSubmenu").innerHTML += inHTML;
        },
        error: function (jqXHR, textStatus, errorThrown){
            //alert("Failed");
            console.log("set workflow tab failed");
        }
    });
}

function addKeyVal(){
    
    var w = parseInt(document.getElementById("paramcnt").value,10) + 1;
    var newpair = '<div class="input-group"><input style="width:50% " class="form-control " placeholder="key"  name="key' + w + '" type="text" /><input style="width:50% " class="form-control " placeholder="value"  name="val' + w + '" type="text" /></div>';
    document.getElementById("params").innerHTML += newpair;
    document.getElementById("paramcnt").value = w;
}

function queryStatus(){
    var formData = task_id;
    console.log("debuging merge html");
    console.log(formData);
    $.ajax({
        url : "/ui/task/",
        type: "POST",
        dataType: "text",
        data : {"csrfmiddlewaretoken": CSRF_TOKEN, "task_id": formData},
        success: function(data, textStatus, jqXHR){
            prev_status = job_status;
            job_status = JSON.parse(data);
            if (prev_status["state"] == job_status["state"] && prev_status["stage"] == job_status["stage"]) return;
            var new_status = "<p>State: " + job_status["state"] + ", " + "Stage: " + job_status["stage"] + ", " + "Info: " + job_status["stage_message"] + "</p>";
            document.getElementById("msgtrain").innerHTML += new_status;
        },
        error: function (jqXHR, textStatus, errorThrown){
            job_status = {"status": "FAILURE"};
            //alert("Failed");
        }
    });
}

function queryProgress() {
    queryStatus();
    if (job_status["state"] == "SUCCESS") {
        return;
    } else if (job_status["state"] == "FAILURE") {
        return;
    } else {
        setTimeout("queryProgress();", 1000);
    }
}