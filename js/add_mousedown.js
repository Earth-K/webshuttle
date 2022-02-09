window.oncontextmenu = function (event) {
    event.preventDefault();
}
const childNodes = document.getElementsByTagName('body')[0].childNodes;

function addEventRight(event) {
    const posTop = window.scrollY + event.clientY + 3;
    const posLeft = window.scrollX + event.clientX + 3;
    const wsTooltip = document.getElementById("ws-tooltip");
    wsTooltip.style.position = "absolute";
    wsTooltip.style.top = posTop.toString() + "px";
    wsTooltip.style.left = posLeft.toString() + "px";
    wsTooltip.style.display = "flex";
    wsTooltip.style.justifyContent = "center";
    wsTooltip.style.alignItems = "center";

    while (true) {
        const wsTargetElements = document.getElementsByClassName("ws-target-element");
        console.log(wsTargetElements)
        if (wsTargetElements.length === 0) {
            break;
        }
        for (let i = 0; i < wsTargetElements.length; i++) {
            wsTargetElements[i].style.backgroundColor = wsTargetElements[i].getAttribute("data-originBackgroundColor");
            wsTargetElements[i].setAttribute("selected", "false");
            const startIdx = wsTargetElements[i].className.indexOf(" ws-target-element");
            wsTargetElements[i].className = wsTargetElements[i].className.substring(0, startIdx);
        }
    }

    const wsTargetClassElements = document.getElementsByClassName(event.target.className);
    if (wsTargetClassElements.length === 0) {
        document.elementFromPoint(posTop - 3, posLeft - 3).className = " ws-target-element";
    } else {
        for (let i = 0; i < wsTargetClassElements.length; i++) {
            wsTargetClassElements[i].className += " ws-target-element";
        }
    }
    event.stopPropagation();
}

function addEventLeft(event) {
    const tooltip = document.getElementById('ws-tooltip');
    tooltip.style.display = "none";
}

const func = (c) => {
    if (c === undefined) return;
    for (let i = 0; i < c.length; i++) {
        c[i].addEventListener("mousedown", function (event) {
            switch (event.which) {
                case 1:
                    addEventLeft(event);
                    break;
                case 3:
                    addEventRight(event);
                    break;
            }
        });
        func(c[i].childNodes);
    }
}
func(childNodes);