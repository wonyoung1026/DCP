function getMonitoring(){
    // Hide other cards and display Full Instance Detail Card
    document.getElementById("monitoring-card").style.display = "block";
    document.getElementById("instance-detail-card").style.display = "none";

    var iframeElement = document.getElementById("monitoring-iframe")
    var containerID = document.getElementById("instance-detail").getAttribute("container-id");

    // Get url 
    var http = new XMLHttpRequest();
    var url = "/buyer/container/"+containerID+"/monitor"
    http.open('GET', url, true);
    http.onreadystatechange = function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response);
            iframeElement.src = res.output;
        }
    }
    http.send()
}

function getInstanceDetail(){
    // Hide other cards and display Full Instance Detail Card
    document.getElementById("instance-detail-card").style.display = "block";
    document.getElementById("monitoring-card").style.display = "none";
}


function addContainerTableRowHandlers(){
    var table = document.getElementById("container-table");
    var rows = table.getElementsByTagName("tr");


    function addStatus(intStatus, element){
        switch(intStatus){
            case 0:
                element.innerHTML = "<span class='btn btn-success'></span> Running";
                break;
            case 1:
                element.innerHTML = "<span class='btn btn-primary'></span> Pending";
                break;
            case 2:
                element.innerHTML = "<span class='btn btn-warning'></span> Unstable";
                break;
            case 3:
                element.innerHTML = "<span class='btn btn-danger'></span> Disconnected";
                break;
            case 4:
                element.innerHTML = "<span class='btn btn-warning'></span> Stopped";
                break;
            default:
                break;

        }

    }

    function addElementByList(listInput, element){
        element.innerHTML = "";
        for(i =0; i<listInput.length; ++i){
            element.innerHTML += listInput[i]
            element.innerHTML += "<br>"
        }

    }
    function addGPUStatus(intStatus){
        html = ""
        switch(intStatus){
            case 0:
                html += "<span class='btn btn-primary'></span> Vacant";
                break;
            case 1:
                html +=  "<span class='btn btn-danger'></span> Occupied";
                break;
        }
        return html
    }
    function addGPU(listGPU, element){
        element.innerHTML = "";
        for(i =0; i<listGPU.length; ++i){
            element.innerHTML += "<span class='col-md-2 instance-detail-inner-key'>Processor</span>"
            element.innerHTML += "<span class='col-md-4 instance-detail-inner-value'>" + listGPU[i].processor +"</span>"
            element.innerHTML += "<span class='col-md-2 instance-detail-inner-key'>Price (per hour)</span>"
            element.innerHTML += "<span class='col-md-4 instance-detail-inner-value'> HKD "+ listGPU[i].price +"</span>"
            element.innerHTML += "<br>"
    
        }
    }



    for (i=0; i< rows.length; i++){
        var currentRow = table.rows[i];
        var createClickHandler = function(row) {
            return function(){
                // Hide other cards
                document.getElementById("instance-detail-card").style.display = "block";
                document.getElementById("monitoring-card").style.display = "none";
                
                // Indicate searching
                var instanceDetailElement = document.getElementById("instance-detail");
                var instanceDetailErrorElement = document.getElementById("instance-detail-err");
                
                var containerID = row.getAttribute("container-id");
                instanceDetailElement.setAttribute("container-id", containerID);

                instanceDetailElement.style.display = "none";
                instanceDetailErrorElement.style.display = "block";
                instanceDetailErrorElement.style.color = "black";
                instanceDetailErrorElement.innerHTML = "Searching...";

                var http = new XMLHttpRequest();
                var url = "/buyer/container/"+containerID;
                
                
                http.open('GET', url, true);
                http.onreadystatechange = function(){
                    if(http.readyState == 4){
                        var res = JSON.parse(http.response);
                        switch(http.status){
                            // Load vm details on success
                            case 200:
                                var output = res.output;
                                console.log(output)

                                instanceDetailElement.style.display = "block";
                                instanceDetailErrorElement.style.display = "none";
                            
                                // Container info
                                document.getElementById("instance-detail-container-id").innerHTML = output.container.id;
                                
                                document.getElementById("instance-detail-container-name").innerHTML = output.container.name;
                                
                                var statusElement = document.getElementById("instance-detail-container-status");
                                addStatus(output.container.status, statusElement);

                                document.getElementById("instance-detail-container-spendings").innerHTML = "HKD " + output.container.dueSpendings + "(HKD "+output.container.costRate+" / hr)"

                                document.getElementById("instance-detail-container-created-time").innerHTML = output.container.createdOn

                                // Image info
                                document.getElementById("instance-detail-image-name").innerHTML = output.container.baseImage.name;
                                document.getElementById("instance-detail-image-description").innerHTML = output.container.baseImage.description;
                                

                                // Provider host info
                                document.getElementById("instance-detail-vm-id").innerHTML = output.vm.id;
                                document.getElementById("instance-detail-vm-provider-email").innerHTML = output.vm.providerEmail;
                                document.getElementById("instance-detail-vm-price").innerHTML = "HKD "+output.vm.price;
                                
                                var statusElement = document.getElementById("instance-detail-vm-status");
                                addStatus(output.vm.status, statusElement);

                                var processorElement = document.getElementById("instance-detail-vm-processor");
                                addElementByList(output.vm.processor, processorElement);

                                document.getElementById("instance-detail-vm-core").innerHTML = output.vm.processor.length;

                                var memoryElement = document.getElementById("instance-detail-vm-memory");
                                addElementByList(output.vm.memory, memoryElement);                                
                                
                                var diskElement = document.getElementById("instance-detail-vm-disk");
                                addElementByList(output.vm.disk, diskElement);

                                document.getElementById("instance-detail-vm-disconnection").innerHTML = output.vm.numberOfDisconnections;
                                
                                document.getElementById("instance-detail-vm-registered-time").innerHTML = output.vm.createdOn;


                                // GPU
                                var gpuElement = document.getElementById("instance-detail-gpu");
                                addGPU(output.gpuList, gpuElement);
                                

                                // Start stop button
                                switch(output.container.status){
                                    case 0:
                                        document.getElementById("stop-btn").style.display = "inline-block";
                                        document.getElementById("launch-shell-btn").style.display = "inline-block";
                                        document.getElementById("start-btn").style.display = "none";

                                        break;
                                    case 4:
                                        document.getElementById("stop-btn").style.display = "none";
                                        document.getElementById("launch-shell-btn").style.display = "none";
                                        document.getElementById("start-btn").style.display = "inline-block";
                                        break;
                                    default:
                                        document.getElementById("stop-btn").style.display = "none";
                                        document.getElementById("start-btn").style.display = "none";
                                        document.getElementById("launch-shell-btn").style.display = "none";
                                        break;

                                        
                                }

                                
                                break;
                            default:
                                instanceDetailElement.style.display = "none";
                                instanceDetailErrorElement.style.display = "block";
                                instanceDetailErrorElement.style.color = "red";
                                instanceDetailErrorElement.innerHTML = res.message;
                                break;
                        }
                    } 
                    
                }
                http.send();


            }
        }
        currentRow.onclick = createClickHandler(currentRow);
    }
}


