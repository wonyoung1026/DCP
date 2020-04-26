
function visualizeGPUUtil(xData, yData){
  
  var gpuUtilCTX = document.getElementById("gpu-cpu-util-chart");
  var bUnit = "%";

  createChart(gpuUtilCTX, xData, yData, "", bUnit);
}

function visualizeMemoryUtil(xData, yData){
  var memoryUtilCTX = document.getElementById("gpu-memory-util-chart");
  var bUnit = "%";
  createChart(gpuUtilCTX, xData, yData, "", bUnit);
}