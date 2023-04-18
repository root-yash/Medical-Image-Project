import EventEmitter from "../Experience/Utils/EventEmitter";

export default class ApiResultImage extends EventEmitter{

    constructor(image_base64, organ){
        
        super()
        image_base64 = image_base64.split(',')[1]

        const headersList = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.com)",
            "x-api-key": "sleeDuaVS956oTzbHOzh6awXLB6sDviM4vCgZaP1",
            "Content-Type": "application/json"
           }
           
        const bodyContent = JSON.stringify({
            "Image": image_base64,
            "Organ": organ
        });
        
        fetch("https://lrblt6nnp4.execute-api.ap-south-1.amazonaws.com/beta/tissue",{
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

