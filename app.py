from flask import Flask, render_template, jsonify, request
import json
import random
import os

app = Flask(__name__)

ai_topics = [
    {
        "key": "machine-learning-fundamentals",
        "title": "Machine Learning Fundamentals",
        "description": "Understand supervised vs unsupervised learning, model selection, and evaluation metrics.",
        "points": [
            "Bias vs variance",
            "Common algorithms: linear regression, decision trees, k-means",
            "Evaluation metrics: accuracy, precision, recall, F1"
        ],
        "topics": [
            {
                "title": "Supervised Learning",
                "summary": "The model learns from labeled examples.",
                "qas": [
                    {
                        "q": "What is supervised learning?",
                        "a": "Supervised learning is a type of machine learning where the model learns from labeled data. The input and correct output are provided during training."
                    },
                    {
                        "q": "What are examples of supervised learning?",
                        "a": "Email spam detection, house price prediction, disease prediction, and sentiment analysis."
                    },
                    {
                        "q": "Difference between classification and regression?",
                        "a": "Classification predicts categories while regression predicts continuous numerical values."
                    }
                ]
            },
            {
                "title": "Overfitting",
                "summary": "When a model fits the training data too closely.",
                "qas": [
                    {
                        "q": "What is overfitting?",
                        "a": "Overfitting occurs when a model learns training data too well including noise, causing poor performance on unseen data."
                    },
                    {
                        "q": "How can you reduce overfitting?",
                        "a": "Using regularization, dropout, more training data, and cross-validation."
                    },
                    {
                        "q": "What is the difference between overfitting and underfitting?",
                        "a": "Overfitting performs well on training data but poorly on test data, while underfitting fails on both."
                    }
                ]
            },
            {
                "title": "Cross Validation",
                "summary": "Evaluate model generalization using data splits.",
                "qas": [
                    {
                        "q": "What is cross-validation?",
                        "a": "Cross-validation is a technique used to evaluate model performance by dividing data into multiple folds."
                    },
                    {
                        "q": "Why is cross-validation important?",
                        "a": "It helps estimate how well the model generalizes to unseen data."
                    },
                    {
                        "q": "What is k-fold cross-validation?",
                        "a": "The dataset is divided into k parts, and the model trains and tests k times."
                    }
                ]
            },
            {
                "title": "Random Forest",
                "summary": "An ensemble of decision trees for more stable predictions.",
                "qas": [
                    {
                        "q": "What is Random Forest?",
                        "a": "Random Forest is an ensemble learning algorithm that combines multiple decision trees."
                    },
                    {
                        "q": "What are advantages of Random Forest?",
                        "a": "High accuracy, reduced overfitting, and good handling of large datasets."
                    },
                    {
                        "q": "Why is Random Forest better than a single decision tree?",
                        "a": "Because it reduces variance and improves generalization."
                    }
                ]
            },
            {
                "title": "Evaluation Metrics",
                "summary": "Metrics to assess classification and model quality.",
                "qas": [
                    {
                        "q": "What is accuracy?",
                        "a": "Accuracy is the ratio of correct predictions to total predictions."
                    },
                    {
                        "q": "What is precision?",
                        "a": "Precision measures how many predicted positives are actually positive."
                    },
                    {
                        "q": "What is recall?",
                        "a": "Recall measures how many actual positives are correctly identified."
                    },
                    {
                        "q": "What is F1-score?",
                        "a": "F1-score is the harmonic mean of precision and recall."
                    }
                ]
            }
        ]
    },
    {
        "key": "deep-learning",
        "title": "Deep Learning",
        "description": "Learn neural network building blocks, activation functions, optimization, and common architectures.",
        "points": [
            "Feedforward and convolutional networks",
            "Backpropagation and gradient descent",
            "Regularization: dropout, batch normalization"
        ],
        "topics": [
            {
                "title": "Neural Networks",
                "summary": "A brain-inspired model of neurons and layered connections.",
                "qas": [
                    {
                        "q": "What is a neural network?",
                        "a": "A neural network is a computational model inspired by the human brain consisting of interconnected neurons."
                    },
                    {
                        "q": "What are layers in neural networks?",
                        "a": "Input layer, hidden layers, and output layer."
                    },
                    {
                        "q": "Why are hidden layers important?",
                        "a": "They help the network learn complex patterns from data."
                    }
                ]
            },
            {
                "title": "CNN",
                "summary": "Convolutional models for image-related tasks.",
                "qas": [
                    {
                        "q": "What is CNN?",
                        "a": "Convolutional Neural Network is a deep learning model mainly used for image processing tasks."
                    },
                    {
                        "q": "Where are CNNs used?",
                        "a": "Image classification, object detection, facial recognition, and medical imaging."
                    },
                    {
                        "q": "What is convolution?",
                        "a": "Convolution extracts important features from images using filters."
                    }
                ]
            },
            {
                "title": "RNN and LSTM",
                "summary": "Sequence models that preserve context over time.",
                "qas": [
                    {
                        "q": "What is RNN?",
                        "a": "Recurrent Neural Networks process sequential data like text and speech."
                    },
                    {
                        "q": "What is LSTM?",
                        "a": "LSTM is a special type of RNN that solves long-term dependency problems."
                    },
                    {
                        "q": "Where are LSTMs used?",
                        "a": "Chatbots, speech recognition, and language translation."
                    }
                ]
            },
            {
                "title": "Transformers",
                "summary": "Modern sequence models built with attention mechanisms.",
                "qas": [
                    {
                        "q": "What are transformers?",
                        "a": "Transformers are deep learning architectures used mainly in NLP tasks."
                    },
                    {
                        "q": "What is attention mechanism?",
                        "a": "Attention helps models focus on important words in a sentence."
                    },
                    {
                        "q": "What is GPT?",
                        "a": "GPT is a transformer-based language model developed for text generation."
                    }
                ]
            },
            {
                "title": "Backpropagation",
                "summary": "Gradient-based learning for neural weights.",
                "qas": [
                    {
                        "q": "What is backpropagation?",
                        "a": "It is the process of updating neural network weights using error gradients."
                    },
                    {
                        "q": "Why is backpropagation important?",
                        "a": "It helps the model learn by minimizing prediction error."
                    },
                    {
                        "q": "What optimizer is commonly used?",
                        "a": "Adam optimizer is widely used because of faster convergence."
                    }
                ]
            }
        ]
    },
    {
        "key": "data-preparation",
        "title": "Data Preparation",
        "description": "Master how to clean data, engineer features, and choose the right training pipeline.",
        "points": [
            "Data cleaning and scaling",
            "Feature engineering and selection",
            "Handling missing values and outliers"
        ],
        "topics": [
            {
                "title": "Data Cleaning",
                "summary": "Remove bad records and clean the dataset.",
                "qas": [
                    {
                        "q": "What is data cleaning?",
                        "a": "Data cleaning removes errors, duplicates, and inconsistencies from datasets."
                    },
                    {
                        "q": "Why is data cleaning important?",
                        "a": "Poor quality data leads to poor model performance."
                    },
                    {
                        "q": "What are duplicate records?",
                        "a": "Repeated entries in a dataset that can affect analysis accuracy."
                    }
                ]
            },
            {
                "title": "Missing Values",
                "summary": "Handle gaps in your dataset safely.",
                "qas": [
                    {
                        "q": "How do you handle missing values?",
                        "a": "By removing rows, replacing with mean/median, or using prediction methods."
                    },
                    {
                        "q": "What is imputation?",
                        "a": "Imputation is filling missing values using statistical methods."
                    },
                    {
                        "q": "Which is better mean or median imputation?",
                        "a": "Median is better when data contains outliers."
                    }
                ]
            },
            {
                "title": "Feature Scaling",
                "summary": "Scale features so all values behave consistently.",
                "qas": [
                    {
                        "q": "Why is feature scaling necessary?",
                        "a": "It ensures all features contribute equally to model training."
                    },
                    {
                        "q": "What is normalization?",
                        "a": "Normalization scales values between 0 and 1."
                    },
                    {
                        "q": "What is standardization?",
                        "a": "Standardization transforms data with mean 0 and standard deviation 1."
                    }
                ]
            },
            {
                "title": "Encoding Techniques",
                "summary": "Convert categories into numeric form.",
                "qas": [
                    {
                        "q": "What is one-hot encoding?",
                        "a": "It converts categorical variables into binary vectors."
                    },
                    {
                        "q": "What is label encoding?",
                        "a": "It converts categories into numerical labels."
                    },
                    {
                        "q": "Which models require encoding?",
                        "a": "Most machine learning algorithms require numerical input."
                    }
                ]
            },
            {
                "title": "Exploratory Data Analysis",
                "summary": "Inspect the data before modeling.",
                "qas": [
                    {
                        "q": "What is Exploratory Data Analysis?",
                        "a": "EDA is analyzing datasets visually and statistically before modeling."
                    },
                    {
                        "q": "What tools are used in EDA?",
                        "a": "Pandas, Matplotlib, Seaborn, and Plotly."
                    },
                    {
                        "q": "Why is EDA important?",
                        "a": "It helps discover patterns, trends, and anomalies in data."
                    }
                ]
            }
        ]
    },
    {
        "key": "model-explainability",
        "title": "Model Explainability",
        "description": "Prepare to explain model behavior, trade-offs, and how you validate performance.",
        "points": [
            "Confusion matrix and ROC curves",
            "Model interpretation techniques",
            "Trade-offs between accuracy and complexity"
        ],
        "topics": [
            {
                "title": "Feature Importance",
                "summary": "Explain which features matter most.",
                "qas": [
                    {
                        "q": "What is feature importance?",
                        "a": "Feature importance measures how much each input contributes to model decisions."
                    },
                    {
                        "q": "Why is feature importance useful?",
                        "a": "It helps explain model behavior and identify the most influential features."
                    },
                    {
                        "q": "How can you compute feature importance?",
                        "a": "Use model coefficients, permutation importance, or tree-based importance scores."
                    }
                ]
            },
            {
                "title": "SHAP and LIME",
                "summary": "Post-hoc tools for black-box models.",
                "qas": [
                    {
                        "q": "What is SHAP?",
                        "a": "SHAP assigns each feature an importance value for a particular prediction."
                    },
                    {
                        "q": "What is LIME?",
                        "a": "LIME explains individual predictions by approximating the model locally with an interpretable model."
                    },
                    {
                        "q": "When should you use SHAP or LIME?",
                        "a": "Use them when you need to explain non-linear or black-box models to stakeholders."
                    }
                ]
            },
            {
                "title": "Metrics and Trade-offs",
                "summary": "Explain model performance and limitations.",
                "qas": [
                    {
                        "q": "How do you explain model performance?",
                        "a": "Compare metrics like precision, recall, and AUC while discussing business impact."
                    },
                    {
                        "q": "What trade-offs matter in explainability?",
                        "a": "Explainability often trades off with model complexity and accuracy."
                    },
                    {
                        "q": "Why is confidence important in explanations?",
                        "a": "It helps stakeholders trust predictions by clarifying uncertainty and limitations."
                    }
                ]
            }
        ]
    },
    {
        "key": "ai-system-design",
        "title": "AI System Design",
        "description": "Plan interviews on how to build reliable AI systems and productionize machine learning models.",
        "points": [
            "Data pipelines and feature stores",
            "Model deployment options",
            "Monitoring, retraining, and scaling"
        ],
        "topics": [
            {
                "title": "Deployment",
                "summary": "Move models from prototype to production.",
                "qas": [
                    {
                        "q": "What are the key steps in model deployment?",
                        "a": "Build, deploy, monitor, and retrain the model in production."
                    },
                    {
                        "q": "Why is monitoring important after deployment?",
                        "a": "Monitoring ensures model performance remains stable and alerts you to issues."
                    },
                    {
                        "q": "What is a model registry?",
                        "a": "A model registry tracks versions, metadata, and deployment status for models."
                    }
                ]
            },
            {
                "title": "Monitoring and Drift",
                "summary": "Detect and respond to data and model changes.",
                "qas": [
                    {
                        "q": "How do you detect data drift?",
                        "a": "Monitor input distributions and performance metrics over time."
                    },
                    {
                        "q": "What is concept drift?",
                        "a": "Concept drift occurs when the underlying data patterns change, degrading model accuracy."
                    },
                    {
                        "q": "Why is retraining needed?",
                        "a": "Retraining updates the model when new data or drift changes the problem."
                    }
                ]
            },
            {
                "title": "Data Pipelines",
                "summary": "Automate data preparation and inference consistently.",
                "qas": [
                    {
                        "q": "What is a feature store?",
                        "a": "A feature store is a centralized repository for reusable, versioned feature data."
                    },
                    {
                        "q": "Why are pipelines important?",
                        "a": "Pipelines automate data preparation, training, and deployment consistently."
                    },
                    {
                        "q": "What is the difference between training and serving pipelines?",
                        "a": "Training pipelines prepare datasets and models, while serving pipelines deliver predictions in production."
                    }
                ]
            }
        ]
    }
]

