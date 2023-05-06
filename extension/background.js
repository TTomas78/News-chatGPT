chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
  if (msg.name == 'getAll'){
    fetch('http://localhost:8000/get-all-news/infobae?words_number='+msg.wordsNumber+'&language='+msg.language+'&soft_limit='+msg.softLimit)
    .then(response => response.json())
    .then(data =>{
      data.news.forEach(function(data) {
        data.summary = data.summary.replace(/\\"/g, '"');
      });
      sendResponse(data)
  })
    .catch(error => {
      sendResponse(error);
    });
  }
  if (msg.name == 'getOne'){
    fetch('http://localhost:8000/get-one-news/infobae?link='+msg.link+'&words_number='+msg.wordsNumber+'&language='+msg.language+'&soft_limit='+msg.softLimit)
    .then(response => response.json())
    .then(data =>{
    if (data.error == undefined){
      data.summary = data.summary.replace(/\\"/g, '"');
    }
    sendResponse(data)
  })
    .catch(error => {
      sendResponse(error);
    });
  }
  return true;
});