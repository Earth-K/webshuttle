window.oncontextmenu = function (event) {
    event.preventDefault();
}
let childNodes = document.getElementsByTagName('body')[0].childNodes;
const func = (c) => {
    if (c === undefined) return;
    for (let i = 0; i < c.length; i++) {
        c[i].addEventListener("mousedown", function (event) {
            if (event.which !== 3) return;
            let posTop = window.scrollY + event.clientY + 3;
            let posLeft = window.scrollX + event.clientX + 3;
            let wsTooltip = document.getElementById("ws-tooltip");
            wsTooltip.style.position = "absolute";
            wsTooltip.style.top = posTop.toString() + "px";
            wsTooltip.style.left = posLeft.toString() + "px";
            wsTooltip.style.display = "flex";
            wsTooltip.style.justifyContent = "center";
            wsTooltip.style.alignItems = "center";
            let wsTargetElement = document.getElementsByClassName(" ws-target-element")[0];
            if (wsTargetElement !== undefined) {
                wsTargetElement.style.backgroundColor = event.target.getAttribute("data-originBackgroundColor");
                wsTargetElement.setAttribute("selected", "false");
                let startIdx = wsTargetElement.className.indexOf(" ws-target-element");
                wsTargetElement.className = wsTargetElement.className.substring(0, startIdx);
            }
            event.target.className += " ws-target-element";
            event.stopPropagation();
        });
        func(c[i].childNodes);
    }
}
func(childNodes);