import EventEmitter from "../Utils/EventEmitter"
import ApiResultImage from "../../API/ApiResult"

export default class onlyImage extends EventEmitter{
    constructor(canvas, canvasImage){
        super()
        this.canvas = canvas 
        this.canvasImage = canvasImage
        this.organ = null
        this.setup(canvas)
    }

    setup(){
        const ctx = this.canvas.getContext('2d');
    
        // Create dropdowns
        this.organ = document.createElement('select');
        
        // Populate dropdowns
        const options = ['None', 'kidney', 'largeintestine', 'lung', 'prostate', 'spleen'];
        for (let i = 0; i < options.length; i++) {
            const option = document.createElement('option')
            option.value = options[i]
            option.text = options[i]
            this.organ.appendChild(option)
        }
        
        // Position dropdowns on canvas
        this.organ.style.position = 'absolute'
        this.organ.style.top = '100px'
        this.organ.style.left = '50px'
        
        // Add dropdowns to canvas
        canvas.parentNode.appendChild(this.organ);
        this.organ.addEventListener("change", () => {
            const submit = document.createElement("submit")

            const input = document.createElement("input")
            input.name = "upload"
            input.type = "file"
            input.accept = "image/*"

            canvas.parentNode.appendChild(input)  
            input.style.position = 'absolute'
            input.style.top = '130px'
            input.style.left = '50px' 
            
            canvas.parentNode.appendChild(submit)
            submit.innerHTML = "Upload Image"
            submit.style.position = 'absolute'
            submit.style.top = '160px'
            submit.style.left = '50px'

            console.log("ok")

            submit.addEventListener("click", () => {
                this.toDataURL(URL.createObjectURL(input.files[0]), (dataUrl)=>{
                    this.image = dataUrl 
                    console.log(this.image)
                    this.apiresult = new ApiResultImage(this.image, this.organ.value)
                    this.apiresult.on("resultRecieved",()=>{
                        this.setupImage()
                        this.getResult()
                    }) 
                    
                })
            })
        })
    }

    getResult() { 
        this.result = 'data:image/jpeg;base64,' + JSON.parse(this.apiresult.result)["Result"].split('"')[1]
        console.log(this.result)

        const imageFrame = document.createElement("img")

        imageFrame.style = `border-radius: 12px; width:35%; position:absolute; top:200px; left: 50px`
        imageFrame.id = 'ClassImage'
        imageFrame.src = this.result

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