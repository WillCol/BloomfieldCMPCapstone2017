$(function() {
var select = document.getElementById("taskType");
var options = ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"];
for(var i = 0; i < options.length; i++) {
    var opt = options[i];
    var el = document.createElement("option");
    el.textContent = opt;
    el.value = opt;
    select.appendChild(el);
}
});