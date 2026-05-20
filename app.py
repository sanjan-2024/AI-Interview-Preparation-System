from flask import Flask, render_template, jsonify, request, abort
import json
import os
import random

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

ML_TOPICS = [
    {
        'key': 'supervised-learning',
        'title': 'Supervised Learning',
        'description': 'Regression, classification, training, and model behavior.'
    },
    {
        'key': 'model-evaluation',
        'title': 'Model Evaluation',
        'description': 'Accuracy, precision, recall, cross-validation, and metrics.'
    },
    {
        'key': 'feature-engineering',
        'title': 'Feature Engineering',
        'description': 'Data preparation, scaling, encoding, and feature selection.'
    },
    {
        'key': 'model-selection',
        'title': 'Model Selection',
        'description': 'Choosing algorithms, tuning hyperparameters, and avoiding overfitting.'
    },
    {
        'key': 'ml-principles',
        'title': 'ML Principles',
        'description': 'Fundamentals, terminology, and interview-style knowledge checks.'
    }
]

DOMAINS = [
    {
        'key': 'ml',
        'title': 'Machine Learning',
        'description': 'Learn core machine learning concepts, algorithms, model evaluation, and interview topics.',
        'topics': ML_TOPICS
    },
    {
        'key': 'dl',
        'title': 'Deep Learning',
        'description': 'Create neural networks, build models, and learn optimization techniques.',
        'topics': [
            {'key': 'cnn-rnn-transformers', 'title': 'CNN / RNN / Transformers', 'description': 'Learn the key architectures used in deep learning.'},
            {'key': 'training-deployment', 'title': 'Training & Deployment', 'description': 'Understand training workflows, loss functions, and serving models.'}
        ]
    },
    {
        'key': 'dp',
        'title': 'Data Preparation',
        'description': 'Discover how to clean, transform, and prepare data for AI systems.',
        'topics': [
            {'key': 'cleaning-engineering', 'title': 'Cleaning & Engineering', 'description': 'Data cleaning, imputation, scaling, and encoding techniques.'},
            {'key': 'pipelines-workflows', 'title': 'Pipelines & Workflows', 'description': 'Build reproducible data pipelines for interview scenarios.'}
        ]
    },
    {
        'key': 'ex',
        'title': 'Explainability',
        'description': 'Explore model interpretability, feature importance, and responsible AI.',
        'topics': [
            {'key': 'model-interpretation', 'title': 'Model Interpretation', 'description': 'Methods for explaining model decisions to stakeholders.'},
            {'key': 'fairness-ethics', 'title': 'Fairness & Ethics', 'description': 'AI ethics, bias detection, and responsible deployment.'}
        ]
    },
    {
        'key': 'sd',
        'title': 'AI System Design',
        'description': 'Design scalable AI systems, architecture, and production readiness.',
        'topics': [
            {'key': 'architecture', 'title': 'Architecture', 'description': 'Design AI systems with databases, APIs, and scalability in mind.'},
            {'key': 'monitoring', 'title': 'Monitoring', 'description': 'Track model performance and maintain systems in production.'}
        ]
    }
]


