TRUNCATE TABLE tasks, sprints, project_members, projects, users RESTART IDENTITY CASCADE;
INSERT INTO users (username, email, first_name, last_name, team, job_title, role, avatar_url)
VALUES
('apandey', 'ananya.pandey@company.com', 'Ananya', 'Pandey', 'Frontend', 'UI Engineer', 'Member', NULL),
('rpatel', 'riya.patel@company.com', 'Riya', 'Patel', 'Backend', 'Backend Developer', 'Member', NULL),
('psharma', 'priya.sharma@company.com', 'Priya', 'Sharma', 'QA', 'QA Engineer', 'Member', NULL),
('nreddy', 'neha.reddy@company.com', 'Neha', 'Reddy', 'DevOps', 'DevOps Engineer', 'Member', NULL),
('kverma', 'kavya.verma@company.com', 'Kavya', 'Verma', 'Frontend', 'React Developer', 'Member', NULL),
('smishra', 'sneha.mishra@company.com', 'Sneha', 'Mishra', 'Backend', 'Node.js Developer', 'Member', NULL),
('eclark', 'emma.clark@company.com', 'Emma', 'Clark', 'Frontend', 'UI/UX Designer', 'Member', NULL),
('lthomas', 'lucy.thomas@company.com', 'Lucy', 'Thomas', 'QA', 'QA Analyst', 'Member', NULL),
('jwilson', 'james.wilson@company.com', 'James', 'Wilson', 'DevOps', 'Cloud Engineer', 'Member', NULL),
('akumar', 'akash.kumar@company.com', 'Akash', 'Kumar', 'Backend', 'Java Developer', 'Member', NULL),
('sgupta', 'sanjay.gupta@company.com', 'Sanjay', 'Gupta', 'DevOps', 'Site Reliability Engineer', 'Member', NULL),
('vjain', 'vikas.jain@company.com', 'Vikas', 'Jain', 'Data Science', 'Data Analyst', 'Member', NULL),
('aroy', 'amit.roy@company.com', 'Amit', 'Roy', 'Mobile', 'Android Developer', 'Member', NULL),
('dsingh', 'deepak.singh@company.com', 'Deepak', 'Singh', 'Security', 'Security Engineer', 'Member', NULL),
('sjohnson', 'sarah.johnson@company.com', 'Sarah', 'Johnson', 'Product', 'Product Manager', 'Admin', NULL),
('emiller', 'emily.miller@company.com', 'Emily', 'Miller', 'Frontend', 'Angular Developer', 'Member', NULL),
('brown', 'olivia.brown@company.com', 'Olivia', 'Brown', 'Design', 'Graphic Designer', 'Member', NULL),
('nlewis', 'nicole.lewis@company.com', 'Nicole', 'Lewis', 'Marketing', 'Marketing Specialist', 'Member', NULL),
('kking', 'kimberly.king@company.com', 'Kimberly', 'King', 'HR', 'HR Generalist', 'Member', NULL),
('dwilliams', 'david.williams@company.com', 'David', 'Williams', 'Backend', 'Python Developer', 'Member', NULL),
('mjones', 'michael.jones@company.com', 'Michael', 'Jones', 'Data Science', 'Machine Learning Eng.', 'Member', NULL),
('rgarcia', 'robert.garcia@company.com', 'Robert', 'Garcia', 'Mobile', 'iOS Developer', 'Member', NULL),
('csmith', 'chris.smith@company.com', 'Chris', 'Smith', 'SRE', 'Systems Engineer', 'Member', NULL),
('jmartin', 'john.martin@company.com', 'John', 'Martin', 'QA', 'Automation Tester', 'Member', NULL),
('mfischer', 'maria.fischer@company.com', 'Maria', 'Fischer', 'Frontend', 'Vue.js Developer', 'Member', NULL),
('svogel', 'sophia.vogel@company.com', 'Sophia', 'Vogel', 'Design', 'UI/UX Designer', 'Member', NULL),
('hleblanc', 'hugo.leblanc@company.com', 'Hugo', 'Leblanc', 'Backend', 'PHP Developer', 'Member', NULL),
('mrossi', 'marco.rossi@company.com', 'Marco', 'Rossi', 'DevOps', 'Kubernetes Specialist', 'Member', NULL),
('lschmidt', 'lukas.schmidt@company.com', 'Lukas', 'Schmidt', 'Security', 'Penetration Tester', 'Member', NULL);

