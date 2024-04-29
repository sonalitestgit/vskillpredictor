from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)

# Define the dataset
data = {
    'Student ID': [2, 3, 4, 5, 6, 7, 8, 9],
    'C': ['Beginner', 'Beginner', 'Moderate', 'Advanced', 'Beginner', 'Beginner', 'Moderate', 'Beginner'],
    'Cpp': ['Beginner', 'Beginner', 'Moderate', 'Advanced', 'Moderate', 'Beginner', 'Moderate', 'Moderate'],
    'Java': ['Moderate', 'Advanced', 'Moderate', 'Advanced', 'Moderate', 'Beginner', 'None', 'Moderate'],
    'Python': ['Beginner', 'Moderate', 'Moderate', 'Moderate', 'Advanced', 'Beginner', 'None', 'Advanced'],
    'Javascript': ['Beginner', 'Advanced', 'None', 'Moderate', 'Moderate', 'Beginner', 'Beginner', 'None'],
    'Competitive programming (DSA)': ['Moderate', 'Moderate', 'None', 'Advanced', 'Moderate', 'Beginner', 'Moderate', 'Beginner'],
    'Frontend Web Development': ['Beginner', 'Advanced', 'None', 'Advanced', 'Advanced', 'Beginner', 'None', 'Beginner'],
    'Backend Web Development': ['Beginner', 'Moderate', 'None', 'Moderate', 'Moderate', 'Beginner', 'None', 'Beginner'],
    'Full Stack Web Development': ['Beginner', 'Moderate', 'Advanced', 'Beginner', 'Beginner', 'None', 'None', 'Advanced'],
    'Data Analysis and Visualization': ['Beginner', 'Advanced', 'Beginner', 'Beginner', 'Beginner', 'None', 'None', 'Moderate'],
    'Machine Learning and Artificial Intelligence': ['Beginner', 'Moderate', 'None', 'Beginner', 'Beginner', 'None', 'None', 'Beginner'],
    'Cloud Computing': ['None', 'Beginner', 'None', 'Moderate', 'None', 'None', 'None', 'None'],
    'DevOps': ['None', 'Beginner', 'None', 'Moderate', 'None', 'None', 'None', 'None'],
    'Android Development': ['None', 'Beginner', 'None', 'Beginner', 'None', 'None', 'None', 'None'],
    'iOS Development': ['None', 'Beginner', 'None', 'Moderate', 'None', 'None', 'None', 'None'],
    'Cross Platforms (React native, Flutter)': ['Moderate', 'Moderate', 'Advanced', 'Moderate', 'Moderate', 'Beginner', 'None', 'Advanced'],
    'Communication Skill': ['Moderate', 'Moderate', 'Advanced', 'Moderate', 'Moderate', 'Beginner', 'Moderate', 'Advanced']
}

# Convert data into DataFrame
df = pd.DataFrame(data)

# Encode categorical variables
encoder = OrdinalEncoder()
encoded_df = pd.DataFrame(encoder.fit_transform(df.iloc[:, 1:]), columns=df.columns[1:])
print("Encoded Data:")
print(encoded_df.head())

# Train the KNN model
k = 3  # number of neighbors
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(encoded_df, df['Student ID'])

# Map input names to skill names
skill_names = {
            'skill1': 'Embedded Systems Engineer',
            'skill2': 'Systems Software Engineer',
            'skill3': 'Enterprise Application Developer',
            'skill4': 'Data Science Engineer',
            'skill5': 'Frontend Web Architect',
            'skill6': 'Algorithm Specialist',
            'skill7': 'UI/UX Developer',
            'skill8': 'Database Architect',
            'skill9': 'FullStack Developer',
            'skill10': 'Data Analysis Engineer',
            'skill11': 'AI Enginner',
            'skill12': 'Cloud  Engineer',
            'skill13': 'DevOps Enginner',
            'skill14': 'Android Developer',
            'skill15': 'iOS Developer',
            'skill16': 'Cross-Platform App Engineer',
            'skill17': 'Sales Engineer'
}

# Define route for index page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/base')
def base():
    return render_template('base.html')
# Define route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    input_data = [request.form[f'skill{i+1}'] for i in range(17)]
    
    beginner_count = 0
    moderate_count = 0
    advanced_count = 0
    
    # Iterate over each skill level in the input data
    for skill_level in input_data:
        if skill_level == 'Beginner':
            beginner_count += 1
        elif skill_level == 'Moderate':
            moderate_count += 1
        elif skill_level == 'Advanced':
            advanced_count += 1
    
    # Extract moderate and advanced skills for job recommendations
    moderateSkills = []
    advancedSkills = []
    beginnerSkills = []
    for i, skill_level in enumerate(input_data):
        if skill_level == 'Advanced':
            advancedSkills.append(skill_names[f'skill{i+1}'])
        elif skill_level == 'Moderate':
            moderateSkills.append(skill_names[f'skill{i+1}'])
        elif skill_level == 'Beginner':
            beginnerSkills.append(skill_names[f'skill{i+1}'])


    
    # Prepare job recommendations
    if advancedSkills:
        job_recommendations = f'Suitable Job Roles That Align with Your Skillset Are: {", ".join(advancedSkills)}'
    elif moderateSkills:
        job_recommendations = f'Suitable Job Roles That Align with Your Skillset Are: {", ".join(moderateSkills)}'
    else:
        job_recommendations = 'You need to work on your skillset to qualify for job roles.'
    
    # Render result template with prediction data
    return render_template('result.html', beginner_count=beginner_count, moderate_count=moderate_count,
                           advanced_count=advanced_count, job_recommendations=job_recommendations)

@app.route('/explore')
def explore():
    return render_template('explore.html')

if __name__ == '__main__':
    app.run(debug=True)









