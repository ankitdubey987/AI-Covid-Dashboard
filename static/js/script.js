$(document).ready(function() {
	M.AutoInit();
	// const camchecks = 'input[type="checkbox"]';
	// Find all checkboxes for 4 camera select
	// const d4cams = $('#camselect4').find(camchecks);
	// const d4camsbBtn = $('#camselect4').find('#submit-btn');
	// let selectCount = 0;
	// $.each(d4cams, function(i, checkbox) {
	// 	checkbox.onchange = function(e) {
	// 		if (this.checked == true) {
	// 			selectCount++;
	// 		}
	// 		if (selectCount == 4) {
	// 			d4camsbBtn.removeAttr('disabled');
	// 		}
	// 	};
	// });
	// // Find all checkboxes for 4 camera select
	// const d8cams = $('#camselect8').find(camchecks);
	// const d8camsbBtn = $('#submit-btn8').find('#submit-btn');
	// let selCount = 0;
	// $.each(d8cams, function(i, checkbox) {
	// 	checkbox.onchange = function(e) {
	// 		if (this.checked == true) {
	// 			selCount++;
	// 		}
	// 		if (selCount == 8) {
	// 			d8camsbBtn.removeAttr('disabled');
	// 		}
	// 	};
	// });
	function sound(src) {
		this.sound = document.createElement("audio");
		this.sound.src = src;
		this.sound.setAttribute("preload", "auto");
		this.sound.setAttribute("controls", "none");
		this.sound.style.display = "none";
		document.body.appendChild(this.sound);
		this.play = function(){
		  this.sound.play();
		}
		this.stop = function(){
		  this.sound.pause();
		}
	  }

	config = {
		"apiKey": "AIzaSyD_0l-rC3hVyUyBjGqSlFY88PCT6jruzNU",
		"authDomain": "linecrossfinal.firebaseapp.com",
		"databaseURL": "https://linecrossfinal.firebaseio.com",
		"projectId": "linecrossfinal",
		"storageBucket": "linecrossfinal.appspot.com",
		"messagingSenderId": "474670727546",
		"appId": "1:474670727546:web:72f837e302d96d151b96c3",
		"measurementId": "G-69KN7308TF"
	}
	
	const messaging  = firebase.messaging();
	const db = firebase.database();
	messaging.usePublicVapidKey("BEaiwVFGwMlkSeaARb-b9yoPiCqRAtnK-2HlGAsgnZkLmBFsGsca27SzjG1WsNqgDV3FnvkcQRLmi3fhEsuIbVs");

	messaging.requestPermission()
	.then(() => messaging.getToken())
	.then(token => {
		// console.log(token)
	})
	.catch(function(err){
		console.log("user didn't give permission!")
	})
	// messaging.onMessage((payload) => {
	// 	console.log('Message received. ', payload);
	// 	M.toast({html: 'I am a toast!'})
	// 	// ...
	//   });
	//   var ref = firebase.database().ref("event");
	  let date = formatDate(new Date());
		db.ref("event").orderByChild("date")
		.equalTo(date)
		.on("child_added", function (snapshot) {
		//   M.toast({ html: "New Notification!", displayLength: 2000 })
		  const imgPath = snapshot.val().img_url;
			if(snapshot.val().type == 'critical'){
				// const alertSound = new sound("beep-02.mp3");
				M.toast({html: "New notification received!"});
				$('#notificationlist').append(`
			<li>
				<div class="collapsible-header" style='background-color: antiquewhite;'><i class="material-icons">warning</i>
				<span> ${snapshot.val().activity}</span><span style="margin-left: auto;"> <a href="/${snapshot.val().activity}/${snapshot.val().camera_name}"> ${snapshot.val().camera_name}</a></span>
				</div>
				<div class="collapsible-body"><p></p>
				<img src='${imgPath}' height="200" width="300" />
				</div>
			</li>
		  `)
		  audioCtx = new(window.AudioContext || window.webkitAudioContext)();

			beep(audioCtx);
			}
			

		});
//     console.log(currentToken)
//     // updateUIForPushEnabled(currentToken);
//   } else {
//     // Show permission request.
//     console.log('No Instance ID token available. Request permission to generate one.');
//     // Show permission UI.
//     // updateUIForPushPermissionRequired();
//     // setTokenSentToServer(false);
//   }
// }).catch(() => {
// //   console.log('An error occurred while retrieving token. ', err);
// //   showToken('Error retrieving Instance ID token. ', err);
// //   setTokenSentToServer(false);
// 	console.log("user didn't give permission!");
// });
messaging.onTokenRefresh(() => {
  messaging.getToken().then((refreshedToken) => {
    console.log('Token refreshed.');
    // Indicate that the new Instance ID token has not yet been sent to the
    // app server.
    setTokenSentToServer(false);
    // Send Instance ID token to app server.
    sendTokenToServer(refreshedToken);
    // ...
  }).catch((err) => {
    console.log('Unable to retrieve refreshed token ', err);
    showToken('Unable to retrieve refreshed token ', err);
  });
});
	let vids = document.querySelectorAll('video');
	// for all the videos in the page
	for (let x = 0; x < vids.length; x++) {
		// add an event listening for errors
		vids[x].addEventListener(
			'error',
			function(e) {
				// console.log('is it working');
				// if the error is caused by the video not loading
				if (this.networkState > 2) {
					// add an image with the message "video not found"
					this.setAttribute('poster', 'http://dummyimage.com/312x175/000/fff.jpg&text=Video+Not+Found');
				}
			},
			true
		);
	}
});

