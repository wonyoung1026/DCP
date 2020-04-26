
function getInstanceDetail(){
    // Hide other cards and display Full Instance Detail Card
    document.getElementById("instance-detail-card").style.display = "block";
    document.getElementById("monitoring-card").style.display = "none";
}

function getMonitoring(){
    // Hide other cards and display Full Instance Detail Card
    document.getElementById("monitoring-card").style.display = "block";
    document.getElementById("instance-detail-card").style.display = "none";

    var monitoringElement = document.getElementById("monitoring");
    var monitoringErrorElement = document.getElementById("monitoring-err");
    
    var http = new XMLHttpRequest();
    var gpuID = document.getElementById("instance-detail").getAttribute("gpu-id");
    var url = "/provider/vm/gpu/"+gpuID+"/monitoring";
    
    http.open('GET', url, true);
    http.onreadystatechange= function(){
        if(http.readyState == 4){
            var res = JSON.parse(http.response)
            switch(http.status){
                case 200:
                    output = res.output;
                    console.log(output)
                    visualizeGPUUtil(output['time'], output["gpuUtils"])
                    visualizeMemoryUtil(output['time'], output["memoryUtils"])
                    break;
                default:
                    
                    monitoringElement.style.display = "none";
                    monitoringErrorElement.style.display = "block";
                    monitoringErrorElement.style.color = "red";
                    monitoringErrorElement.innerHTML = res.message;

                    break;
            }
        }
    }
    http.send();
}



function addVacancy(boolVacancy, element){
    if (boolVacancy)
        element.innerHTML = "<span class='btn btn-primary'></span> Vacant";
    else
        element.innerHTML = "<span class='btn btn-danger'></span> Occupied";
    

}


function addVMTableRowHandlers(){
    var table = document.getElementById("vm-table");
    var rows = table.getElementsByTagName("tr");
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
                
                var gpuID = row.getAttribute("gpu-id");
                instanceDetailElement.setAttribute("gpu-id", gpuID);

                instanceDetailElement.style.display = "none";
                instanceDetailErrorElement.style.display = "block";
                instanceDetailErrorElement.style.color = "black";
                instanceDetailErrorElement.innerHTML = "Searching...";

                
                var http = new XMLHttpRequest();
                var url = "/provider/vm/gpu/"+gpuID
                
                http.open('GET', url, true);
                http.onreadystatechange = function(){
                    if(http.readyState == 4){
                        
                        var res = JSON.parse(http.response);
                        switch(http.status){
                            // Load vm details on success
                            case 200:
                                instanceDetailElement.style.display = "block";
                                instanceDetailErrorElement.style.display = "none";
                            
                                var output = res.output;
                                console.log(output);
                                
                                // GPU id
                                document.getElementById("instance-detail-instance-id").innerHTML = output.id;
                                
                                // GPU name
                                document.getElementById("instance-detail-name").innerHTML = output.name;
                                
                                // Host ID
                                document.getElementById("instance-detail-host-id").innerHTML = output.hostID;
                                
                                // UUID
                                document.getElementById("instance-detail-uuid").innerHTML = output.uuid;
                                
                                // Total earnings
                                document.getElementById("instance-detail-earnings").innerHTML = output.dueEarnings + "/" + output.totalEarnings ;
                                
                                // Processor
                                document.getElementById("instance-detail-processor").innerHTML = output.processor;
                                
                                // Price
                                document.getElementById("instance-detail-price").innerHTML = output.price;

                                // Status
                                var vacancyElement = document.getElementById("instance-detail-vacancy");
                                addVacancy(output.isVacant, vacancyElement);

                                // Registered Time
                                document.getElementById("instance-detail-registered-time").innerHTML = output.createdOn;
                                
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

function modifyConfirm(){
    var priceInputElement = document.getElementById("instance-detail-price-input")
    var nameInputElement = document.getElementById("instance-detail-name-input")
    
    var gpuID = document.getElementById("instance-detail").getAttribute("gpu-id");

    var data = JSON.stringify({'name': nameInputElement.value, 'price': priceInputElement.value})
    var url = "/provider/vm/gpu/"+gpuID;
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
                    var instanceDetailElement = document.getElementById("instance-detail");
                    var instanceDetailErrorElement = document.getElementById("instance-detail-err");

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

function modifyClose(){
    var nameInputElement = document.getElementById("instance-detail-name-input");
    var nameElement = document.getElementById("instance-detail-name");

    var priceInputElement = document.getElementById("instance-detail-price-input");
    var priceElement = document.getElementById("instance-detail-price");

    nameInputElement.style.display = "none";
    nameElement.style.display = "block";
    
    priceInputElement.style.display = "none";
    priceElement.style.display = "block";

    document.getElementById("modify-btn-col").style.display = "none";
    document.getElementById("btn-col").style.display = "block";
}


function modify(){
    // Name
    var nameInputElement = document.getElementById("instance-detail-name-input")
    var nameElement = document.getElementById("instance-detail-name")
    var oldName = nameElement.innerHTML;
    
    // Price
    var priceInputElement = document.getElementById("instance-detail-price-input")
    var priceElement = document.getElementById("instance-detail-price")
    var oldPrice = priceElement.innerHTML;

    nameInputElement.style.display = "block";
    nameInputElement.setAttribute("value", oldName);
    nameElement.style.display = "none";
    

    priceInputElement.style.display = "block";
    priceInputElement.setAttribute("value", oldPrice);
    priceElement.style.display = "none";


    document.getElementById("modify-btn-col").style.display = "block";
    document.getElementById("btn-col").style.display = "none";


}


// Call the dataTables jQuery plugin
$(document).ready(function() {
    $('#dataTable').DataTable();
    addVMTableRowHandlers();
  });
  
  