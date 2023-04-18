import EventEmitter from '../Experience/Utils/EventEmitter.js'
import onlyImage from './DifferentModel/onlyImage.js'
import onlyText from './DifferentModel/onlyText.js'

let instance = null

export default class Experience extends EventEmitter
{
    constructor(canvas0, canvasImage, canvasText)
    {
        super()
        this.whichScene = 0
        // Singleton
        if(instance)
        {
            return instance
        }

        instance = this

        // if the 
        
        // Global access
        window.experience = this

        // Options
        this.canvas = canvas0
        this.canvasImage = canvasImage
        this.canvasText = canvasText
        

        // setup 
        this.setup(canvas)

    }

    setup(canvas){
        const ctx = canvas.getContext('2d');
    
        // Create dropdowns
        const dropdown1 = document.createElement('select');
        
        // Populate dropdowns
        const options = ['None', 'HPA/Hubmap Segmentation', 'Brats Malignant Tumor Value', 'Check Leukaemia', 'Check Xray for Chest Disease'];
        for (let i = 0; i < options.length; i++) {
            const option = document.createElement('option');
            option.value = options[i];
            option.text = options[i];
            dropdown1.appendChild(option);
        }
        
        // Position dropdowns on canvas
        dropdown1.style.position = 'absolute';
        dropdown1.style.top = '50px';
        dropdown1.style.left = '50px';
        
        // Add dropdowns to canvas
        canvas.parentNode.appendChild(dropdown1);
        dropdown1.addEventListener("change", () => {
            if (dropdown1.value == "HPA/Hubmap Segmentation"){
                this.onlyImage = new onlyImage(this.canvas, this.canvasImage)
            }else if(dropdown1.value != "None"){
                this.onlyText = new onlyText(this.canvas, dropdown1.value)
                console.log
            }
            console.log(dropdown1.value)
        })
    }
}