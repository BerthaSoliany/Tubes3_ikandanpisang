CREATE TABLE IF NOT EXISTS ApplicantProfile (
    applicant_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) DEFAULT NULL,
    last_name VARCHAR(50) DEFAULT NULL,
    date_of_birth DATE DEFAULT NULL,
    address VARCHAR(255) DEFAULT NULL,
    phone_number VARCHAR(20) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS ApplicationDetail (
    detail_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    applicant_id INT NOT NULL,
    application_role VARCHAR(100) DEFAULT NULL,
    cv_path TEXT,
    FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
);

CREATE INDEX idx_applicant_name ON ApplicantProfile(first_name, last_name);
CREATE INDEX idx_application_role ON ApplicationDetail(application_role);
CREATE INDEX idx_applicant_id ON ApplicationDetail(applicant_id);