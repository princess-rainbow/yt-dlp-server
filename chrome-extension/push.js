var URL = location.href;
var xmlhttp = new XMLHttpRequest();
// console.log(URL);

xmlhttp.onreadystatechange = function() {
  if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
    chrome.runtime.sendMessage({closeThis: true});
  } else if (xmlhttp.readyState == 4) {
  }
}
xmlhttp.open('POST', 'https://__HOSTNAME__:8801/', true);
xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xmlhttp.send('url=' + encodeURIComponent(URL));