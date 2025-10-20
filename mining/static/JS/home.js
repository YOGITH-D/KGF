const bgEle=document.querySelector('.background-img-div');

window.addEventListener("scroll",()=>{
    updateImage();
});

function updateImage(){
    bgEle.style.opacity=1-window.pageYOffset/650;
    bgEle.style.backgroundSize = 160 - window.pageYOffset / 12 + "%";
}


const sidebarEle=document.querySelector('.sidebar-div');
const featureEle=document.querySelector('.home-text-div1');
const cancelEle=document.querySelector('.cancel');

let issidebaropen=false;
cancelEle.addEventListener("click",(event)=>{
    event.preventDefault();
    sidebarOpen();
});

featureEle.addEventListener("click",(event)=>{
    event.preventDefault();
    sidebarOpen();
});

function sidebarOpen(){
    if(issidebaropen){
        sidebarEle.style.transform="translateX(-105%)";
        cancelEle.style.transform="translateX(-400px)";
    }else{
        sidebarEle.style.transform="translateX(0%)";
        cancelEle.style.transform="translateX(0%)";
    }
    issidebaropen=!issidebaropen;
}


//display link contents
function toggleContent(event, selector) {
    event.preventDefault();
    const element = document.querySelector(selector);
    if (element.style.display === "block") {
        element.style.display = "none";
    } else {
        element.style.display = "block";
    }
}