function formatDate(date) {
	var d = new Date(date),
		month = '' + (d.getMonth() + 1),
		day = '' + d.getDate(),
		year = d.getFullYear();

	if (month.length < 2) month = '0' + month;
	if (day.length < 2) day = '0' + day;

	return [ year, month, day ].join('-');
}

function getSeletedCams(allcams) {
	const selCams = [];
	$.each(allcams, function(index, checkbox) {
		if (this.checked == true) {
			selCams.push(this.getAttribute('data-id'));
			this.checked = false;
		}
	});
	return selCams;
}

function playcams(count) {
	const dateStr = formatDate(new Date());
	for (let i = 1; i <= count; i++) {
		let colSize;
		if (count == 8) colSize = 3;
		if (count == 4) colSize = 6;
		const display = $(`<div class='col-md-${colSize} col-sm-12' id='display${i}'></div>`);
		const videoItem = $(
			`<video id='video${i}' width='500' height=270 class="video-js vjs-default-skin" controls></video>`
		);
		const sourceItem = $(`<source>`);
		const srcStr = `http://localhost:8080/hls/cam${i}/${dateStr}/index.m3u8`;
		sourceItem.attr('src', srcStr);
		sourceItem.attr('type', 'application/x-mpegURL');
		videoItem.append(sourceItem);
		display.append(videoItem);
		$('#camsDisplay').append(display);
		try {
			let player = videojs(`video${i}`);
			player.play();
			player.ready(function() {
				if (this.error !== null) {
				}
			});
		} catch (error) {
			console.log(error);
		}
	}
}
var mini = true;
function openSlideMenu() {
	document.getElementById('side-menu').style.width = '250px';
	document.getElementById('main').style.marginLeft = '250px';
}
function closeSlideMenu() {
	document.getElementById('side-menu').style.width = '0';
	document.getElementById('main').style.marginLeft = '0';
}
function beep(audioCtx){
	var oscillator = audioCtx.createOscillator();
	let gainNode = audioCtx.createGain();

	oscillator.connect(gainNode);
	gainNode.connect(audioCtx.destination);

	gainNode.gain.value = 0.45;
	oscillator.frequency.value = 620;
	oscillator.type = 'triangle';

	oscillator.start();

	setTimeout(function(){
		oscillator.stop();
	}, 1000)
}
// function toggleSidebar() {
// 	if (mini) {
// 		document.getElementById('sidebar').style.width = '200px';
// 		document.getElementById('camsDisplay').style.marginLeft = '200px';
// 		this.mini = false;
// 	} else {
// 		document.getElementById('sidebar').style.width = '85px';
// 		document.getElementById('camsDisplay').style.marginLeft = '85px';
// 		$('.collapse').collapse();
// 		this.mini = true;
// 	}
// }

// const date = new Date();
// const month = (date.getMonth() + 1).toLocaleString().padStart(2, '0');
// const day = date.getDate()().toLocaleString().padStart(2, '0');
// const dateStr = date.getFullYear() + '-' + month + '-' + day;
