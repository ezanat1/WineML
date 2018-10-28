# Project-Team-9
Student Names: Steven Duong,​ ​Ezana Tesfaye, Lishan Zhu, Shengqi Suizhu
Team Name: Pioneers
 
Project title: Music Classifier
 
Project description: People want to explore new music in similar or closely related genres. Therefore, it’s helpful to categorize music in order to quantify and recommend new music to users that are looking for new content. The model will take training data with different music samples and their respective classifications. After training the model, it should be able to predict the type of any given music samples. When the user inputs a song he/she likes into the model, it should be able to recommend new songs based on similarity in genre or artist.
 
Proposed methodology/ resources, etc:  Training an AutoEncoder on the training set to shrink the sample data. Then we can train a CNN classifier to the encoded data. After the user inputs a song, we can return the user with songs of the same genre.
 
Data set: The project can either be done collecting categorized MIDI files, or process music videos from youtube as training data.
 
Project title: Wine Recommender  - APPROVED
 
Project description: Sometimes when people find a type of wine they enjoy, they are likely to try similar types of wine.
With this project, the user will be able to input a group of wines he/she like, and set filters for attributes such as price, region, or varietal. The model then recommends new wines to the user that it thinks he/she would like. Similarity will be calculated based on attributes such as varietal, region, previous user’s reviews, and keywords from the wine’s description.
 
Proposed methodology/ resources, etc: We’ll be using sentiment analysis to determine the similarity between each wine’s description and factor that into the overall similarity of each wine. Then a classifier is used to match the description of the user input and then return the types of wine that matches the input.
 
Data set: https://www.kaggle.com/zynicide/wine-reviewss 
 
Project title: Kickstarter Success Predictor
 
Project description: Not all projects are fully funded on kickstarter, so when backing a project, there are risks that the project will never be funded or completed. We also don’t want to wait until the very end to back a project because there are limited early bird incentives offered. To obtain the best value when backing a campaign while decreasing the chance of losing money, we want to create a model that can accurately predict the likelihood of a campaign’s success. Additionally, when a project is started on kickstarter, the organizer is also eager to know whether the project is going to be a success or not. The model takes previous kickstarter campaign data and predicts whether a given current kickstarter project will successfully be funded. 
 
Proposed methodology/ resources, etc: We can apply sentiment analysis on the description of the project, then we can train a SVM on the training dataset based on attributes such as positive words, project type, etc . Given the user project input, we can determine the probability of it being successful or not.
 
Data set: https://www.kaggle.com/kemical/kickstarter-projects
 
 