DO $$
DECLARE
    i INT;
    creator TEXT;
    manager_id INT;
    project_names TEXT[] := ARRAY[
        'E-commerce Platform Revamp', 'Mobile App Redesign', 'Internal CRM Development', 'Data Analytics Dashboard',
        'Cloud Migration Project', 'Customer Support Automation', 'AI-Powered Recommendation Engine',
        'Website Performance Optimization', 'Payment Gateway Integration', 'Inventory Management System',
        'Security Audit & Enhancement', 'DevOps Pipeline Automation', 'New User Onboarding Flow',
        'API Gateway Implementation', 'Marketing Campaign Management Tool'
    ];
BEGIN
    FOR i IN 1..15 LOOP
        IF i % 2 = 0 THEN
            creator := 'apandey';
        ELSE
            creator := 'eclark';
        END IF;
        SELECT id INTO manager_id FROM users WHERE username = creator;
        INSERT INTO projects (name, description, created_date, created_by, project_manager_id)
        VALUES (
            project_names[i],
            'Detailed description for the ' || project_names[i] || ' project, focusing on its core objectives and scope.',
            DATE '2025-04-01' + ((i-1) * INTERVAL '7 days'), 
            creator,
            manager_id
        );
    END LOOP;
END $$;

DO $$
DECLARE
    proj RECORD;
    all_user_ids INT[];
    all_usernames TEXT[];
    all_first_names TEXT[];
    all_last_names TEXT[];
    u_idx INT := 1;
    pm_name TEXT;
    num_users INT;
BEGIN
    SELECT
        array_agg(id ORDER BY id),
        array_agg(username ORDER BY id),
        array_agg(first_name ORDER BY id),
        array_agg(last_name ORDER BY id)
    INTO
        all_user_ids, all_usernames, all_first_names, all_last_names
    FROM users;

    SELECT array_length(all_user_ids, 1) INTO num_users;

    FOR proj IN SELECT * FROM projects ORDER BY id LOOP
        SELECT first_name || ' ' || last_name INTO pm_name FROM users WHERE id = proj.project_manager_id;

        FOR i IN 1..5 LOOP 
            u_idx := ((proj.id - 1) * 5 + i - 1) % num_users + 1;

            INSERT INTO project_members (user_id, project_id, username, first_name, last_name, project_name, project_manager_name)
            VALUES (
                all_user_ids[u_idx],
                proj.id,
                all_usernames[u_idx],
                all_first_names[u_idx],
                all_last_names[u_idx],
                proj.name,
                pm_name
            );
        END LOOP;
    END LOOP;
END $$;

DO $$
DECLARE
    proj RECORD;
    sprint_start DATE;
    i INT;
BEGIN
    FOR proj IN SELECT * FROM projects ORDER BY id LOOP
        sprint_start := proj.created_date;
        FOR i IN 1..3 LOOP
            INSERT INTO sprints (name, goal, status, start_date, end_date, created_date, planned_release_date, project_id, created_by)
            VALUES (
                'Sprint ' || i || ' - ' || proj.name,
                'Complete key features for ' || CASE i WHEN 1 THEN 'Phase 1' WHEN 2 THEN 'core functionalities' ELSE 'final integrations' END || ' of ' || proj.name,
                'Planning',
                sprint_start,
                sprint_start + INTERVAL '13 days',
                sprint_start,
                sprint_start + INTERVAL '13 days',
                proj.id,
                proj.created_by
            );
            sprint_start := sprint_start + INTERVAL '14 days';
        END LOOP;
    END LOOP;
END $$;

DO $$
DECLARE
    spr RECORD;
    members INT[];
    member_usernames TEXT[];
    t INT;
    task_titles TEXT[] := ARRAY[
        'Develop User Authentication Module', 'Design and Implement Dashboard UI', 'Create API for Product Catalog',
        'Optimize Database Queries for Performance', 'Set Up CI/CD Pipeline for Frontend', 'Conduct User Acceptance Testing',
        'Implement Password Encryption and Hashing', 'Build Responsive Navigation Bar', 'Integrate Third-Party Payment Gateway',
        'Refactor Legacy Codebase', 'Configure Cloud Load Balancers', 'Write Unit Tests for Backend Services',
        'Develop Mobile Push Notification Service', 'Perform Security Vulnerability Scan', 'Design Marketing Landing Page',
        'Implement Data Export Functionality', 'Automate Daily Data Backups', 'Create Admin Panel for Content Management',
        'Enhance Search Functionality with Filters', 'Debug and Resolve Production Issues',
        'Research and Integrate New Analytics Tool', 'Improve Error Logging and Monitoring', 'Update API Documentation',
        'Conduct A/B Testing for New Feature', 'Develop Chatbot Integration', 'Implement Geolocation Services',
        'Optimize Image Loading Performance', 'Design Email Notification Templates', 'Build Microservice for User Profiles',
        'Set Up Distributed Caching System'
    ];
    due_date DATE;
    owner_id INT;
    owner_username TEXT;
    random_task_title TEXT;
    title_idx INT;
