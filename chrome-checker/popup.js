document.getElementById("manualCheck").addEventListener("click", () => {
  chrome.tabs.create({ url: "https://127.0.0.1:5555/index" });  
});
