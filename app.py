from flask import Flask, render_template

app = Flask(__name__)

ai_topics = [
    {
        "title": "Machine Learning Fundamentals",
        "description": "Understand supervised vs unsupervised learning, model selection, and evaluation metrics.",
        "points": [
            "Bias vs variance",
            "Common algorithms: linear regression, decision trees, k-means",
            "Evaluation metrics: accuracy, precision, recall, F1"
        ]
    },
    {
        "title": "Deep Learning",
        "description": "Learn neural network building blocks, activation functions, optimization, and common architectures.",
        "points": [
            "Feedforward and convolutional networks",
            "Backpropagation and gradient descent",
            
            "Regularization: dropout, batch normalization"
        ]
    },
    {
        "title": "Data Preparation",
        "description": "Master how to clean data, engineer features, and choose the right training pipeline.",
        "points": [
            "Data cleaning and scaling",
            "Feature engineering and selection",
            "Handling missing values and outliers"
        ]
    },
    {
        "title": "Model Explainability",
        "description": "Prepare to explain model behavior, trade-offs, and how you validate performance.",
        "points": [
            "Confusion matrix and ROC curves",
            "Model interpretation techniques",
            "Trade-offs between accuracy and complexity"
        ]
    },
    {
        "title": "AI System Design",
        "description": "Plan interviews on how to build reliable AI systems and productionize machine learning models.",
        "points": [
            "Data pipelines and feature stores",
            "Model deployment options",
            "Monitoring, retraining, and scaling"
        ]
    }
]

practice_questions = [
    {
        "topic": "Machine Learning Fundamentals",
        "text": "How do you decide whether to use a classification or regression model for a problem?",
        "tip": "Explain the target variable type and how the prediction output determines the model family."
    },
    {
        "topic": "Machine Learning Fundamentals",
        "text": "What is overfitting and how can you prevent it?",
        "tip": "Mention cross-validation, regularization, simpler models, and more training data."
    },
    {
        "topic": "Deep Learning",
        "text": "Describe the vanishing gradient problem and a solution to it.",
        "tip": "Talk about activation functions, gradient flow, and modern architectures like ResNet."
    },
    {
        "topic": "Deep Learning",
        "text": "When would you use a convolutional neural network instead of a dense network?",
        "tip": "Focus on spatial patterns and images, and how convolution preserves local structure."
    },
    {
        "topic": "Data Preparation",
        "text": "Why is feature scaling important, and which algorithms need it?",
        "tip": "Discuss distance-based models like k-NN and gradient-based optimization methods."
    },
    {
        "topic": "Model Explainability",
        "text": "How do you explain a model’s decision to a non-technical stakeholder?",
        "tip": "Use simple analogies, focus on key features, and avoid technical jargon."
    },
    {
        "topic": "AI System Design",
        "text": "What steps are needed to deploy a machine learning model in production?",
        "tip": "Cover data pipelines, model packaging, monitoring, and retraining strategy."
    }
]

quiz_questions = [
    {
        "topic": "Machine Learning Fundamentals",
        "question": "Which technique helps prevent overfitting by adding a penalty to model complexity?",
        "options": ["Data augmentation", "Regularization", "Feature scaling", "Normalization"],
        "answer": "Regularization",
        "explanation": "Regularization discourages overly complex models by penalizing large weights."
    },
    {
        "topic": "Machine Learning Fundamentals",
        "question": "What type of model would you use for predicting a continuous value?",
        "options": ["Classification", "Regression", "Clustering", "Dimensionality reduction"],
        "answer": "Regression",
        "explanation": "Regression models predict continuous numeric outcomes."
    },
    {
        "topic": "Deep Learning",
        "question": "Which activation function is commonly used to avoid vanishing gradients?",
        "options": ["Sigmoid", "Tanh", "ReLU", "Linear"],
        "answer": "ReLU",
        "explanation": "ReLU maintains stronger gradients for positive values, helping deeper networks train."
    },
    {
        "topic": "Data Preparation",
        "question": "Why is feature scaling important for many machine learning models?",
        "options": ["It reduces model size", "It ensures features have equal influence", "It increases training data", "It adds noise"],
        "answer": "It ensures features have equal influence",
        "explanation": "Scaling helps distance-based and gradient-based models treat features consistently."
    },
    {
        "topic": "AI System Design",
        "question": "What is one key reason to monitor a deployed AI model in production?",
        "options": ["To collect more training data", "To ensure model performance remains stable", "To reduce data storage", "To hide model internals"],
        "answer": "To ensure model performance remains stable",
        "explanation": "Monitoring detects drift, errors, and performance degradation after deployment."
    },
    {
        "topic": "Model Explainability",
        "question": "Which metric is useful for evaluating a classifier when classes are imbalanced?",
        "options": ["Accuracy", "Precision", "Mean squared error", "R-squared"],
        "answer": "Precision",
        "explanation": "Precision focuses on true positives and helps evaluate models with imbalanced classes."
    }
]

resources = [
    {
        "title": "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow",
        "description": "A practical guide to machine learning and deep learning concepts with code examples.",
        "link": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/"
    },
    {
        "title": "Coursera: Machine Learning by Andrew Ng",
        "description": "A popular introductory ML course covering core algorithms and practical techniques.",
        "link": "https://www.coursera.org/learn/machine-learning"
    },
    {
        "title": "AI Interview Guide",
        "description": "Review common AI and machine learning interview questions and answer strategies.",
        "link": "https://www.interviewbit.com/machine-learning-interview-questions/"
    }
]

@app.route('/')
def index():
    return render_template('index.html', topics=ai_topics)

@app.route('/topics')
def topics_page():
    return render_template('topics.html', topics=ai_topics)

@app.route('/practice')
def practice_page():
    return render_template('practice.html', questions=practice_questions, topics=ai_topics)

@app.route('/quiz')
def quiz_page():
    return render_template('quiz.html', topics=ai_topics, quiz_questions=quiz_questions)

@app.route('/resources')
def resources_page():
    return render_template('resources.html', resources=resources)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
