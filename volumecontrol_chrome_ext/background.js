//chrome.action.onClicked.addListener(buttonClicked)
//const confurl = chrome.runtime.getURL('conf.json')
/*
function buttonClicked(tab){
    fetch(confurl)
    .then((response) => response.json()) 
    .then(json => send2Tab(tab,json));
    
}
*/

const urlDict = {
    "Youtube": "https://www.youtube.com/watch*",
    "Twitch" : "https://www.twitch.tv/*",
    "Mako" : "https://www.mako.co.il/*",
    "Netflix" : "https://www.netflix.com/*",
    "Kan" : "https://www.kan.org.il/*"
}
const blackListedURL = new RegExp(["https://www.twitch.tv/directory.*","https://www.netflix.com/browse.*"].join('|'))
var currentMode = "Youtube";
var tabInd = 0;

async function send2Tab(cmd)
{
    var mode = cmd.Mode;
    var command = cmd.Command;

    tab = await getTargetTab(mode);
    if(tab != undefined)
    {
        console.log(tab.url)
        chrome.tabs.sendMessage(tab.id,cmd);
    }
    return;
}


async function getTargetTab(name) //Returns tab object that corresponds to the name of the media website
{
    let queryOptions = {url : urlDict[name]};
    let tabs = await chrome.tabs.query(queryOptions);

    if(tabs.length == 0){ //If there are no tabs that corresponsd to the media website return undefined
        return undefined 
    }

    filteredTabs = filterBlackListedURLS(tabs) 
    tabInd = tabInd%filteredTabs.length;
    console.log(tabInd);
    return filteredTabs[tabInd]
}


function filterBlackListedURLS(tabs){ //Returns array of tabs which dont have a url that is blacklisted
    var filteredTabs = [];
    var counter = 0;
    for(let i = 0; i < tabs.length; i++)
    {
        if(blackListedURL.exec(tabs[i].url) == null){
            filteredTabs[counter] = tabs[i];
            counter+=1;
        }
    }
    return filteredTabs
}

console.log("Sending:ping");
var port = chrome.runtime.connectNative("pyserver");
port.postMessage("ping");

port.onMessage.addListener(function(message){

    console.log(message);
    if(message == "pong"){ //Used to keep background script running and not closed by chrome
        console.log("test");
        return;
    }
    
    if(("Mode" in message)){ 
        currentMode = message["Mode"];
        tabInd = 0;
    }
    if("Command" in message){

        if(message["Command"] == "Tab cycle")
        {
            tabInd += 1;
        }else{
            message["Mode"] = currentMode;
            send2Tab(message);
        }
    }
    
    return;
})

port.onDisconnect.addListener(function() {
    console.log("Disconnected");
  });
/*
port.onDisconnect.addListener(function(port) {
    console.log("Disconnected");
	port = chrome.runtime.connectNative("pyserver");
  });
*/


chrome.tabs.onUpdated.addListener(updateOpenTabs);

function updateOpenTabs(tabID,changeinfo,tab){
    /*
    if("status"  in changeInfo){
        if(changeinfo["status"] == "complete")
        {
            console.log(tabID);
            console.log(changeInfo)
        }
    }
    */
   console.log(tabID)
}