BEGIN
    FOR spr IN SELECT s.*, p.id as project_id FROM sprints s JOIN projects p ON s.project_id = p.id ORDER BY s.id LOOP
        SELECT array_agg(user_id ORDER BY user_id), array_agg(username ORDER BY user_id) INTO members, member_usernames
        FROM project_members WHERE project_id = spr.project_id LIMIT 5;

        FOR t IN 1..20 LOOP
            owner_id := members[((t-1) % 5) + 1];
            owner_username := member_usernames[((t-1) % 5) + 1];
            due_date := spr.start_date + ((t-1) % 14) * INTERVAL '1 day';
            title_idx := (random() * (array_length(task_titles, 1) - 1) + 1)::INT;
            random_task_title := task_titles[title_idx];

            INSERT INTO tasks (
                title, description, status, priority, type, scope, tool, due_date, created_date, completed_date, last_updated_date,
                sprint_id, owner_id, created_by, project_id
            )
            VALUES (
                random_task_title,
                json_build_object('details', 'Detailed work for "' || random_task_title || '" within sprint ' || spr.name || '.'),
                CASE WHEN t % 4 = 0 THEN 'In Progress' WHEN t % 7 = 0 THEN 'Completed' ELSE 'To Do' END,
                CASE WHEN t % 5 = 0 THEN 'High' WHEN t % 3 = 0 THEN 'Low' ELSE 'Medium' END,
                CASE WHEN t % 2 = 0 THEN 'Feature' ELSE 'Bug' END,
                CASE WHEN t % 3 = 0 THEN 'Backend' WHEN t % 5 = 0 THEN 'DevOps' ELSE 'Frontend' END,
                CASE WHEN t % 3 = 0 THEN 'Python' WHEN t % 5 = 0 THEN 'AWS' ELSE 'React' END,
                due_date,
                spr.start_date,
                CASE WHEN t % 7 = 0 THEN due_date - INTERVAL '2 days' ELSE NULL END, -- completed tasks
                spr.start_date,
                spr.id,
                owner_id,
                owner_username,
                spr.project_id
            );
        END LOOP;
    END LOOP;
END $$;

DO $$
DECLARE
    task_record RECORD;
    tasks_to_update INT;
    completed_count INT := 0;
    days_duration INT;
    random_days_offset INT;
    max_completion_timestamp TIMESTAMP WITHOUT TIME ZONE := '2025-06-03 23:59:59';
BEGIN
    SELECT COUNT(*) INTO tasks_to_update FROM tasks;

    tasks_to_update := CEIL(tasks_to_update * 0.60);

    RAISE NOTICE 'Attempting to complete % tasks before June 4th, 2025.', tasks_to_update;

    FOR task_record IN
        SELECT id, created_date
        FROM tasks
        WHERE status != 'Completed'
        ORDER BY RANDOM()
    LOOP
        IF completed_count < tasks_to_update THEN
            days_duration := (max_completion_timestamp::DATE - task_record.created_date::DATE);

            IF days_duration < 0 THEN
                days_duration := 0;
            END IF;

            IF days_duration > 0 THEN
                random_days_offset := FLOOR(RANDOM() * (days_duration + 1));
            ELSE
                random_days_offset := 0;
            END IF;

            UPDATE tasks
            SET
                status = 'Completed',
                completed_date = LEAST(max_completion_timestamp, task_record.created_date + (random_days_offset * INTERVAL '1 day')),
                last_updated_date = NOW()
            WHERE id = task_record.id;

            completed_count := completed_count + 1;
        ELSE
            EXIT; 
        END IF;
    END LOOP;

    RAISE NOTICE 'Successfully completed % tasks.', completed_count;

END $$;