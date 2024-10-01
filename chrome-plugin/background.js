chrome.runtime.onInstalled.addListener(function() {
  console.log('YouTube URL Extractor installed');
});

// Добавляем пустой обработчик для поддержки сервис-воркера
self.addEventListener('fetch', function(event) {});