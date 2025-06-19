const ws = new WebSocket("ws://localhost:8000/ws/comments/");

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    alert(data.message);
};

ws.onopen = function() {
    console.log("WebSocket connection opened");
};

ws.onclose = function() {
    console.log("WebSocket connection closed");
};

ws.onerror = function(error) {
    console.error("WebSocket error:", error);
};