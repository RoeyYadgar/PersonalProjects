
window.addEventListener("message",(event) => {
    console.log("Message Received");
    message = event.data;
    var mode = message['Mode']
    var command = message['Command']
    
    switch(message['Mode']){
        case "Youtube":
            var player = document.getElementById("movie_player");
            break;
        case "Twitch":
            var player = document.getElementsByTagName('video')[0];
            break;
        case "Mako":
            var player = document.getElementsByTagName('video')[0];
            break;
        case "Netflix":
            var player = document.getElementsByTagName('video')[0];
            console.log(player);
            break;
        case "Kan":
            var player = document.getElementsByTagName('video')[0];
            break;        
    }


    switch (message['Command']){
        case "Mute":          
            Mute(mode,player);
            break;
        case "Volume up":
            Volumeup(mode,player);        
            break;
        case "Volume down":
            Volumedown(mode,player);      
            break;
        case "Pause":
            Pause(mode,player);
            break;
        case "Forward":
            Forward(mode,player);
            break;
        case "Backward":
            Backward(mode,player);
            break;
    }

    return;
});


function Mute(mode,player){

    if(mode == "Youtube"){
        if(player.isMuted()){
            player.unMute();
        }else{
            player.mute();
        }

    }else{
        player.muted = !player.muted;
    }
    
    return 
}
function Volumeup(mode,player){
    if(mode == "Youtube"){
        player.setVolume(player.getVolume()+5);
    }else{
        player.volume+=0.05;
    }
    showVolumeBar(mode,player);
    return
}
function Volumedown(mode,player){
    if(mode == "Youtube"){
        player.setVolume(player.getVolume()-5);
    }else{
        player.volume-=0.05;
    }
    showVolumeBar(mode,player);
    return   
}
function Pause(mode,player){
    if(mode == "Youtube"){
        if(document.getElementsByClassName("video-stream html5-main-video")[0].paused){
            player.playVideo();
        }else{
            player.pauseVideo();
        }
    }else{
        if(player.paused)
        {
            player.play();
        }else{
            player.pause();
        }
    }
    return
}
function Forward(mode,player){
    if(mode == "Youtube"){
        player.seekTo(player.getCurrentTime()+5);
    }else{
        player.currentTime+=5;
    }
    return
}
function Backward(mode,player){
    if(mode == "Youtube"){
        player.seekTo(player.getCurrentTime()-5);
    }else{
        player.currentTime-=5;
    }
    return
}


var firstVolChange = false;
var t = document.createTextNode(" ");

function showVolumeBar(mode,player)
{
    
    switch(mode){
        case "Youtube":
            player.wakeUpControls();
            document.getElementsByClassName("ytp-volume-area")[0].dispatchEvent(new MouseEvent('mouseover', { 'bubbles': true }));
            break;
        case "Twitch":
            /*
            volumebar = document.getElementsByClassName("ScRangeInput-sc-1qrd37x-0 jZQpag tw-range")[0];
            volumebar.dispatchEvent(new MouseEvent('mouseover', { 'bubbles': true }));
            volumebar.value = player.value;
            */
           
            if(!firstVolChange)
            {
                var p = document.getElementsByClassName("Layout-sc-nxg1ff-0 kEFnEs")[0];
                var h = document.createElement("H3");
                h.id = "volumeindicator";
                h.appendChild(t);
                p.appendChild(h);
                firstVolChange = true;
            }
            t.textContent = Math.round(player.volume*100).toString();

            break;
        case "Mako":
            if(!firstVolChange)
            {
                var p = document.getElementsByClassName("bottom")[1];
                console.log(p);
                var h = document.createElement("H3");
                h.id = "volumeindicator";
                h.appendChild(t);
                p.appendChild(h);
                firstVolChange = true;
            }
            t.textContent = Math.round(player.volume*100).toString();
            try{
                document.getElementsByClassName("controls off")[0].setAttribute("class","controls");
                setTimeout(function() {
                    document.getElementsByClassName("controls")[0].setAttribute("class","controls off");
                },3000);
            }
            catch{
                console.log(" ");
            }
            
    }

}