let childNodes = document.getElementsByTagName('body')[0].childNodes;
const addMouseoutEventAll = (children) => {
    if (children === undefined){
        return;
    }

    for (let i = 0; i < children.length; i++) {
        children[i].addEventListener("mouseout", function (event) {
            event.stopPropagation();
            if (!event.target.hasAttribute("selected") || !event.target.getAttribute("selected")) {
                event.target.style.backgroundColor = event.target.getAttribute("data-originBackgroundColor");
            }
        });
        addMouseoutEventAll(children[i].childNodes);
    }
}
addMouseoutEventAll(childNodes);