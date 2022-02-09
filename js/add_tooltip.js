let wsTooltip = document.createElement('div');
wsTooltip.id = "ws-tooltip";
wsTooltip.style.width = "150px";
wsTooltip.style.height = "45px";
wsTooltip.style.backgroundColor = "tomato";
wsTooltip.style.display = "none";
wsTooltip.style.justifyContent = "center";
wsTooltip.style.alignItems = "center";
wsTooltip.style.border = "1px solid";
wsTooltip.setAttribute('data-click-log', '');

let selectBtn = document.createElement('div');
selectBtn.id = "ws-select-btn";
selectBtn.innerText = "Select";
selectBtn.style.color = "white";
selectBtn.style.flexGrow = "1";
selectBtn.style.height = "100%";
selectBtn.style.borderRight = "1px solid black";
selectBtn.style.display = "flex";
selectBtn.style.cursor = "pointer";
selectBtn.style.justifyContent = "center";
selectBtn.style.alignItems = "center";

const selectPoint = () => {
    const wsTargetElement = document.getElementsByClassName("ws-target-element")[0];
    wsTargetElement.style.backgroundColor = "rgba(217,217,243,0.5)";
    wsTargetElement.setAttribute("selected", "true");
    console.log(wsTargetElement);
}

const selectClass = (className) => {
    const wsTargetElements = document.getElementsByClassName(className);
    for (let i = 0; i < wsTargetElements.length; i++) {
        wsTargetElements[i].style.backgroundColor = "rgba(217,217,243,0.5)";
        if(wsTargetElements[i].className.indexOf("ws-target-element") === -1) {
            wsTargetElements[i].className += " ws-target-element";
        }
        wsTargetElements[i].setAttribute("selected", "true");
        console.log(wsTargetElements[i]);
    }
}
selectBtn.addEventListener("click", () => selectClass("ws-target-element"));

let clickBtn = document.createElement('div');
clickBtn.id = "ws-click-btn";
clickBtn.innerText = "Click";
clickBtn.style.color = "white";
clickBtn.style.flexGrow = "1";
clickBtn.style.height = "100%";
clickBtn.style.display = "flex";
clickBtn.style.cursor = "pointer";
clickBtn.style.justifyContent = "center";
clickBtn.style.alignItems = "center";
clickBtn.style.borderRight = "1px solid black";

clickBtn.addEventListener("click", () => {
    const ws_tooltip = document.getElementById("ws-tooltip");
    const tooltip_rect = ws_tooltip.getBoundingClientRect();
    const targetElementX = tooltip_rect.left - 3;
    const targetElementY = tooltip_rect.top - 3;
    const scrollY = window.scrollY;
    const scrollX = window.scrollX;
    const lastClickPos = '(' + targetElementX + '+' + scrollX + ',' + targetElementY + '+' + scrollY + ')';
    console.log(targetElementX + ", " + targetElementY);
    console.log(document.elementFromPoint(targetElementX, targetElementY));
    wsTooltip.setAttribute('data-click-log', lastClickPos);
});

let parentSelectBtn = document.createElement('div')
parentSelectBtn.id = "ws-parent-select-btn";
parentSelectBtn.innerText = "Parent\nSelect";
parentSelectBtn.style.color = "white";
parentSelectBtn.style.flexGrow = "1";
parentSelectBtn.style.height = "100%";
parentSelectBtn.style.display = "flex";
parentSelectBtn.style.cursor = "pointer";
parentSelectBtn.style.justifyContent = "center";
parentSelectBtn.style.alignItems = "center";

let parentSelect = () => {
    const ws_tooltip = document.getElementById("ws-tooltip");
    const tooltip_rect = ws_tooltip.getBoundingClientRect();
    const targetElementX = tooltip_rect.left - 3;
    const targetElementY = tooltip_rect.top - 3;
    const target_element = document.elementFromPoint(targetElementX, targetElementY)
    selectClass(target_element.parentElement.className)
}
parentSelectBtn.addEventListener('click', parentSelect);


wsTooltip.appendChild(selectBtn);
wsTooltip.appendChild(clickBtn);
wsTooltip.appendChild(parentSelectBtn);
document.body.appendChild(wsTooltip);