practice_questions = [
    {
        "topic": "Machine Learning Fundamentals",
        "text": "How do you decide whether to use a classification or regression model for a problem?",
        "options": ["Use regression for categorical output", "Use classification for continuous output", "Use regression for continuous output", "Use clustering for all tasks"],
        "answer": "Use regression for continuous output",
        "tip": "Explain the target variable type and how the prediction output determines the model family."
    },
    {
        "topic": "Machine Learning Fundamentals",
        "text": "What is overfitting and how can you prevent it?",
        "options": ["Train longer", "Use simpler models and regularization", "Ignore validation", "Use more features"],
        "answer": "Use simpler models and regularization",
        "tip": "Mention cross-validation, regularization, simpler models, and more training data."
    },
    {
        "topic": "Deep Learning",
        "text": "Describe the vanishing gradient problem and a solution to it.",
        "options": ["It is caused by large weights", "Use ReLU or skip connections", "Increase the learning rate", "Use fewer layers"],
        "answer": "Use ReLU or skip connections",
        "tip": "Talk about activation functions, gradient flow, and modern architectures like ResNet."
    },
    {
        "topic": "Deep Learning",
        "text": "When would you use a convolutional neural network instead of a dense network?",
        "options": ["For text classification", "For spatial data like images", "For tabular data only", "For clustering tasks"],
        "answer": "For spatial data like images",
        "tip": "Focus on spatial patterns and images, and how convolution preserves local structure."
    },
    {
        "topic": "Data Preparation",
        "text": "Why is feature scaling important, and which algorithms need it?",
        "options": ["Only tree models need scaling", "It helps distance-based algorithms", "It reduces dataset size", "It is never needed"],
        "answer": "It helps distance-based algorithms",
        "tip": "Discuss distance-based models like k-NN and gradient-based optimization methods."
    },
    {
        "topic": "Model Explainability",
        "text": "How do you explain a model’s decision to a non-technical stakeholder?",
        "options": ["Use technical formulas", "Use simple analogies and key feature examples", "Never explain the model", "Only show the training data"],
        "answer": "Use simple analogies and key feature examples",
        "tip": "Use simple analogies, focus on key features, and avoid technical jargon."
    },
    {
        "topic": "AI System Design",
        "text": "What steps are needed to deploy a machine learning model in production?",
        "options": ["Only build the model", "Train locally and forget it", "Build, deploy, monitor, and retrain", "Use the training data as the final app"],
        "answer": "Build, deploy, monitor, and retrain",
        "tip": "Cover data pipelines, model packaging, monitoring, and retraining strategy."
    },
    {
        "topic": "Machine Learning Fundamentals",
        "text": "What is the difference between supervised and unsupervised learning?",
        "options": ["Supervised uses labels, unsupervised does not", "Unsupervised uses labels, supervised does not", "Both use labels", "Neither uses labels"],
        "answer": "Supervised uses labels, unsupervised does not",
        "tip": "Mention that supervised learning uses labeled training data while unsupervised finds patterns without labels."
    },
    {
        "topic": "Machine Learning Fundamentals",
        "text": "What does cross-validation help you evaluate?",
        "options": ["Training speed", "Model generalization performance", "Number of features", "Dataset size"],
        "answer": "Model generalization performance",
        "tip": "Cross-validation helps estimate how well a model performs on unseen data."
    },
    {
        "topic": "Data Preparation",
        "text": "Why is it important to handle missing values before training a model?",
        "options": ["Missing values always improve accuracy", "Models can fail or learn wrong patterns", "It makes the dataset larger", "It is never important"],
        "answer": "Models can fail or learn wrong patterns",
        "tip": "Handling missing values avoids unexpected model behavior and biased results."
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
    domain_key = request.args.get('domain', 'All')
    domain = get_domain(domain_key) if domain_key != 'All' else None
    selected_title = domain['title'] if domain else 'All'
    return render_template(
        'quiz.html',
        topics=ai_topics,
        quiz_questions=quiz_questions,
        selected_domain_key=domain_key,
        selected_domain_title=selected_title
    )

@app.route('/domain/<domain_key>')
def domain_page(domain_key):
    domain = get_domain(domain_key)
    if not domain:
        abort(404)
    return render_template('domain_detail.html', domain=domain, topics=ai_topics)

@app.route('/resources')
def resources_page():
    return render_template('resources.html', resources=resources)


def get_domain(domain_key):
    return next((domain for domain in ai_topics if domain.get('key') == domain_key), None)


def load_questions_for(domain_key):
    """Load questions JSON for a given domain key (e.g., 'ml')."""
    base = os.path.join(os.path.dirname(__file__), 'data')
    if domain_key == 'ml':
        path = os.path.join(base, 'ml_questions.json')
    else:
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def shuffle_question_options(q):
    """Return a copy of question with shuffled options and adjusted answer index."""
    opts = list(q.get('options', []))
    if not opts:
        return q
    indices = list(range(len(opts)))
    random.shuffle(indices)
    shuffled = [opts[i] for i in indices]
    # find new answer index
    orig_answer = q.get('answer')
    if isinstance(orig_answer, int) and 0 <= orig_answer < len(opts):
        new_index = indices.index(orig_answer)
    else:
        # if answer stored as value, find it
        try:
            new_index = shuffled.index(orig_answer)
        except Exception:
            new_index = 0
    new_q = q.copy()
    new_q['options'] = shuffled
    new_q['answer'] = new_index
    return new_q


@app.route('/api/questions/<domain_key>')
def api_questions(domain_key):
    """Return shuffled questions for a domain. Query params: count, difficulty"""
    qs = load_questions_for(domain_key)
    if not qs:
        return jsonify({"error": "domain not found"}), 404
    # optional filter by difficulty
    difficulty = request.args.get('difficulty')
    if difficulty:
        qs = [q for q in qs if q.get('difficulty', '').lower() == difficulty.lower()]
    random.shuffle(qs)
    try:
        count = int(request.args.get('count'))
    except Exception:
        count = None
    if count:
        qs = qs[:count]
    # shuffle options for each question
    qs_shuffled = [shuffle_question_options(q) for q in qs]
    return jsonify(qs_shuffled)


@app.route('/api/quiz')
def api_quiz():
    """Create a mixed quiz from multiple domains. For now supports 'ml' only. Query: count"""
    # gather all domains – extendable
    all_qs = load_questions_for('ml')
    random.shuffle(all_qs)
    try:
        count = int(request.args.get('count', 10))
    except Exception:
        count = 10
    selected = all_qs[:count]
    selected = [shuffle_question_options(q) for q in selected]
    return jsonify({"questions": selected, "count": len(selected)})


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', topics=ai_topics)


@app.route('/runner')
def quiz_runner():
    return render_template('quiz_runner.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
