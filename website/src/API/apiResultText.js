import EventEmitter from "../Experience/Utils/EventEmitter";

export default class ApiResultText extends EventEmitter{

    constructor(image_base64, type){
        
        super()
        image_base64 = image_base64.split(',')[1]

        const weblink = {
            'Brats Malignant Tumor Value': "brain", 
            'Check Leukaemia': "leukaemia", 
            'Check Xray for Chest Disease': "chest"
        }

        const headersList = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.com)",
            "x-api-key": "sleeDuaVS956oTzbHOzh6awXLB6sDviM4vCgZaP1",
            "Content-Type": "application/json"
           }
           
        const bodyContent = JSON.stringify({
            "Image": image_base64,
        });
        
        fetch(`https://lrblt6nnp4.execute-api.ap-south-1.amazonaws.com/beta/${weblink[type]}`,{
            method:"POST",
            body: bodyContent,
            headers: headersList
        }).then((response)=>{
            return response.text()
        }).then((data)=>{
            this.result = data
            this.trigger("resultRecieved")
        })
    } 
}

