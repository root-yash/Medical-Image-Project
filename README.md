# Medical Image Project



## Getting Started

### Body Parts
* Brain 
* Chest
* Blood
* Tissue


### In Chest: 
* Atelectasis
* Consolidation
* Infiltration
* Pneumothorax
* Edema
* Emphysema
* Fibrosis
* Effusion
* Pneumonia
* Pleural thickening
* Cardiomegaly
* Nodule Mass
* Hernia
* Tuberculosis

### In Brain:
* Brain tumour

### In Blood:
* Leukaemia

### Segment of functional tissue units:
* Kidney
* Lungs
* Spleen
* Prostate
* Intestine

### Dataset
* [NIH Chest X-rays](https://www.kaggle.com/datasets/nih-chest-xrays/data): This NIH Chest X-ray Dataset is comprised of 112,120 X-ray images with disease labels from 30,805 unique patients.    
* [Tuberculosis (TB) Chest X-ray Database](https://www.kaggle.com/datasets/tawsifurrahman/tuberculosis-tb-chest-xray-dataset): A team of researchers from Qatar University, Doha, Qatar, and the University of Dhaka, Bangladesh along with their collaborators from Malaysia in collaboration with medical doctors from Hamad Medical Corporation and Bangladesh have created a database of chest X-ray images for Tuberculosis (TB) positive cases along with Normal images. In our current release, there are 700 TB images publicly accessible and 2800 TB images can be downloaded from NIAID TB portal[3] by signing an agreement, and 3500 normal images.
* [Brain Tumor Segmentation Dataset](http://braintumorsegmentation.org/): BraTS has always been focusing on the evaluation of state-of-the-art methods for the segmentation of brain tumors in multimodal magnetic resonance imaging (MRI) scans.
* [Leukemia Classification Dataset](https://www.kaggle.com/datasets/andrewmvd/leukemia-classification): In total there are 15,135 images from 118 patients with two labelled classes Normal and Leukemia cells. It is from National Cancer institute.
* [Blood Cell Image](https://github.com/Shenggan/BCCD_Dataset): The diagnosis of blood-based diseases often involves identifying and characterizing patient blood samples. Automated methods to detect and classify blood cell subtypes have important medical applications.
* [Hubmap](https://hubmapconsortium.org/): The Human BioMolecular Atlas Program (HuBMAP) is working to create a Human Reference Atlas at the cellular level. In this competition, you’ll identify and segment functional tissue units (FTUs) across five human organs.

### API
**Check this website https://base64.guru/converter/encode/image to know what kind of input goes into api( you can convert you image to base 64 and use postman to check if api working fine by passing input image through there as base 64 )**
Header 
```
let headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "x-api-key": "<key>",
 "Content-Type": "application/json"
}
```
#### Brain 
**Input type**: dcm
Payload
```
{
    "Image": "<image in base 64>"
}
```
Return
```
{
    "Result": "Image is of tumour/ not tumour"
}
```
#### Chest
**Input type**: png
Payload
```
{
    "Image": "<image in base 64>"
}
```
Return
```
{
    "Result": "Image is of x disease"
}
```

#### Leukaemia
**Input type**: bmp
Payload
```
{
    "Image": "<image in base 64>"
}
```
Return
```
{
    "Result": "Image is of leukaemia/or not"
}
```

#### Tissue
**Input type**: Tiff
**Output type**: jpg
Payload
```
{
    "Image": "<image in base 64>",
    "Organ": "spleen"    // there is 4 option 'kidney', 'largeintestine', 'lung', 'prostate', 'spleen'
}
```
Return
```
{
    "Result": "<Image result in base64>"
}
```

