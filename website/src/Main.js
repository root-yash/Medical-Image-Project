import './Main.css'
import Experience from './Experience/Experience'

function main(){
    const canvas = document.querySelector("#canvas")
    const canvasImage = document.querySelector("#canvasImage")
    const canvasText = document.querySelector("#canvasText")
    new Experience(canvas, canvasImage, canvasText)
}

main()

