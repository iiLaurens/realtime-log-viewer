from bottle import default_app, route, run
import wsgiserver
from time import sleep

@route('/log.html')
def hello():
    yield log_page_head
    for line in follow_log('file.log'):
        yield line + '<br/>'

@route('/')
def main():
    return "<b>Below is a live log:</b></br></br><iframe src='http://localhost:8080/log.html' style='display: block; width: 800px; height: 400px; align: center;'></iframe>"

def follow_log(filepath):
    thefile = open(filepath,"r")
    # thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            sleep(0.1)
        else:
            yield line

log_page_head = """
     <head>
    <style>
    body {
        font-family: "Lucida Console", Monaco, monospace;
        background-color: black;
        color: white;
        overflow-y: scroll;
    }

    #FloatButton {
        display: none;
        position: fixed;
        bottom: 20px;
        right: 30px;
        z-index: 99;
        border: none;
        outline: none;
        background-color: Grey;
        color: LightGrey;
        cursor: pointer;
        padding: 8px;
        border-radius: 4px;
        font-weight: bold;
    }

    #FloatButton:hover {
        background-color: #555;
    }
    </style>

      <script type="text/javascript">
        var stickToBottom;
        var interval;

        function onFloatButton() {
            if (stickToBottom) {
                stopStick();
            } else {
                startStick();
            }
        }

        function stopStick() {
            stickToBottom = false;
            clearInterval(interval);
            document.getElementById("FloatButton").style.display = "block";
        }

        function startStick() {
            stickToBottom = true;
            interval = setInterval(autoScrolling, 10); 
            document.getElementById("FloatButton").style.display = "none";
        }

        function autoScrolling() {
            window.scrollTo(0,document.body.scrollHeight);
        }

        window.onscroll = function(e) {
            if (stickToBottom && this.oldScroll > this.scrollY){
                console.log('Up scroll detected, aborting auto scroll');
                stopStick();
            }
            
            this.oldScroll = this.scrollY;
        }

        startStick();
      </script>
      </head>
      
      <button onclick="onFloatButton()" id="FloatButton" title="Stick to bottom">Stick to bottom</button>
      """

wsgiapp = default_app()
httpd = wsgiserver.Server(wsgiapp)
httpd.serve_forever()

