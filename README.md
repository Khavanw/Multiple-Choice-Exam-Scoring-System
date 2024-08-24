# [OpenCV] Multiple Choice Exam Scoring System

Automated Scoring System for Multiple Choice Tests Using OpenCV.

## Overview

In this project, we apply the OpenCV image processing library to address the problem of automated scoring for 120-question multiple-choice answer sheets in the National High School Examination without using machine learning or deep learning. Instead, we focus on utilizing traditional image processing methods and image analysis techniques to achieve the project's goals.

## Main Features
1. Read Scanned Image
2. Image Preprocessing:
    - Resize
    - Convert to Grayscale
    - Thresholding
3. Find Contours of Answer Blocks, Candidate Numbers, Exam Codes, etc.
4. Process and Filter Marked Boxes Recognition
5. Match and Compare Results
6. Visualization
7. Save Results

## Build Model
### Dataset
The input images in the automated scoring process are scanned images of actual high school multiple-choice answer sheets. These images typically contain information about the questions and the answer bubbles filled in by the students. The images may be either color or grayscale, depending on the scanner settings.

![phieuthi](phieuthi.png)
### Image Preprocessing
1. Resize: Although the input images are scanned and have a fixed size, in this model, we will resize the images to 640x480 for convenience in subsequent processing steps
2. Convert to Grayscale
3. Thresholding
### Identify Areas to Process
After finding the contours in the image, the next step is to identify the answer blocks, candidate number, and exam code blocks. Thus, we need to identify 6 boxes present in the image

![Areas](results/img_box_contour.jpg)
### Process Answer Blocks
In this exam template, we have 120 questions divided into 4 columns. Each column contains 6 boxes, each box contains 5 questions. For each question, there are 4 answer choices: 'A', 'B', 'C', 'D'. After understanding the general input structure, I divide the solution into the following steps:

- Process the input image to separate the 4 answer columns
- Divide each answer column into 6 boxes, and each box further into 5 questions
- Identify the chosen answer for each question: 
    - Use pixel-level processing techniques on the objects to determine the marked answer box for each question

![Answer](results/img_threshold.jpg)
### Match and Visualize
After obtaining the list of answers chosen by the candidates, we proceed to match the answers to determine the score. We also perform visualization on the screen, where correctly marked answer boxes are highlighted in green and incorrectly marked ones in red, including any invalid boxes as follows

![Result]()
### Process Candidate Number and Exam Code Blocks
### Save Results
