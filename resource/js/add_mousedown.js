const WS_TARGET_ELEMENT = "ws-target-element";

window.oncontextmenu = function (event) {
    event.preventDefault();
}
const childNodes = document.getElementsByTagName('body')[0].childNodes;
addMousedownEventAll(childNodes);


function addMousedownEventAll(children) {
    if (children === undefined) return;
    for (let i = 0; i < children.length; i++) {
        children[i].addEventListener("mousedown", function (event) {
            switch (event.which) {
                case 1:
                    addEventLeft(event);
                    break;
                case 3:
                    showTooltip();
                    deselectArea();
                    addEventRight(event);
                    break;
            }
        });
        addMousedownEventAll(children[i].childNodes);
    }
}
function addEventLeft(event) {
    const tooltip = document.getElementById('ws-tooltip');
    tooltip.style.display = "none";
}
function showTooltip() {
    const posTop = window.scrollY + event.clientY + 3;
    const posLeft = window.scrollX + event.clientX + 3;
    const wsTooltip = document.getElementById("ws-tooltip");
    wsTooltip.style.position = "absolute";
    wsTooltip.style.top = posTop.toString() + "px";
    wsTooltip.style.left = posLeft.toString() + "px";
    wsTooltip.style.display = "flex";
    wsTooltip.style.justifyContent = "center";
    wsTooltip.style.alignItems = "center";
}
function deselectArea() {
    while (true) { // 한 번만 수행하면 일부 엘리먼트 선택이 해제되지 않음
        const wsTargetElements = document.getElementsByClassName(WS_TARGET_ELEMENT);
        console.log(wsTargetElements)
        if (wsTargetElements.length === 0) {
            break;
        }
        for (let i = 0; i < wsTargetElements.length; i++) {
            wsTargetElements[i].style.backgroundColor = wsTargetElements[i].getAttribute("data-originBackgroundColor");
            wsTargetElements[i].setAttribute("selected", "false");
            if (wsTargetElements[i].classList.contains(WS_TARGET_ELEMENT)) {
                wsTargetElements[i].classList.remove(WS_TARGET_ELEMENT);
            }
        }
    }
}
function addEventRight(event) {
    const wsTargetClassElements = document.getElementsByClassName(event.target.className);
    if (wsTargetClassElements.length === 0) {
        document.elementFromPoint(posTop - 3, posLeft - 3).classList.add(WS_TARGET_ELEMENT);
    } else {
        for (let i = 0; i < wsTargetClassElements.length; i++) {
            wsTargetClassElements[i].classList.add(WS_TARGET_ELEMENT);
        }
    }
    event.stopPropagation();
}

