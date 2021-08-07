# DarkCityScape_mIOU_mPA
This is a repository for calculating the mIOU (mean intersection over union) and mPA (mean average precision) for DarkCityScapes. DarkCityScapes is the "Dark version" of the CityScape dataset and is specifically designed for extreme low-light image enhancement tasks. 
The dataset is simulated using gamma correction on 150 CityScape validation images. 

# Sample Images from DarkCityScapes
![alt text](image.jpg)

# Get Started
Firstly, download the DarkCityScape dataset from [Baiduyun](https://pan.baidu.com/s/1--xG3uNuH_9rKzcHpQKqgQ) with passord wvhy

Secondly, put the predicted outcome (i.e., model output maps) in

`path_to_your_pred`

And the Groudtruth in 

`path_to_your_gt`

Note: you could refers to Dark.txt if you are not sure how to put the images.


Finally, run the following script 


`python main.py --pred path_to_your_pred --gt path_to_your_gt`


# Sample Result
Following is the result table from some state-of-the-art low-light image enhancement models
