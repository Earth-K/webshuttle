let wsTooltip = document.createElement('div');
wsTooltip.id = "ws-tooltip";
wsTooltip.style.width = "100px";
wsTooltip.style.height = "45px";
wsTooltip.style.backgroundColor = "tomato";
wsTooltip.style.display = "none";
wsTooltip.style.justifyContent = "center";
wsTooltip.style.alignItems = "center";

let wsBtn = document.createElement('button');
wsBtn.id = "ws-select-btn";
wsBtn.innerText = "Select";
wsBtn.style.width = "50px";
wsBtn.style.height = "30px";

wsBtn.addEventListener("click", () => {
    let wsTargetElement = document.getElementsByClassName("ws-target-element")[0];
    console.log(wsTargetElement);
});

wsTooltip.appendChild(wsBtn);
document.body.appendChild(wsTooltip);