import EventEmitter from "../Utils/EventEmitter"
import ApiResultImage from "../../API/ApiResult"
import ApiResultText from "../../API/apiResultText"

export default class onlyText extends EventEmitter{
    constructor(canvas, type){
        super()
        this.canvas = canvas 
        this.type = type
        this.setup(canvas)
    }

    setup(){
        const ctx = this.canvas.getContext('2d')
        
        const submit = document.createElement("submit")

        const input = document.createElement("input")
        input.name = "upload"
        input.type = "file"
        input.accept = "image/*"

        canvas.parentNode.appendChild(input)  
        input.style.position = 'absolute'
        input.style.top = '250px'
        input.style.left = '50px' 
        
        canvas.parentNode.appendChild(submit)
        submit.innerHTML = "Upload Image"
        submit.style.position = 'absolute'
        submit.style.top = '280px'
        submit.style.left = '50px'

        console.log("ok")

        submit.addEventListener("click", () => {
            this.toDataURL(URL.createObjectURL(input.files[0]), (dataUrl)=>{
                this.image = dataUrl 
                console.log(this.image)
                this.apiresult = new ApiResultText(this.image, this.type)
                this.apiresult.on("resultRecieved",()=>{
                    this.setupImage()
                    this.getResult()
                }) 
                
            })
        })
    }

    getResult() { 
        this.result = 'data:image/bmp;base64,' + JSON.parse(this.apiresult.result)["Result"].split('"')[1]
        console.log(this.result)

        const imageFrame = document.createElement("img")

        imageFrame.style = `border-radius: 12px; width:50%; align: center;right: block;margin-left: auto;margin-right: auto;`
        imageFrame.id = 'ClassImage'
        imageFrame.src = this.image

        this.canvas.parentNode.appendChild(imageFrame)
        // this.canvas.parentNode.appendChild(this.imageFrame)
        // this.imageFrame.src = this.result
    }

    setupImage(){
        
    }

    toDataURL(url, callback) {
        var xhr = new XMLHttpRequest();
        xhr.onload = function() {
          var reader = new FileReader();
          reader.onloadend = function() {
            callback(reader.result);
          }
          reader.readAsDataURL(xhr.response);
        };
        xhr.open('GET', url);
        xhr.responseType = 'blob';
        xhr.send();
    }
}