def load_ml_questions():
    path = os.path.join(DATA_DIR, 'ml_questions.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def slugify(value):
    return ''.join(c.lower() if c.isalnum() else '-' if c.isspace() else '' for c in value).replace('--', '-').strip('-')


def get_domain(domain_key):
    for domain in DOMAINS:
        if domain['key'] == domain_key or slugify(domain['title']) == domain_key:
            return domain
    return None


def get_topic(domain, topic_key):
    if not domain:
        return None
    for topic in domain.get('topics', []):
        if topic['key'] == topic_key or slugify(topic['title']) == topic_key:
            return topic
    return None


def build_topic_for_question(question):
    question_id = question.get('id', 0)
    if 1 <= question_id <= 20:
        return ML_TOPICS[0]['key']
    if 21 <= question_id <= 40:
        return ML_TOPICS[1]['key']
    if 41 <= question_id <= 60:
        return ML_TOPICS[2]['key']
    if 61 <= question_id <= 80:
        return ML_TOPICS[3]['key']
    return ML_TOPICS[4]['key']


def questions_for_topic(domain_key, topic_key=None):
    questions = load_ml_questions()
    if not topic_key or topic_key == 'all':
        return questions
    if domain_key != 'ml':
        return questions
    return [q for q in questions if build_topic_for_question(q) == topic_key]


def topic_title_for_question(question):
    topic_key = build_topic_for_question(question)
    for topic in ML_TOPICS:
        if topic['key'] == topic_key:
            return topic['title']
    return question.get('domain', 'Unknown')


def question_page_items(domain_key, topic_key):
    questions = questions_for_topic(domain_key, topic_key)
    out = []
    for q in questions:
        out.append({
            'id': q.get('id'),
            'question': q.get('question'),
            'options': q.get('options', []),
            'answer': q.get('options', [])[q.get('answer', 0)] if q.get('options') else None,
            'explanation': q.get('explanation', ''),
            'difficulty': q.get('difficulty')
        })
    return out


def shuffle_question_options(question):
    options = list(question.get('options', []))
    answer_index = question.get('answer', 0)
    correct = options[answer_index] if 0 <= answer_index < len(options) else None
    random.shuffle(options)
    return options, options.index(correct) if correct in options else None


def build_quiz_question(question):
    opts, new_idx = shuffle_question_options(question)
    return {
        'id': question.get('id'),
        'question': question.get('question'),
        'options': opts,
        'answer_index': new_idx,
        'answer_text': opts[new_idx] if new_idx is not None else None,
        'explanation': question.get('explanation', ''),
        'difficulty': question.get('difficulty')
    }


def synthesize_chat_response(message):
    text = message.strip().lower()
    if not text:
        return "Hi there! Ask me anything about AI interview prep, quizzes, or study topics."
    if 'hello' in text or 'hi' in text or 'hey' in text:
        return "Hello! I'm your Prep assistant. Ask me about domains, quizzes, or how to practice for AI interviews."
    if 'domain' in text or 'topics' in text:
        return "We cover Machine Learning, Deep Learning, Data Preparation, Explainability, and AI System Design. You can open any domain from the home page or use the dropdown."
    if 'quiz' in text or 'questions' in text:
        return "Each quiz gives you 10 fresh questions every time. Click a topic page and then tap Start Quiz to begin."
    if 'machine' in text or 'ml' in text:
        return "Machine Learning is our first domain, with topics like supervised learning, model evaluation, feature engineering, and model selection."
    if 'deep' in text or 'dl' in text:
        return "Deep Learning covers neural network architectures like CNN, RNN, and transformers, plus training and deployment."
    if 'data' in text or 'preparation' in text:
        return "Data Preparation is about cleaning, feature engineering, pipelines, and making your data ready for models."
    if 'explain' in text or 'interpret' in text:
        return "Explainability helps you understand model decisions, interpret results, and handle bias or fairness questions."
    if 'design' in text or 'system' in text:
        return "AI System Design is about building scalable ML infrastructure, monitoring models, and production readiness."
    if 'score' in text or 'result' in text:
        return "At the end of every quiz you will see your score and whether each answer was correct. Keep practicing to improve."
    return "Great question! I can help with interview topics, quiz flow, and domain landing pages. Try asking for a domain summary or quiz guidance."


@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json(silent=True) or {}
    message = data.get('message', '')
    reply = synthesize_chat_response(message)
    return jsonify({'reply': reply})


@app.route('/')
def index():
    return render_template('index.html', topics=DOMAINS)


@app.route('/topics')
def topics():
    return render_template('topics.html', topics=DOMAINS)


@app.route('/practice')
def practice():
    sample_questions = [
        {
            'topic': topic_title_for_question(q),
            'text': q.get('question'),
            'tip': q.get('explanation', '')[:120],
            'answer': q.get('options', [])[q.get('answer', 0)] if q.get('options') else None
        }
        for q in load_ml_questions()[:50]
    ]
    return render_template('practice.html', topics=DOMAINS, questions=sample_questions)


@app.route('/domain/<domain_key>')
def domain_detail(domain_key):
    domain = get_domain(domain_key)
    if not domain:
        abort(404)
    return render_template('domain_detail.html', domain=domain, topics=DOMAINS)


@app.route('/domain/<domain_key>/<topic_key>')
def topic_detail(domain_key, topic_key):
    domain = get_domain(domain_key)
    if not domain:
        abort(404)
    topic = get_topic(domain, topic_key)
    if not topic:
        abort(404)
    questions = question_page_items(domain_key, topic_key)
    return render_template('topic_detail.html', domain=domain, topic=topic, questions=questions, topics=DOMAINS)


@app.route('/quiz/<domain_key>/<topic_key>')
def quiz(domain_key, topic_key):
    domain = get_domain(domain_key)
    if not domain:
        abort(404)
    topic = get_topic(domain, topic_key) if topic_key != 'all' else None
    return render_template('quiz.html', domain=domain, topic=topic, topics=DOMAINS)


@app.route('/api/quiz/<domain_key>/<topic_key>')
def api_quiz(domain_key, topic_key):
    count = int(request.args.get('count', 10))
    questions = questions_for_topic(domain_key, topic_key)
    random.shuffle(questions)
    selected = questions[:min(count, len(questions))]
    return jsonify([build_quiz_question(q) for q in selected])


@app.route('/resources')
def resources():
    resources = [
        {
            'title': 'Coursera AI For Everyone',
            'description': 'A practical introduction to AI applications and workflows.',
            'link': 'https://www.coursera.org/learn/ai-for-everyone'
        },
        {
            'title': 'Fast.ai Deep Learning Course',
            'description': 'Hands-on deep learning with practical examples and exercises.',
            'link': 'https://www.fast.ai/'
        },
        {
            'title': 'Kaggle Learn Python',
            'description': 'Data science and machine learning fundamentals for interviews.',
            'link': 'https://www.kaggle.com/learn/python'
        }
    ]
    return render_template('resources.html', topics=DOMAINS, resources=resources)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', topics=DOMAINS)


@app.route('/runner')
def runner():
    return render_template('quiz_runner.html', topics=DOMAINS)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
