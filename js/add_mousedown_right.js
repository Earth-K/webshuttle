window.oncontextmenu = function (event) {
    event.preventDefault();
}
const childNodes = document.getElementsByTagName('body')[0].childNodes;
const func = (c) => {
    if (c === undefined) return;
    for (let i = 0; i < c.length; i++) {
        c[i].addEventListener("mousedown", function (event) {
            if (event.which !== 3) return;
            const posTop = window.scrollY + event.clientY + 3;
            const posLeft = window.scrollX + event.clientX + 3;
            const wsTooltip = document.getElementById("ws-tooltip");
            wsTooltip.style.position = "absolute";
            wsTooltip.style.top = posTop.toString() + "px";
            wsTooltip.style.left = posLeft.toString() + "px";
            wsTooltip.style.display = "flex";
            wsTooltip.style.justifyContent = "center";
            wsTooltip.style.alignItems = "center";
            const wsTargetElement = document.getElementsByClassName(" ws-target-element")[0];
            if (wsTargetElement !== undefined) {
                wsTargetElement.style.backgroundColor = event.target.getAttribute("data-originBackgroundColor");
                wsTargetElement.setAttribute("selected", "false");
                const startIdx = wsTargetElement.className.indexOf(" ws-target-element");
                wsTargetElement.className = wsTargetElement.className.substring(0, startIdx);
            }
            event.target.className += " ws-target-element";
            event.stopPropagation();
        });
        func(c[i].childNodes);
    }
}
func(childNodes);