
 $(document).ready(function() {
    var node = document.createElement("li");
    var name = "John Smith"
	var textnode = document.createTextNode("Logged In: " + name );
    node.appendChild(textnode);
	node.id="log";
    document.getElementById("navbar").appendChild(node);

});


