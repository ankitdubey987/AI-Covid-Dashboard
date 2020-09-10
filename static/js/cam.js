$(document).ready(function() {
    displayVideo(camData);
    $('#displaydetails').css('display', 'block')
})


function displayVideo(cam_data){
    const dateStr = formatDate(new Date());
    const display = $("#display1")
    const sourceItem = $(`<source>`);
    const videoItem = $(`<video id='video${cam_data.id}' width='900' height=560 class="video-js vjs-default-skin" controls></video>`);
    const srcStr = `http://localhost:8080/hls/${cam_data.id}/${dateStr}/index.m3u8`;
    sourceItem.attr('src', srcStr);
    sourceItem.attr('type', 'application/x-mpegURL');
    videoItem.append(sourceItem);
    display.append(videoItem);
    // const displaydetail = $(`<div class='col s4' id='displaydetail'></div>`)
    // displaydetail.append(`<h1>Camera ${cam_data.id}</h1>`)
    $('#camsDisplay').append(display);
    // $('#camsDisplay').append(displaydetail);
    if(videojs != undefined){
        let player = videojs(`video${cam_data.id}`);
        player.play();
    }
}


function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [ year, month, day ].join('-');
}