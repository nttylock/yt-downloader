document.addEventListener('DOMContentLoaded', function() {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    document.getElementById('url').value = tabs[0].url;
  });

  document.getElementById('extract').addEventListener('click', function() {
    var url = document.getElementById('url').value;
    var resultDiv = document.getElementById('result');
    resultDiv.innerHTML = 'Loading...';

    fetch('http://127.0.0.1:5000/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'url=' + encodeURIComponent(url)
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        resultDiv.innerHTML = '<p>Error: ' + data.error + '</p>';
      } else {
        var html = '<h3>Results:</h3>';
        html += '<a href="' + data.audio_url + '" class="download-link" target="_blank">Download audio (m4a, ' + data.audio_size + ')</a>';
        html += '<a href="' + data.video_url + '" class="download-link" target="_blank">Download video (' + data.video_ext + ', ' + data.video_size + (data.video_resolution ? ', ' + data.video_resolution : '') + ')</a>';
        resultDiv.innerHTML = html;
      }
    })
    .catch(error => {
      console.error('Error:', error);
      resultDiv.innerHTML = '<p>An error occurred while processing the request: ' + error.message + '</p>';
    });
  });
});