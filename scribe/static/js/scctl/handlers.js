
var app = angular.module("scribe", []);
app.controller("scctl", function($scope, $http) {
    $scope.home = "This is the homepage";
    $scope.test = "This is the homepage";

  $scope.loadSection = function(field) {
    console.log("I've been pressed! "  + Math.random());
    $http.get("/files").then(
	function successCallback(response) {
	    
            $scope.response = response + Math.random();
	    document.getElementById(field).innerHTML = response.data
      },
      function errorCallback(response) {
        console.log("Unable to perform get request");
      }
    );
  };
});


function loadSectionPlain(element) {
    var xhttp = new XMLHttpRequest();
    
    xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
	    document.getElementById(element).innerHTML =
		this.responseText;
	}
    };
    xhttp.open("GET", "/files", true);
    console.log("Sending request")
    xhttp.send();
}



function onEdit() {
    console.log("Edit clicked");
}

function onEditSave() {
    console.log("Save clicked");
}

function onEditCancel() {
    console.log("Cancel clicked");
}


function onStop() {
    
    console.log("Stop clicked");
}

function onDelete(id) {
    console.log("Delete clicked");

    var xhttp = new XMLHttpRequest();
    
    xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
	    console.log(this.responseText);
	    loadSectionPlain('files');
	}
    };
    xhttp.open("POST", "/delete-transcript/"+id, true);
    console.log("Sending request")
    xhttp.send();

    
}


