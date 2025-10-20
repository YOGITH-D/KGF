

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

async function sendPredictionRequest(event){
    event.preventDefault(); 
    
    // --- FIX IS HERE: Select the element that displays the result ---
    // You must select the element you want to update (e.g., the <h2> inside the result container)
    const resultContainerEle = document.querySelector('.result-container .prediction-message'); 
    
    // Ensure the selection was successful before continuing
    if (!resultContainerEle) {
        console.error("Critical Error: Cannot find the result display element ");
        alert("Cannot find result display element on the page. Check HTML.");
        return; // Stop the function if the element isn't found
    }

    let inputs =document.getElementsByClassName("text-box");
    let inputData=[];
    for(let i=0;i<inputs.length;i++){
        inputData.push(parseFloat(inputs[i].value) || 0);
    }

    const dataToSend = { input_data: inputData };
    const jsonPayload = JSON.stringify(dataToSend);

    resultContainerEle.textContent = "Calculating prediction...";
    
    // 3. Send the Request (Using Fetch API)
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: jsonPayload 
        });

        // --- Server Error Handling (e.g., 400, 500 status codes) ---
        if (!response.ok) {
            const errorResult = await response.json();
            
            // Throw an error that the catch block will handle
            throw new Error(`Server responded with status ${response.status}: ${errorResult.error || 'Unknown Server Error'}`);
        }

        // Parse the successful response body
        const result = await response.json();

        // --- Application Logic Handling (Server returned 200, but logic failed) ---
        if (result.success) {
            const finalPrediction = result.prediction.toFixed(4);
            
            // 4. Update the result container text with the final value
            resultContainerEle.textContent = `Predicted Final Recovery: ${finalPrediction}%`;
            
            // Call your function to display the result container
            showResult(); 

        } else {
            // If the server returned success: false, handle the specific error message
            throw new Error(result.error || 'Prediction failed due to unspecific model error.');
        }

    } catch (error) {
        // --- Network and Catch-All Error Handling ---
        console.error('Prediction Request Failed:', error);
        
        // Display user-friendly error message
        resultContainerEle.textContent = `Error: Prediction failed. Details: ${error.message}`;
        showResult(); // Ensure the result box is shown even with an error
        alert(`Prediction failed. Check console for details: ${error.message}`);
    }
}

// Attach the function to your button
const predictBtnEle = document.querySelector('.predict-btn');
predictBtnEle.addEventListener('click', sendPredictionRequest);
