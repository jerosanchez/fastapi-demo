-- Sample data
-- All hashed passwords correspond to "password123"
INSERT INTO
    users (
        id,
        email,
        password,
        created_at,
        is_active
    )
VALUES (
        'b3c1a7e2-4f8d-4a1e-9c2d-5e6f7a8b9c0d',
        'john.doe@example.com',
        '$2b$12$JqMDYlEya7QEZX3UJxOHNeofsT/ot99TRxTpwiAKiiJZ4yaBy.UTa',
        '2025-01-03T10:15:00Z',
        true
    ),
    (
        'c4d2e3f1-5b6a-7c8d-9e0f-2b3c4d5e6f7a',
        'alice.smith@example.com',
        '$2b$12$JqMDYlEya7QEZX3UJxOHNeofsT/ot99TRxTpwiAKiiJZ4yaBy.UTa',
        '2025-03-12T08:30:00Z',
        true
    ),
    (
        'd5e6f7a8-9b0c-1d2e-3f4a-5b6c7d8e9f0a',
        'bob.jones@example.com',
        '$2b$12$JqMDYlEya7QEZX3UJxOHNeofsT/ot99TRxTpwiAKiiJZ4yaBy.UTa',
        '2025-06-25T14:45:00Z',
        true
    );

INSERT INTO
    posts (
        id,
        owner_id,
        title,
        content,
        published,
        rating,
        created_at
    )
VALUES
    -- John Doe's posts (3)
    (
        'e2f1c3b4-5d6e-7a8b-9c0d-1e2f3a4b5c6d',
        'b3c1a7e2-4f8d-4a1e-9c2d-5e6f7a8b9c0d',
        'Getting Started with FastAPI for AI Projects',
        'FastAPI is a modern Python web framework that makes it easy to build APIs for machine learning models. In this post, I share tips for structuring your first AI backend.',
        true,
        5,
        '2025-01-05T09:00:00Z'
    ),
    (
        'f4e3d2c1-b5a6-7c8d-9e0f-1a2b3c4d5e6f',
        'b3c1a7e2-4f8d-4a1e-9c2d-5e6f7a8b9c0d',
        'Deploying Machine Learning Models with Docker',
        'Containerization simplifies the deployment of AI models. Here, I explain how to use Docker to package and serve your machine learning models efficiently.',
        false,
        3,
        '2025-02-10T16:20:00Z'
    ),
    (
        'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d',
        'b3c1a7e2-4f8d-4a1e-9c2d-5e6f7a8b9c0d',
        'Best Practices for Training Neural Networks',
        'Training deep learning models can be tricky. This article covers essential practices like data normalization, regularization, and monitoring validation loss.',
        true,
        4,
        '2025-03-01T12:10:00Z'
    ),

-- Alice Smith's posts (5)
(
    'b7c8d9e0-1f2a-3b4c-5d6e-7f8a9b0c1d2e',
    'c4d2e3f1-5b6a-7c8d-9e0f-2b3c4d5e6f7a',
    'Building Chatbots with NLP',
    'Natural Language Processing enables the creation of intelligent chatbots. This post explores libraries and techniques for building conversational AI.',
    true,
    5,
    '2025-03-15T11:00:00Z'
),
(
    'c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f',
    'c4d2e3f1-5b6a-7c8d-9e0f-2b3c4d5e6f7a',
    'Fine-Tuning Transformers for Custom Tasks',
    'Transformers have revolutionized NLP. Learn how to fine-tune pre-trained models for your own datasets and tasks.',
    true,
    4,
    '2025-04-10T15:30:00Z'
),
(
    'd9e0f1a2-3b4c-5d6e-7f8a-9b0c1d2e3f4a',
    'c4d2e3f1-5b6a-7c8d-9e0f-2b3c4d5e6f7a',
    'Serving AI Models with FastAPI and Uvicorn',
    'FastAPI and Uvicorn make it easy to serve AI models in production. This post covers deployment strategies and performance tips.',
    true,
    5,
    '2025-05-22T10:05:00Z'
),
(
    'e0f1a2b3-4c5d-6e7f-8a9b-0c1d2e3f4a5b',
    'c4d2e3f1-5b6a-7c8d-9e0f-2b3c4d5e6f7a',
    'Monitoring AI Model Performance in Production',
    'Monitoring deployed models is crucial for reliability. Here are tools and metrics to track your AI systems in real time.',
    false,
    3,
    '2025-07-03T18:40:00Z'
),
(
    'f1a2b3c4-5d6e-7f8a-9b0c-1d2e3f4a5b6c',
    'c4d2e3f1-5b6a-7c8d-9e0f-2b3c4d5e6f7a',
    'Automating Data Labeling for Machine Learning',
    'Efficient data labeling accelerates AI development. This article discusses automation tools and best practices for labeling datasets.',
    true,
    4,
    '2025-08-15T07:55:00Z'
),

