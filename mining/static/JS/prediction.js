const btnEle=document.querySelector('.predict-btn');

btnEle.addEventListener("mousemove",(event)=>{
    btnEle.style.setProperty("--mouse-y",event.offsetY+"px");
    btnEle.style.setProperty("--mouse-x",event.offsetX+"px");
})




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
        sidebarEle.style.transform="translateX(-100%)";
        cancelEle.style.transform="translateX(-400px)";
    }else{
        sidebarEle.style.transform="translateX(0%)";
        cancelEle.style.transform="translateX(0%)";
    }
    issidebaropen=!issidebaropen;
}

const resultdivEle=document.querySelector('.result-container');
const cancelResultEle=document.querySelector('.cancel-result');
cancelResultEle.addEventListener("click",(event)=>{
    event.preventDefault();
    disableResult();
})

let isresultdivopen=false;
function disableResult(){
    if(isresultdivopen){
        resultdivEle.style.display="none";
        document.body.classList.remove("no-scroll");
    }else{
        resultdivEle.style.display="block";
        document.body.classList.add("no-scroll");
    }
    isresultdivopen=!isresultdivopen;
}

function showResult(){
    resultdivEle.style.display="block";
    isresultdivopen=true;
    document.body.classList.add("no-scroll");
}