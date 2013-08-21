
 
 var pictureSource; 
    var destinationType;
		var message;
			var recipient;
				var subject;
					var ImageSrc;
						var attachment;
    // Wait for device API libraries to load
    document.addEventListener("deviceready",onDeviceReady,false);

    // device APIs are available
    //
    // Called when a photo is successfully retrieved
    //
	function  changePage(){
		window.location = "processing.html";
	}
	//USED FOR FIRST PHOTO --- SENDER
    function onPhotoDataSuccess(imageData) {
      ImageSrc = "data:image/jpeg;base64," + imageData;
	  localStorage.setItem("imageSrc", ImageSrc);
	  document.location.href = "input.html";
	  }
	  function backgroundSet(){
	  var background = new Image();
	  background.src = localStorage.imageSrc;
	  document.getElementById("page1").style.backgroundImage = "url(" + background.src + ")";
	  document.getElementById("page1").style.backgroundSize = "100%";
	  }
	  //USED FOR THE SECOND PHOT0 --- RECIPIENT'S ATTEMPT
	  function onPhotoDataSuccess2(imageData) {
      ImageSrc = "data:image/jpeg;base64," + imageData;
	  document.getElementById("container2").innerHTML = "<img src = '" + ImageSrc + "' width = '100%'/>"
	  }
	  
	  //SENDS EMAIL
	  function sendMessage(){
	  recipient = document.getElementById("recipient").value;
	  subject = "You got a new garfiti!";
	  message = document.getElementById("message").value;
	  writeGarf();
	  //alert(attachment);
	  setTimeout(window.plugins.emailComposer.showEmailComposerWithCallback(null, subject,message,[recipient],[],[],true,["/mnt/sdcard/newMessage.txt"]), 1000);	  
	  //window.location = "open.html";
	  	toastr.success("Message sent!");
	  window.location = "index.html";
	  
    }
	

    //
    function capturePhoto() {
	  
	    pictureSource=navigator.camera.PictureSourceType;
        destinationType=navigator.camera.DestinationType;
      // Take picture using device camera and retrieve image as base64-encoded string
      navigator.camera.getPicture(onPhotoDataSuccess, onFail, { quality: 50,
        destinationType: destinationType.DATA_URL });
    }
	
	    function capturePhoto2() {
	  
	    pictureSource=navigator.camera.PictureSourceType;
        destinationType=navigator.camera.DestinationType;
      // Take picture using device camera and retrieve image as base64-encoded string
      navigator.camera.getPicture(onPhotoDataSuccess2, onFail, { quality: 50,
        destinationType: destinationType.DATA_URL });
    }


    // A button will call this function
    //
    
    function onFail(message) {
      alert('Failed because: ' + message);
    }

	
//ALL OF THE CODE FOR THE WRITER FUNCTIONALITY
//BASICALLY WRITES TO A FILE THAT IS THEN ATTACHED IN THE SEND EMAIL FUNCTIONALITY	
        function writeGarf(){
			window.requestFileSystem(LocalFileSystem.PERSISTENT, 0, gotFS, fail);
		}
    

            function gotFS(fileSystem) {
                fileSystem.root.getFile("newMessage.txt", {create: true, exclusive: false}, gotFileEntry, fail);
            }

            function gotFileEntry(fileEntry) {
				attachment = fileEntry;
                fileEntry.createWriter(gotFileWriter, fail);
            }

            function gotFileWriter(writer) {
                writer.onwrite = function(evt) {
                    console.log("write success");
                };

                writer.write(document.getElementById("recipient").value + "\n" + document.getElementById("message").value + "\n" + document.getElementById("title").value + "\n" + localStorage.username + "\n" + localStorage.imageSrc);
                writer.abort();
                // contents of file now 'some different text'
            }

            function fail(error) {
                console.log("error : "+error.code);
            }
			
//END CODE FOR WRITER

//BEGIN CODE FOR READER
//READS FILES AS TEXT AND RESOLVES EACH LINE TO VARIABLE IT REPRESENTS			
			
		function openFile(){
			window.location = "open.html";
		}
			
	function startRead() {
        window.requestFileSystem(LocalFileSystem.PERSISTENT, 0, gotFS2, fail);
    }

    function gotFS2(fileSystem) {
		var fullPath = document.getElementById('fileChoose').value;
        fileSystem.root.getFile(fullPath.replace(/^.*[\\\/]/, ''), null, gotFileEntry2, fail);
	
    }

    function gotFileEntry2(fileEntry) {
        fileEntry.file(gotFile, fail);
    }

    function gotFile(file){
        readAsText(file);		
    }

 

    function readAsText(file) {
        var reader = new FileReader();
        reader.onloadend = function(evt) {
            console.log("Read as text");
           var text =  evt.target.result;
		   openFunction(text);
        };
       reader.readAsText(file);
	   
    }

    function fail(evt) {
        toastr.warning("Something went wrong");
    }
	
//FILE HAS BEEN READ AND HERE IT IS MADE USEFUL
	var recipient;
	var message;
	var title;
	var sender;
	var base64IMG
	function openFunction(text){
		lines = text.split("\n");
		recipient = lines[0];		
		message = lines[1];
		title = lines[2];
		sender = lines[3];
		
		lines.splice(0,4);
		base64IMG = lines.join('\n');
	
		document.getElementById("container1").innerHTML = "<img src = '" + base64IMG + "' width = '100%'  />";
		document.getElementById("heading").innerHTML = "Sent to: " + recipient + "<br />" +  "From: " + sender;
		document.getElementById("title").innerHTML = "'" + title + "'";
		document.getElementById("choose").innerHTML = "";
		document.getElementById("compare").innerHTML = "<input type = 'button' value = 'Match' onclick = 'success()'/><input type = 'button' value = 'Fail' onclick = 'failMatch()' />";
	}

//NO MORE READING
//END READER FUNCTION


//SUCCESS OR FAIL MATCH?
	function success(){
		document.getElementById("page1").innerHTML = "";
		var back = new Image();
		back.src = base64IMG;
		alert(base64IMG);
		document.getElementById("page1").style.background = "url(" + back.src + ")";
		document.getElementById("page1").style.backgroundSize = "100%";
		document.getElementById("page1").innerHTML = " \
	<div style = 'width: 49%; float: left; background-color: grey; color: white; opacity: 0.5; font-family: cursive; border: 2px solid white;'> From: " + sender + "\
	 \
   </div> \
      <div style = 'width: 49%; float: right;background-color: grey; color: white; opacity: 0.5; font-family: cursive; border: 2px solid white;'>" + title + "\
	\
	</div>\
	\
	<center>\
   <div style = 'width: 65%; left: 50%; margin-left: -32.5%; position: absolute; top: 30%; text-align: center; background-color: grey; border: 2px solid white; opacity: 0.5; color: white; font-family: cursive; padding: 20px; font-size: 20px;'>"  + message + "\
	 \
	</div>\
	\
	</center>\
	";
	toastr.success("Nice Job!");
	}
	
	function failMatch(){
		toastr.warning("Oops! Looks like it wasn't a match! Try Again!");
		document.getElementById("container2").innerHTML = "<input type = 'button' value =  'Attempt Match' onclick = 'capturePhoto2()' />";
	}

	
//DECODES A BASE64 STRING SO THAT IT CAN BE SET AS THE BACKGROUND IMAGE?

