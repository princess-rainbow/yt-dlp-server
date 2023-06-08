chrome.action.onClicked.addListener(tab => {
    console.log(tab.url);
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ["push.js"]
    });
});

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.closeThis) chrome.tabs.remove(sender.tab.id);
});
