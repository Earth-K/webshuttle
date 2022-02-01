let wsTooltip = document.createElement('div');
wsTooltip.id = "ws-tooltip";
wsTooltip.style.width = "100px";
wsTooltip.style.height = "45px";
wsTooltip.style.backgroundColor = "tomato";
wsTooltip.style.display = "none";
wsTooltip.style.justifyContent = "center";
wsTooltip.style.alignItems = "center";
wsTooltip.style.border = "1px solid";

let wsBtn = document.createElement('div');
wsBtn.id = "ws-select-btn";
wsBtn.innerText = "Select";
wsBtn.style.color = "white";
wsBtn.style.width = "100%";
wsBtn.style.height = "100%";
wsBtn.style.display = "flex";
wsBtn.style.cursor = "pointer";
wsBtn.style.justifyContent = "center";
wsBtn.style.alignItems = "center";

wsBtn.addEventListener("click", () => {
    let wsTargetElement = document.getElementsByClassName("ws-target-element")[0];
    wsTargetElement.style.border = "3px solid rgba(217,217,243,90)";
    wsTargetElement.setAttribute("selected", "true");
    console.log(wsTargetElement);
});

wsTooltip.appendChild(wsBtn);
document.body.appendChild(wsTooltip);