// =======================================================
// Terminate without save button
// =======================================================
function terminateContainer(){
    var containerID = document.getElementById("instance-detail").getAttribute("container-id");
    
    var terminateBtnElement = document.getElementById("terminate-btn");
    terminateBtnElement.getElementsByTagName("span")[0].innerHTML = "Terminating..."
    terminateBtnElement.classList.add("btn-light");


    var url = "/buyer/container/"+containerID+"/terminate";
    var http = new XMLHttpRequest();
    http.open('POST', url, true);
    http.setRequestHeader('Content-Type', 'application/json');
    http.onreadystatechange= function(){

        if(http.readyState == 4){
            var res = JSON.parse(http.response);
            alert("["+http.status+"]" + res.message)
            switch(http.status){
                case 201:
                    window.location.reload(false);
                    break;
                default:
                    terminateBtnElement.getElementsByTagName("span")[0].innerHTML = "Terminate"
                    terminateBtnElement.classList.remove("btn-light");
                    break;
            }
        }
    }
    http.send()
}

function getGPUModal(){
    var vmID = document.getElementById("instance-detail-vm-id").innerHTML;
    var selectGPUModalBody = document.getElementById("select-gpu-modal-body")
    selectGPUModalBody.innerHTML = "Loading GPUs..."
    var url = "/buyer/vm/"+vmID +"/gpu"
    var http = new XMLHttpRequest();

    http.open('GET', url, true);
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response)
            selectGPUModalBody.innerHTML=""
            switch(http.status){
                case 200:
                    var gpuList = res.output;
                    console.log(gpuList)
                    if (gpuList.length == 0){
                        selectGPUModalBody.innerHTML = "No GPU!";
                        break;
                    }
                    selectGPUModalBody.innerHTML = ""
                    for (i=0;i<gpuList.length; i++){
                        if(gpuList[i].status == 0){
                            selectGPUModalBody.innerHTML += 
                            "<div class='funkyradio-default'> \
                                <input type='checkbox' name='checkbox' processor="+gpuList[i].processor+" id="+gpuList[i].id+" price="+gpuList[i].price+" /> \
                                <label for="+gpuList[i].id+">"+gpuList[i].processor+" [HKD"+gpuList[i].price+"]</label>\
                            </div> \
                            "

                        }
                        else{
                            selectGPUModalBody.innerHTML += 
                            "<div class='funkyradio-danger'> \
                                <input disabled='disabled' type='checkbox' name='checkbox' id="+gpuList[i].id+" /> \
                                <label for="+gpuList[i].id+">"+gpuList[i].processor+" [HKD"+gpuList[i].price+"]</label>\
                            </div> \
                            "
                        }
                    }

                    break;
                default:

                    break;
            }

        }
    }
    http.send();
}

