html = """
<!DOCTYPE html>
<html>
<head>
    <title>Message</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">

    <style>
        h1 {
            color: #6a0dad;
            font-size: 32px;
            font-family: Arial, sans-serif;
            font-weight: bold;
            text-align: center;
            text-transform: uppercase;
            margin-top: 20px;
            margin-bottom: 20px;
        }

        h4 {
            color: #6a0dad;
            font-size: 18px;
            font-family: Arial, sans-serif;
            font-weight: bold;
            text-transform: uppercase;
            text-decoration: underline;
        }

        .form-control {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #d8b9ff;
            border-radius: 5px;
            box-sizing: border-box;
        }

        .btn {
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            background-color: #6a0dad;
            color: white;
            cursor: pointer;
        }

        .btn:hover {
            background-color: #d8b9ff;
        }

         #messages li {
        font-size: 22px; /* Adjust the font size to your preference */
    }
    </style>
</head>
<body>
<div class="container mt-3">
    <h1>Message</h1>
    <h4>User ID: <span id="ws-id"></span></h4>
    <form action="" onsubmit="sendMessage(event)">
        <input type="text" class="form-control" id="messageText" autocomplete="off"/>
        <button class="btn btn-outline-primary mt-2">Send</button>
    </form>
    <ul id='messages' class="mt-5">
    </ul>
</div>

<script>
    var client_id = Date.now()
    document.querySelector("#ws-id").textContent = client_id;
    var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
    ws.onmessage = function(event) {
        var messages = document.getElementById('messages')
        var message = document.createElement('li')
        var content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
    };
    function sendMessage(event) {
        var input = document.getElementById("messageText")
        ws.send(input.value)
        input.value = ''
        event.preventDefault()
    }
</script>
</body>
</html>

"""