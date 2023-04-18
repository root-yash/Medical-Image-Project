import EventEmitter from "./EventEmitter"

export default class ImageBrowse extends EventEmitter{
    constructor(canvas){
        super()
        let input = document.createElement("input")
        input.name = "upload"
        input.type = "file"
        input.accept = "image/*"
        input.click()
        input.addEventListener("change",()=>{
            this.toDataURL(URL.createObjectURL(input.files[0]), (dataUrl)=>{
                this.image = dataUrl 
                this.trigger("imageUploaded")
            })
        })
        canvas.parentNode.appendChild(input)   
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