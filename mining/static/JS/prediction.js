
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



async function sendPredictionRequest(event){
    event.preventDefault(); 
    const resultContainerEle = document.querySelector('.modal-body .prediction-message'); 
    const modalElement = document.getElementById('exampleModal');  

    if (!resultContainerEle || !modalElement) {
        console.error("Critical Error: Cannot find required display elements.");
        alert("Cannot find result display elements on the page. Check HTML IDs/Classes.");
        return;
    }

    let inputs =document.getElementsByClassName("text-box");
    let inputData=[];
    for(let i=0;i<inputs.length;i++){
        inputData.push(parseFloat(inputs[i].value) || 0);
    }

    const dataToSend = { input_data: inputData };
    const jsonPayload = JSON.stringify(dataToSend);
    resultContainerEle.textContent = "Calculating prediction...";
    
    $('#exampleModal').modal('show'); 
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: jsonPayload 
        });

        if (!response.ok) {
            const errorResult = await response.json();
            throw new Error(`Server responded with status ${response.status}: ${errorResult.error || 'Unknown Server Error'}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            const finalPrediction = result.prediction.toFixed(4);
            resultContainerEle.textContent = `Expected silica conc: ${finalPrediction}%`;
        } else {
            throw new Error(result.error || 'Prediction failed due to unspecific model error.');
        }

    } catch (error) {
        console.error('Prediction Request Failed:', error);
        resultContainerEle.textContent = `Error: Prediction failed. Details: ${error.message}`;
        alert(`Prediction failed. Check console for details: ${error.message}`);
    }
}

const predictBtnEle = document.querySelector('.btn-outline-danger');
predictBtnEle.addEventListener('click', sendPredictionRequest);
