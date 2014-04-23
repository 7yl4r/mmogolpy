<!--
<link href="css/barebones.css" rel="stylesheet" type="text/css" />
-->
<!DOCTYPE html>
    <head>
        <script type="text/javascript">
            function parseMessage(m){
                // interprets and carries out messages
                var mes = m.split(" ");
                var act = mes[0];
                var row = mes[1];
                var col = mes[2];
                var dat = mes[3];
                
                if (act == "set"){
                    var el = document.getElementById('R'+row+'C'+col);
                    el.innerHTML = dat;
                    el.style.color = "rgb(200,255,100)";
                } else if (act == "ERR:"){
                    console.log("server-side error: "+m);
                } else if (act == "confirm"){
                    console.log("confirmed: "+dat);
                } else if (act == "update"){
                    var el = document.getElementById('R'+row+'C'+col);
                    el.innerHTML = dat;
                    el.style.color = "rgb(150,150,150)";
                } else if (act == "pause"){
                    document.getElementById('countDown').innerHTML = dat;
                } else {
                    console.log("ERR: unknown message to client: "+m);
                }
            }
        
            var ws = new WebSocket("ws://{{DOMAIN}}/websocket");
                ws.onopen = function() {
                    ws.send("Hello None None {{client_id}}");
            };
            ws.onmessage = function (evt) {
                parseMessage(evt.data);
            };
            ws.onclose = function (){
                ws.send("goodbye None None {{client_id}}");
            };
        </script>
    </head>
    <body>
        <tt> 
            <p>
                You have <span id="countDown">{{timeLeft}}</span>s until the next cell generation. <a href="#edit_req" id="edit_request">Request 10s pause to edit cells.<a>
                <script type="text/javascript">

                    var edit_button = document.getElementById('edit_request');

                    edit_button.addEventListener('click', function (e)
                    {
                        e = e || window.event; //? what is this?

                        ws.send("pause None None 10");

                        e.preventDefault(); //? what is that?
                    }, false);
                    
                </script>
                
            </p>
            <h1>
                % n_row = 0
                % n_col = 0
                % for row in cellList:
                    <p>
                        % for cell in row:
                            <a href="#R{{n_row}}C{{n_col}}" id="R{{n_row}}C{{n_col}}">
                                {{cell}}
                            <a>
                            % include('tpl/js/clickState',row=n_row,col=n_col)
                            % n_col+=1
                        % end
                    </p>
                    % n_row+=1
                    % n_col =0
                % end
            </h1>
            <p>
                {{len(cellList)*len(cellList[0])}} cells shown in {{n_row}} rows and {{len(cellList[0])}} cols.
            </p>
        </tt> 

        <script src="js/countdown.js" type="text/javascript" onload="setInterval(uCountdown,1000)"></script>
    </body>
</html>