-- Bob Jones's posts (4)
(
    'a2b3c4d5-e6f7-8a9b-0c1d-2e3f4a5b6c7d',
    'd5e6f7a8-9b0c-1d2e-3f4a-5b6c7d8e9f0a',
    'Introduction to Computer Vision with PyTorch',
    'PyTorch is a flexible framework for computer vision tasks. This post introduces image classification and transfer learning with PyTorch.',
    true,
    5,
    '2025-06-28T13:00:00Z'
),
(
    'b3c4d5e6-f7a8-9b0c-1d2e-3f4a5b6c7d8e',
    'd5e6f7a8-9b0c-1d2e-3f4a-5b6c7d8e9f0a',
    'Optimizing Inference Speed for AI APIs',
    'Speed is critical for AI-powered APIs. Learn how to optimize inference time using batching, quantization, and hardware acceleration.',
    true,
    4,
    '2025-07-20T09:45:00Z'
),
(
    'c4d5e6f7-a8b9-0c1d-2e3f-4a5b6c7d8e9f',
    'd5e6f7a8-9b0c-1d2e-3f4a-5b6c7d8e9f0a',
    'Data Augmentation Techniques for Deep Learning',
    'Data augmentation can improve model generalization. This post reviews popular augmentation methods for images and text.',
    false,
    3,
    '2025-08-30T17:25:00Z'
),
(
    'd5e6f7a8-b9c0-1d2e-3f4a-5b6c7d8e9f0b',
    'd5e6f7a8-9b0c-1d2e-3f4a-5b6c7d8e9f0a',
    'Using GPUs for Scalable AI Training',
    'GPUs accelerate deep learning training. Here, I discuss how to leverage GPU resources for faster model development and experimentation.',
    true,
    5,
    '2025-09-15T21:10:00Z'
);

-- Sample votes data
INSERT INTO votes (post_id, user_id) VALUES
    -- John's posts getting votes
    ('e2f1c3b4-5d6e-7a8b-9c0d-1e2f3a4b5c6d', 'c4d2e3f1-5b6a-7c8d-9e0f-2b3c4d5e6f7a'), -- Alice votes on John's FastAPI post
    ('e2f1c3b4-5d6e-7a8b-9c0d-1e2f3a4b5c6d', 'd5e6f7a8-9b0c-1d2e-3f4a-5b6c7d8e9f0a'), -- Bob votes on John's FastAPI post
    ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d', 'c4d2e3f1-5b6a-7c8d-9e0f-2b3c4d5e6f7a'), -- Alice votes on John's Neural Networks post
    
    -- Alice's posts getting votes
    ('b7c8d9e0-1f2a-3b4c-5d6e-7f8a9b0c1d2e', 'b3c1a7e2-4f8d-4a1e-9c2d-5e6f7a8b9c0d'), -- John votes on Alice's Chatbots post
    ('b7c8d9e0-1f2a-3b4c-5d6e-7f8a9b0c1d2e', 'd5e6f7a8-9b0c-1d2e-3f4a-5b6c7d8e9f0a'), -- Bob votes on Alice's Chatbots post
    ('c8d9e0f1-2a3b-4c5d-6e7f-8a9b0c1d2e3f', 'b3c1a7e2-4f8d-4a1e-9c2d-5e6f7a8b9c0d'), -- John votes on Alice's Transformers post
    ('d9e0f1a2-3b4c-5d6e-7f8a-9b0c1d2e3f4a', 'd5e6f7a8-9b0c-1d2e-3f4a-5b6c7d8e9f0a'), -- Bob votes on Alice's FastAPI/Uvicorn post
    ('f1a2b3c4-5d6e-7f8a-9b0c-1d2e3f4a5b6c', 'b3c1a7e2-4f8d-4a1e-9c2d-5e6f7a8b9c0d'), -- John votes on Alice's Data Labeling post
    
    -- Bob's posts getting votes
    ('a2b3c4d5-e6f7-8a9b-0c1d-2e3f4a5b6c7d', 'b3c1a7e2-4f8d-4a1e-9c2d-5e6f7a8b9c0d'), -- John votes on Bob's PyTorch post
    ('a2b3c4d5-e6f7-8a9b-0c1d-2e3f4a5b6c7d', 'c4d2e3f1-5b6a-7c8d-9e0f-2b3c4d5e6f7a'), -- Alice votes on Bob's PyTorch post
    ('b3c4d5e6-f7a8-9b0c-1d2e-3f4a5b6c7d8e', 'c4d2e3f1-5b6a-7c8d-9e0f-2b3c4d5e6f7a'), -- Alice votes on Bob's Inference Speed post
    ('d5e6f7a8-b9c0-1d2e-3f4a-5b6c7d8e9f0b', 'b3c1a7e2-4f8d-4a1e-9c2d-5e6f7a8b9c0d'), -- John votes on Bob's GPU post
    ('d5e6f7a8-b9c0-1d2e-3f4a-5b6c7d8e9f0b', 'c4d2e3f1-5b6a-7c8d-9e0f-2b3c4d5e6f7a'); -- Alice votes on Bob's GPU post