// =======================================================
// Start button
// =======================================================
function startContainer(){
    var containerID = document.getElementById("instance-detail").getAttribute("container-id");
    var checkboxList = document.getElementById("select-gpu-modal-body").getElementsByTagName("input");
    
    var startBtnElement = document.getElementById("start-btn");
    startBtnElement.getElementsByTagName("span")[0].innerHTML = "Starting..."
    startBtnElement.classList.add("btn-light");

    var gpuIDs = []
    
    for (i=0;i<checkboxList.length; i++){
        if (checkboxList[i].checked){
            gpuIDs.push(checkboxList[i].getAttribute("id"));
        }
    }

    var url = "/buyer/container/"+containerID+"/start";
    var data = JSON.stringify({"gpuIDs":gpuIDs})
    var http = new XMLHttpRequest();
    http.open('POST', url, true);
    http.setRequestHeader('Content-Type', 'application/json');
    http.onreadystatechange= function(){

        
        if(http.readyState == 4){
            var res = JSON.parse(http.response);
            alert("["+http.status+"]" + res.message)
            switch(http.status){
                case 201:
                    window.location.reload(false);
                    break;
                default:
                    startBtnElement.getElementsByTagName("span")[0].innerHTML = "Start"
                    startBtnElement.classList.remove("btn-light");
                    break;
            }
        }

    }

    http.send(data);

}
// =======================================================
// Stop button
// =======================================================
function stopContainer(){
    var containerID = document.getElementById("instance-detail").getAttribute("container-id");
    
    var stopBtnElement = document.getElementById("stop-btn");
    stopBtnElement.getElementsByTagName("span")[0].innerHTML = "Stopping..."
    stopBtnElement.classList.add("btn-light");

    var url = "/buyer/container/"+containerID+"/stop";
    var http = new XMLHttpRequest();
    http.open('POST', url, true);
    http.setRequestHeader('Content-Type', 'application/json');
    http.onreadystatechange= function(){

        if(http.readyState == 4){
            var res = JSON.parse(http.response);
            alert("["+http.status+"]" + res.message)

            switch(http.status){
                case 201:
                    window.location.reload(false);
                    break;
                default:
                    stopBtnElement.getElementsByTagName("span")[0].innerHTML = "Stop"
                    stopBtnElement.classList.remove("btn-light");
                    break;
            }
        }

    }
    http.send()
}



// =======================================================
// Modify button
// =======================================================
function modifyClose(){
    var nameInputElement = document.getElementById("instance-detail-container-name-input");
    var nameElement = document.getElementById("instance-detail-container-name");


    nameInputElement.style.display = "none";
    nameElement.style.display = "block";
    
    document.getElementById("modify-btn-col").style.display = "none";
    document.getElementById("btn-col").style.display = "block";
}


function modifyConfirm(){
    var nameInputElement = document.getElementById("instance-detail-container-name-input")
    var instanceDetailElement = document.getElementById("instance-detail");
    var instanceDetailErrorElement = document.getElementById("instance-detail-err");
    
    var containerID = document.getElementById("instance-detail").getAttribute("container-id");

    var data = JSON.stringify({'name': nameInputElement.value})
    var url = "/buyer/container/"+containerID;
    var http = new XMLHttpRequest();
    http.open('UPDATE', url, true);
    http.setRequestHeader('Content-Type', 'application/json');
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response)
            switch(http.status){
                case 202:
                    window.location.reload(false);

                    break;
                default:
                    instanceDetailElement.style.display = "none";
                    instanceDetailErrorElement.style.display = "block";
                    instanceDetailErrorElement.style.color = "red";
                    instanceDetailErrorElement.innerHTML = res.message;
                    break;
            }
        }
    }
    http.send(data);
}

function modify(){
    // Name
    var nameInputElement = document.getElementById("instance-detail-container-name-input")
    var nameElement = document.getElementById("instance-detail-container-name")
    var oldName = nameElement.innerHTML;

    nameInputElement.style.display = "block";
    nameInputElement.setAttribute("value", oldName);
    nameElement.style.display = "none";


    document.getElementById("modify-btn-col").style.display = "block";
    document.getElementById("btn-col").style.display = "none";


}

function launchContainerShell(){
    var containerID = document.getElementById("instance-detail").getAttribute("container-id");

    var http = new XMLHttpRequest();
    var url = "/buyer/container/"+containerID+"/shell"
    http.open('GET', url, true);
    http.onreadystatechange = function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response);
            window.open(res.output)
        }
    }
    http.send()
    
}


// Call the dataTables jQuery plugin
$(document).ready(function() {
    $('#dataTable').DataTable();
    addContainerTableRowHandlers();
  });
  
  