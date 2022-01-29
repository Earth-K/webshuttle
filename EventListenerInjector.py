class EventListenerInjector:

    def __init__(self, web_crawler):
        self._web_crawler = web_crawler

    def add_mouseover(self):
        script = ''' 
        let childNodes = document.getElementsByTagName('body')[0].childNodes;
        const func = (c) => {
          if(c==undefined) return;
          for(let i = 0 ; i<c.length; i++) {
            c[i].addEventListener("mouseover", function(event) {
                event.stopPropagation();
                event.target.style.border = "3px solid rgba(217,217,243,90)";
            });
            func(c[i].childNodes);
          }
        }
        func(childNodes);
        '''
        self._web_crawler.execute_js(script)

    def add_mouseleave(self):
        script = ''' 
        let childNodes = document.getElementsByTagName('body')[0].childNodes;
        const func = (c) => {
          if(c==undefined) return;
          for(let i = 0 ; i<c.length; i++) {
            c[i].addEventListener("mouseleave", function(event) {
                event.stopPropagation();
                event.target.style.border = "";
            });
            func(c[i].childNodes);
          }
        }
        func(childNodes);
        '''
        self._web_crawler.execute_js(script)

    def add_tooltip(self):
        script = ''' 
        let wsTooltip = document.createElement('div');
        wsTooltip.id = "ws-tooltip";
        wsTooltip.style.width = "100px";
        wsTooltip.style.height = "45px";
        wsTooltip.style.backgroundColor = "tomato";
        wsTooltip.style.display = "flex";
        wsTooltip.style.justifyContent = "center";
        wsTooltip.style.alignItems = "center";

        let wsBtn = document.createElement('button');
        wsBtn.id = "ws-select-btn";
        wsBtn.innerText = "선택";
        wsBtn.style.width = "50px";
        wsBtn.style.height = "30px"

        wsTooltip.appendChild(wsBtn);

        document.body.appendChild(wsTooltip);
        '''
        self._web_crawler.execute_js(script)

    def add_mousedown_right(self):
        script = ''' 
        window.oncontextmenu = function (event) {   event.preventDefault() }
        let childNodes = document.getElementsByTagName('body')[0].childNodes;
        const func = (c) => {
          if(c==undefined) return;
          for(let i = 0 ; i<c.length; i++) {
            c[i].addEventListener("mousedown", function(event) {
                if(event.which != 3) return;
                let posTop = window.scrollY + event.clientY+3;
                let posLeft = event.clientX+3;
                let wsTooltip = document.getElementById("ws-tooltip"); 
                wsTooltip.style.position = "absolute";
                wsTooltip.style.top = posTop.toString()+"px";
                wsTooltip.style.left = posLeft.toString()+"px";
                wsTooltip.style.display = "flex";
                wsTooltip.style.justifyContent = "center";
                wsTooltip.style.alignItems = "center";
                event.stopPropagation();
            });
            func(c[i].childNodes);
          }
        }
        func(childNodes);
        '''
        self._web_crawler.execute_js(script)