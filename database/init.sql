-- Initialize PostgreSQL Database Schema for Multimodal Fake News & Misinformation Detector

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table: predictions
CREATE TABLE IF NOT EXISTS predictions (
    id VARCHAR(36) PRIMARY KEY,
    input_type VARCHAR(20) NOT NULL,
    text_content TEXT,
    image_path VARCHAR(500),
    url VARCHAR(1000),
    prediction VARCHAR(20) NOT NULL,
    confidence FLOAT NOT NULL,
    text_score FLOAT DEFAULT 0.0,
    image_score FLOAT DEFAULT 0.0,
    multimodal_score FLOAT DEFAULT 0.0,
    alignment_score FLOAT DEFAULT 0.0,
    model_version VARCHAR(50) NOT NULL,
    cached BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_predictions_prediction ON predictions(prediction);
CREATE INDEX IF NOT EXISTS idx_predictions_input_type ON predictions(input_type);

-- Table: feedback
CREATE TABLE IF NOT EXISTS feedback (
    id VARCHAR(36) PRIMARY KEY,
    prediction_id VARCHAR(36) NOT NULL REFERENCES predictions(id) ON DELETE CASCADE,
    human_label VARCHAR(20) NOT NULL,
    reviewer_comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_feedback_prediction_id ON feedback(prediction_id);

-- Table: audit_logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id VARCHAR(36) PRIMARY KEY,
    action VARCHAR(100) NOT NULL,
    prediction_id VARCHAR(36),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);

-- Table: model_versions
CREATE TABLE IF NOT EXISTS model_versions (
    id VARCHAR(36) PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial model version entry
INSERT INTO model_versions (id, model_name, version, metrics, created_at)
VALUES (
    'mv-001',
    'Multimodal Transformer Baseline (RoBERTa + CLIP)',
    '0.1.0',
    '{"accuracy": 0.82, "f1_macro": 0.78, "status": "active", "demo_mode": true}'::jsonb,
    CURRENT_TIMESTAMP
) ON CONFLICT (id) DO NOTHING;
