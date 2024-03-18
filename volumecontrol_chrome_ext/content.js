
chrome.runtime.onMessage.addListener(gotMessage);

var script = document.createElement('script');
script.src = chrome.runtime.getURL('injected.js');
(document.head||document.documentElement).appendChild(script)

function gotMessage(message,sender,sendResnpose)
{
    
    console.log("Sending Message");
    window.postMessage(message,"*");
    
    return;
}


