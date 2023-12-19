~~# My Contributions to PitchTek
## By Ethan Carroll

### NOTE: My IDE started pushing from my casual GitHub account and not my professional one. I could not figure out how to change it back. Therefor, some of my commits come from <ins>ethancarrollUNR</ins> and half come from <ins>chunkyshrapnel

### <ins>Work Completed Prior to 12/9/23
1. I made a breakdown of data variables by usefulness. The Excel doc can be seen in the screenshot below or at the following link: https://docs.google.com/spreadsheets/d/1YPk4Ht_ik9Fv__ZcWwB1SbodhqzvTOse7eczARbWEdk/edit#gid=0

    ![Feature Breakdown](images_for_ethans_read_me/feature_breakdown.png)   


2. I cleaned the data and outlined further steps to make the data perfect for our project. This can be seen in the <ins>backend\modify_data.py</ins> file.

3. I experimented with several different ML models to try and get a prototype for our algorithm. This includes an MLP model and a Decision Tree model. This work can be seen in the <ins>backend\model.py</ins> file.

### <ins>Work Completed for 12/9/23

1. Created and experimented with Mark Down README.

### <ins>Work Completed for 12/10/23

1. Implemented One-Hot Encoding technique to change categorical variables to numerical. 

    ![hot_encode](images_for_ethans_read_me/hotencoder.png)   


2. Attempted to get a DT classifier working. Unfortunately I am still running into errors.

### <ins>Work Completed for 12/16/23

1. Got a DT classifier to work and return an accuracy of 42%

2. Split the data into two different categories: first_pitch.csv and subsequent_pitches.csv. One file contains all the 
   data for the first pitch in each plate appearance, while the other only has the data for the following plate appearances.

3. Wrote a DT classifier for each set where each DT uses different labels. The first pitch DT has an accuracy of 42% while
   the other DT classifier has an accuracy of 39%. I know that this seems like a downgrade from part 1 but I still believe 
   that this DT makes more sense.
   
### <ins>Work Completed for 12/17/23

1. Imported the "mitt" library so that different Vue components can communicate with each other. 

   This is demonstrated in the following images. When a user clicks "PREDICT" in the first image, the "Pitch type" 
   variable in the second image is changed to "TEST PITCH. This sets the framework for updating the predictions when new
   data in input. 

   ![select_predict_button](images_for_ethans_read_me/select_predict_button.png)    
   ![pitch_type_changed](images_for_ethans_read_me/pitch_type_changed.png)

### <ins>Work Completed for 12/18/23

1. Figured out how to get the front end to communicate with the "Flask" backend.
2. Created a new DT that to better reflect the front end. Has an accuracy of 46% 
3. Exported the DT model so that it can be used by get_prediciton.py
4. The website can now be used to predict Pitch Type!
   ![PitchTek_predicts_slider](images_for_ethans_read_me/Slider_predicted.png)    
5. Added backend functionality so that a prediction for speed is made when the user clicks "Predict". NOTE: This is not
an ML prediction. But a dummy place-holder predictions

### <ins>Work Completed for 12/19/23
   
1. Added create_heatmap.py. This file is used to aggregate Justin Verlander's pitches and create a
heat map for every type of pitch he throws.

HERE ARE THE CREATED HEATMAPS

   ![FF_heat](images_for_ethans_read_me/FF_heat_map.jpg)    
   ![SL_heat](images_for_ethans_read_me/SL_heat_map.jpg)
   ![CU_heat](images_for_ethans_read_me/CU_heat_map.jpg)    
   ![CH_heat](images_for_ethans_read_me/CH_heat_map.jpg)